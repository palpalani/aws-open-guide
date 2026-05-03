# Playbook: GenAI / RAG application

> Retrieval-augmented generation on AWS — Bedrock + a vector store + a retrieval layer + safety. Grounded answers, controlled cost, and a path to evaluation.

**Tags:** `production-ready` · `complex`

**Status:** ✅ Available

---

## 1. Problem

You want users to ask questions in natural language and get grounded answers based on **your** content — docs, support tickets, codebase, transcripts. Pure LLMs hallucinate; pure search doesn't synthesise. RAG threads the needle: retrieve relevant passages, hand them to an LLM, return a synthesised answer with citations.

Building a demo takes a weekend. Building one that's **accurate, cheap, safe, evaluable, and tenant-aware** is a different project. This playbook is the second one.

## 2. Constraints

- **Corpus size** — KB to TB; affects vector DB choice
- **Document update cadence** — daily, hourly, real-time?
- **Query volume** — QPS at peak; affects token cost and concurrency
- **Latency target** — typically 2–5s for chat-style; 30s+ for agent flows
- **Quality threshold** — hallucination rate, citation accuracy, refusal rate
- **Safety** — prompt injection resistance, content filtering, PII redaction
- **Tenancy** — single-tenant vs multi-tenant (per-tenant data + per-tenant cost)
- **Compliance** — HIPAA, SOC2, data residency for both corpus and prompts

## 3. Reference architecture

```
                Ingestion (offline / scheduled)
─────────────────────────────────────────────────────────────────
┌────────────┐   ┌──────────┐   ┌──────────┐   ┌─────────────┐
│  Sources   │──▶│  Loader  │──▶│  Chunker │──▶│  Embedding  │
│  (S3, web, │   │  (Lambda,│   │  (split, │   │  (Bedrock   │
│   Notion,  │   │   Glue)  │   │   overlap│   │   Titan /   │
│   GitHub…) │   │          │   │   metadat│   │   Cohere)   │
└────────────┘   └──────────┘   └──────────┘   └──────┬──────┘
                                                       │
                                                       ▼
                                              ┌─────────────┐
                                              │ Vector store│
                                              │ (OpenSearch │
                                              │  k-NN /     │
                                              │  Aurora     │
                                              │  pgvector / │
                                              │  Pinecone)  │
                                              └─────────────┘

                Query (online)
─────────────────────────────────────────────────────────────────
┌────────────┐   ┌──────────┐   ┌──────────┐   ┌─────────────┐
│  User      │──▶│ API GW + │──▶│ Retrieve │──▶│  Re-rank    │
│  question  │   │ Lambda   │   │ top-k    │   │  (Cohere /  │
│            │   │          │   │ from     │   │   Bedrock)  │
└────────────┘   └────┬─────┘   │ vector   │   └──────┬──────┘
                      │         │ store    │          │
                      │         └──────────┘          ▼
                      │                        ┌─────────────┐
                      │                        │  Bedrock    │
                      │                        │  LLM        │
                      │                        │  (Claude /  │
                      │                        │   Nova /    │
                      │                        │   Llama)    │
                      │                        └──────┬──────┘
                      │                               │
                      ▼                               ▼
              ┌──────────────┐                 ┌─────────────┐
              │  Bedrock     │                 │  Response + │
              │  Guardrails  │◀────────────────│  citations  │
              └──────────────┘                 └─────────────┘
                      │
                      ▼
              ┌──────────────┐
              │  Logging,    │
              │  evals,      │
              │  metering    │
              └──────────────┘
```

**Ingestion (offline, idempotent):**

1. **Load** — pull from sources; track checksums to detect changes.
2. **Chunk** — split documents into passages (typically 500–1,500 tokens) with overlap (10–20%); preserve metadata (source URL, section, tenant, doc-type).
3. **Embed** — Bedrock Titan or Cohere embedding model; store vectors with metadata.
4. **Index** — OpenSearch k-NN, Aurora pgvector, DocumentDB vector, or third-party (Pinecone, Weaviate).

**Query (online):**

5. **Retrieve** — embed the query, k-NN against vector store, return top-k passages (typically k=10–50).
6. **Re-rank** (optional but high-impact) — Cohere Rerank or Bedrock model scores passages by relevance, prunes to top-3–10.
7. **Compose prompt** — system prompt + retrieved passages + user question; cite passages by ID.
8. **Generate** — Bedrock LLM call; streaming if user-facing.
9. **Guardrails** — Bedrock Guardrails layer for content filtering, PII redaction, denied topics; both pre- (input) and post- (output).
10. **Return** — answer with citation references back to source passages.

## 4. Architecture variants

| Variant | When | Notes |
|---------|------|-------|
| **Bedrock Knowledge Bases** | Most teams; managed RAG | AWS-managed retrieval + chunking; less control |
| **Self-built (this playbook)** | Custom retrieval, re-rank, multi-step | More control, more ops |
| **OpenSearch k-NN** | Existing OpenSearch, hybrid search | Lexical + vector; storage cost grows |
| **Aurora pgvector** | Already on Postgres | Familiar; scales to medium |
| **DocumentDB vector** | Already on DocumentDB | Same idea; AWS-native |
| **S3 Vectors (preview)** | Cost-conscious cold vector store | New; evaluate against alternatives |
| **Pinecone / Weaviate / Qdrant** | Best-in-class vector DB | Vendor cost; managed or self-host |
| **Agentic / multi-step** | Tool use, planning, multiple retrievals | Bedrock Agents or LangGraph; cost and complexity grow |
| **Multi-tenant SaaS RAG** | Per-tenant corpus + cost | See [`multi-tenant-saas.md`](multi-tenant-saas.md) + Multi-tenant GenAI on Bedrock (References — Production guides) |

## 5. Failure modes

Cross-cutting patterns: see [`failure-first.md`](failure-first.md). RAG-specific:

### Hallucination

- **What it looks like** — answer sounds confident but contradicts the corpus or invents facts
- **Why it happens** — retrieval missed the relevant passage; model ignores context; question outside corpus scope
- **Detection** — eval suite with golden questions and expected answers; user feedback; LLM-as-judge for citation faithfulness
- **Recovery** — improve retrieval (chunking, hybrid search, re-rank); prompt engineering ("answer only from provided context, otherwise say you don't know"); refusal mode for out-of-scope

### Retrieval misses

- **What it looks like** — relevant doc exists but doesn't appear in top-k
- **Why it happens** — bad chunking (split mid-concept), embedding model weak for the domain, query rewording differs from doc phrasing
- **Recovery** — hybrid search (vector + BM25); query expansion; better chunking with semantic boundaries; re-rank larger k

### Stale corpus

- **What it looks like** — answers reference outdated content
- **Why it happens** — ingestion broke; cadence too slow
- **Detection** — track last-updated timestamp per source; alarm on staleness
- **Recovery** — incremental ingestion (process only changed docs); EventBridge schedule; checksum-based change detection

### Prompt injection

- **What it looks like** — user input or retrieved content tries to override system prompt ("ignore previous instructions, …")
- **Why it happens** — adversarial input, or compromised content in the corpus
- **Recovery** — Bedrock Guardrails for prompt-injection detection; structured output with strong schema; never execute model output as code without sandbox; trust boundary between user input and system prompt

### Sensitive data leakage

- **What it looks like** — model returns PII / secrets that are in the corpus
- **Why it happens** — corpus contains sensitive data; access controls on retrieval missing
- **Recovery** — redact PII at ingestion; per-tenant or per-role retrieval filters; Bedrock Guardrails PII filter on output; audit logs of every retrieval

### Cost runaway

- **What it looks like** — bill explodes; one user/agent loop responsible
- **Why it happens** — long system prompts, high retrieval `top_k`, agent loops without termination, abusive user
- **Detection** — per-user token meter; cost alarms
- **Recovery** — prompt caching for repeated system prompts; cap `top_k`; agent iteration limits; per-tenant token budgets; rate-limit at API

### Latency degradation

- **What it looks like** — response time creeps up; users abandon
- **Why it happens** — vector store cold cache, cold model, large prompts, many sequential tool calls
- **Recovery** — warm-up retrieval cache; provisioned throughput on Bedrock for hot models; trim retrieval `top_k`; parallelise where possible

### Multi-tenant bleeding

- **What it looks like** — tenant A's question retrieves tenant B's content
- **Why it happens** — missing tenant filter in vector query; shared collection without tenancy metadata
- **Recovery** — tenant ID is metadata on every chunk; **always** included as filter on retrieval; integration tests assert isolation; see [`multi-tenant-saas.md`](multi-tenant-saas.md)

## 6. Cost model

Worked example: 100k queries/month, average 8 retrieved passages × 800 tokens = 6.4k input tokens + 500 output tokens; using Claude Sonnet 4.5; Titan embeddings.

| Line item | Monthly | Notes |
|-----------|---------|-------|
| Embedding (queries: 100k × 50 tokens) | ~$0.50 | Cheap |
| Embedding (corpus: 10M tokens initial + monthly delta) | ~$10 | One-time + ongoing |
| Vector store (OpenSearch m6g.large × 3) | ~$430 | Or pgvector on Aurora; varies |
| Bedrock LLM input (100k × 6.4k tokens × $3/M) | ~$1,920 | Bulk of cost |
| Bedrock LLM output (100k × 500 tokens × $15/M) | ~$750 | |
| Bedrock Guardrails | ~$10 | $0.75/1k policy applications |
| Re-rank (Cohere via Bedrock, 100k × 50 docs) | ~$200 | Optional but high-quality lift |
| API Gateway, Lambda, logging | ~$50 | Plumbing |
| **Total** | **~$3,370** | ~$0.034 per query |

**With prompt caching** for shared system prompt (~2k tokens): input cost drops 40–60% on repeated calls. **With cheaper model** for routing (Haiku for classification, Sonnet for synthesis): another 20–40% cut.

**Scaling shape:** linear with queries × tokens. Vector store cost is mostly fixed (instance hours).

**Cost traps:**
- **Long unchanging system prompts not cached** — Bedrock prompt caching exists; use it
- **`top_k` set to 50 by default** — every extra passage is paid input tokens; tune ruthlessly
- **Agent loops without iteration cap** — runaway agent burns budget
- **Embedding model run on full corpus monthly** — incremental ingestion, only embed changed chunks
- **Vector store right-sizing** — over-provisioned OpenSearch is the silent killer
- **Streaming abandoned mid-stream** — full output still billed; user closing tab doesn't refund tokens
- **Bedrock model in non-US region** — token pricing varies by region; check before committing

## 7. When NOT to use this

- **Question can be answered by structured search** — full-text + filters is cheaper, more predictable, more debuggable
- **Corpus is one document** — pre-load into prompt instead of building retrieval
- **Real-time / sub-second response required** — RAG is multi-second; not a fit for in-flow autocomplete
- **No evaluation discipline** — without evals, you can't tell if changes help or hurt; don't ship in that state
- **Compliance forbids LLM use on the data** — verify before building

## 8. Alternatives

| Approach | Best for | Tradeoff |
|----------|----------|----------|
| **Self-built RAG (this playbook)** | Custom requirements | Most control, most work |
| **Bedrock Knowledge Bases** | Standard RAG, fast time-to-ship | Less control over chunking, retrieval, prompting |
| **Bedrock Agents** | Multi-step tool use | Built-in orchestration; observability less mature |
| **OpenAI Assistants / GPT** | Best-in-class quality | Vendor lock-in; data leaves AWS |
| **LangChain / LlamaIndex on AWS** | Framework speeds dev | Frameworks add complexity; pin versions |
| **Pinecone + OpenAI / Anthropic SDK** | Best-in-class vector + LLM | Multi-vendor; AWS data egress |
| **Semantic Kernel / Haystack** | Enterprise patterns | Same trade-off as LangChain |

For X-vs-Y: Bedrock vs SageMaker, Bedrock Agents vs Step Functions, Fine-tuning vs RAG on Bedrock — see Decision guides and Production guides in References.

## 9. Anti-patterns

- **No evaluation framework** — every change is a vibes-based judgment; ship eval set first
- **Trusting LLM-as-judge unconditionally** — use it as one signal; correlate with human review
- **Putting the entire document in the prompt** — token cost; quality often degrades past 100k tokens; chunk and retrieve
- **Chunking by character count** with no semantic awareness — splits mid-sentence, mid-section
- **No metadata on chunks** — can't filter by source, recency, tenant, permission
- **Single index for all tenants** — bleeding risk; per-tenant filter on every retrieval
- **No citation in the answer** — user can't verify; trust collapses on first hallucination
- **System prompt in every request without caching** — direct token waste at scale
- **Ignoring re-rank** — cheap cross-encoder re-rank improves top-k materially
- **Agent loops without budget cap** — runaway invocation; cost-based DoS
- **No request logging** — can't debug, can't improve, can't prove what happened
- **Treating the LLM as deterministic** — temperature, sampling, model updates change output; pin model version, snapshot eval results
- **Skipping guardrails** — production GenAI without content filtering is reputational risk; Bedrock Guardrails is cheap
- **Storing prompts and responses without redaction** — long-term data residue with PII

For cross-cutting AWS anti-patterns, see [`anti-patterns.md`](anti-patterns.md).

## 10. Production checklist

- [ ] **Evaluation suite** — golden questions with expected answers; CI runs evals on prompt or model changes
- [ ] **LLM-as-judge** for citation faithfulness alongside human spot-check
- [ ] **Hallucination rate target** documented and tracked; alarm on regression
- [ ] **Bedrock Guardrails** configured for input + output: prompt injection, PII, denied topics, custom word filter
- [ ] **Tenant ID on every chunk** and required as a filter on every retrieval (in multi-tenant)
- [ ] **Per-user / per-tenant token budgets**; rate limit at API
- [ ] **Cost alarms** at multiple thresholds; per-tenant cost report
- [ ] **Prompt caching** enabled for shared system prompts
- [ ] **Model version pinned** (e.g., `claude-sonnet-4.5`); upgrade is a deliberate change with re-evaluation
- [ ] **PII redaction at ingestion** for chunks; PII filter on output
- [ ] **Citations in every response**; source IDs traceable to original document
- [ ] **Refusal path** for out-of-scope or low-confidence retrievals
- [ ] **Agent iteration cap** if using agents
- [ ] **Logging** — request, retrieved chunk IDs, model, prompt tokens, output tokens, latency, user feedback
- [ ] **Streaming** for user-facing chat; non-streaming for batch / agent
- [ ] **Incremental ingestion** with checksum-based change detection; staleness alarm
- [ ] **Vector store backup / DR** plan
- [ ] **Drill** — corrupt corpus, prompt injection attack, agent loop; confirm guardrails fire

## 11. References

**Official:**
- [Amazon Bedrock Documentation](https://docs.aws.amazon.com/bedrock/) — full guide
- [Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html) — managed RAG
- [Bedrock Agents](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html) — tool use and orchestration
- [Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) — safety layer
- [Bedrock prompt caching](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html) — token discount on shared context
- [Bedrock pricing](https://aws.amazon.com/bedrock/pricing/) — per-model token pricing
- [OpenSearch k-NN](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/knn.html) — vector search
- [Aurora pgvector](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraPostgreSQL.VectorDB.html) — Postgres vector store
- [SageMaker JumpStart](https://docs.aws.amazon.com/sagemaker/latest/dg/studio-jumpstart.html) — pre-trained models
- [Designing serverless AI architectures (Prescriptive Guidance)](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-serverless/designing-serverless-ai-architectures.html) — official patterns

**Production guides:**
- [Build a RAG pipeline with Bedrock Knowledge Bases](https://www.factualminds.com/blog/how-to-build-rag-pipeline-amazon-bedrock-knowledge-bases/) — Bedrock-managed RAG walkthrough
- [Bedrock multi-agent supervisor pattern](https://www.factualminds.com/blog/aws-bedrock-multi-agent-supervisor-pattern/) — multi-agent orchestration
- [Multi-tenant GenAI on Bedrock](https://www.factualminds.com/blog/multi-tenant-genai-bedrock/) — RAG in SaaS
- [Fine-tuning vs RAG on Bedrock](https://www.factualminds.com/blog/fine-tuning-vs-rag-bedrock-when-to-use/) — when each fits

**Decision guides:**
- [Bedrock vs SageMaker](https://www.factualminds.com/compare/aws-bedrock-vs-sagemaker/) — managed model APIs vs custom training
- [Bedrock Agents vs Step Functions](https://www.factualminds.com/compare/aws-bedrock-agents-vs-step-functions/) — orchestration choice
- [Amazon Q vs ChatGPT Enterprise](https://www.factualminds.com/compare/amazon-q-vs-chatgpt-enterprise/) — productised GenAI choice

**OSS tools:**
- [LangChain](https://github.com/langchain-ai/langchain) — RAG / agent framework (Python / JS)
- [LlamaIndex](https://github.com/run-llama/llama_index) — RAG-focused framework
- [LangGraph](https://github.com/langchain-ai/langgraph) — graph-based agent orchestration
- [aws-genai-llm-chatbot](https://github.com/aws-samples/aws-genai-llm-chatbot) — AWS sample multi-model chatbot
- [bedrock-claude-chat](https://github.com/aws-samples/bedrock-claude-chat) — sample Bedrock chat app
- [ragas](https://github.com/explodinggradients/ragas) — RAG evaluation framework
- [DSPy](https://github.com/stanfordnlp/dspy) — programmatic prompt optimisation
- [Haystack](https://github.com/deepset-ai/haystack) — search and RAG pipelines

---

*See also: [`multi-tenant-saas.md`](multi-tenant-saas.md) · [`async-jobs.md`](async-jobs.md) · [`cost-pitfalls.md`](cost-pitfalls.md) · [GenAI architecture patterns in root README](../README.md#architecture-patterns).*
