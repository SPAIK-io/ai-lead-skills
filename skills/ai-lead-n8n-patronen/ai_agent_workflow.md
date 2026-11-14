# AI Agent Workflow Pattern

AI steps are only built when the lead says an AI connection is available in their n8n. Otherwise leave an empty placeholder (No Operation node) with a note that explains what the AI step would do. See `ai-lead-workflow-n8n`.

**Use Case**: An AI agent with tool access, memory, and reasoning sits inside a larger workflow — trigger feeds it, it decides and acts, output flows on.

This file covers where an AI agent sits in a workflow's architecture (trigger → agent → output, the `ai_*` sub-node connection types). It does not go deep into agent design (tool selection and `$fromAI` parameters, system prompts, structured output, memory, human review, RAG); keep a first prototype to one agent with one model and as few tools as possible.

---

## Pattern Structure

```
Trigger → AI Agent (Model + Tools + Memory + optional Output Parser) → [Process Response] → Output
```

**Key Characteristic**: AI-powered decision making with tool use. From the *workflow* angle, an agent is one node with a main input/output plus `ai_*` sub-node slots — it slots into the same trigger → process → deliver spine as every other pattern.

---

## Core AI Connection Types

Agent workflows wire sub-nodes into the agent with dedicated `ai_*` connection types — **not** the regular `main` connection. This is the single most important architectural fact: a tool wired to `main` is invisible to the agent (after import you see it in n8n as a node that is not attached to the agent's tool slot).

| Connection type | Wires in | Into slot |
|---|---|---|
| `ai_languageModel` | The LLM (OpenAI, Anthropic, Gemini, Ollama…) | model (required) |
| `ai_tool` | Any node the agent can call | tools |
| `ai_memory` | Conversation context store | memory |
| `ai_outputParser` | Structured-output parser | output parser |
| `ai_embedding` | Vector embeddings | RAG chain |
| `ai_vectorStore` | Vector database | RAG chain |
| `ai_document` | Document loaders | RAG ingest |
| `ai_textSplitter` | Text chunking | RAG ingest |

**Wiring direction**: a sub-node connects FROM itself TO the agent, and the connection lives on the sub-node keyed by its `ai_*` type. In the workflow JSON that is an entry under the sub-node's name in `connections`, keyed `"ai_tool"` (or `"ai_languageModel"`, etc.) instead of `"main"`. Multiple tools all stack on the same `ai_tool` index 0.

---

## Core Components

The agent has a **main input** (the user message / prompt) and up to four sub-node slots:

1. **Trigger** — Chat Trigger (chat UI/streaming), Webhook (API), Manual (testing), or Schedule (periodic). Feeds the agent's main input.
2. **Language Model** (`ai_languageModel`, required) — the reasoning engine. One chat-model sub-node; a second can be wired as a fallback.
3. **Tools** (`ai_tool`, optional but the whole point) — **ANY node can be a tool.** HTTP Request, a database node, a sub-workflow, Code, or a pre-built tool node connects via the `ai_tool` port and the agent calls it by name.
4. **Memory** (`ai_memory`, optional) — maintains conversation context across turns, keyed by a `sessionKey`.
5. **Output Parser** (`ai_outputParser`, optional) — forces structured JSON instead of free text.

**Critical output fact**: the AI Agent node puts its final answer in **`$json.output`** — not `$json.text` or `$json.response`. Downstream nodes reference `{{ $json.output }}`.

**Fan-out tip**: when several agents run in parallel (e.g. multiple research agents feeding one report), avoid funneling them into a Merge node — Merge `combineAll` does a cross-product and mishandles inputs arriving at different times (often yielding 0 output). Either have each agent deliver its own output directly, or collect same-shaped items with an **Aggregate** node followed by a Code node for formatting.

---

## Common Use Cases

Short architecture sketches. Each is a trigger → agent → output spine; the agent's sub-nodes are listed under it.

### 1. Conversational Chatbot
```
Webhook (chat message) → AI Agent → Webhook Response
                          ├─ Chat Model (ai_languageModel)
                          ├─ HTTP Request Tool — search knowledge base (ai_tool)
                          ├─ Database node — query orders (ai_tool)
                          └─ Window Buffer Memory, keyed on session_id (ai_memory)
```

### 2. Document Q&A (RAG)
```
Setup (run once):  Read Files → Text Splitter → Embeddings → Vector Store
Query (recurring): Webhook → AI Agent → Webhook Response
                              ├─ Chat Model (ai_languageModel)
                              ├─ Vector Store Tool — search docs (ai_tool)
                              └─ Buffer Memory (ai_memory)
```

### 3. Data Analysis Assistant
```
Webhook (data question) → AI Agent → Code (chart data) → Webhook Response
                          ├─ Chat Model (ai_languageModel)
                          ├─ Postgres node, read-only user (ai_tool)
                          └─ Code Tool — analysis (ai_tool)
```

### 4. Workflow Automation Agent
```
Slack (slash command) → AI Agent → Slack (status)
                        ├─ Chat Model (ai_languageModel)
                        ├─ HTTP Request Tool — GitHub API (ai_tool)
                        ├─ HTTP Request Tool — Deploy API (ai_tool)
                        └─ Postgres node — deployment logs (ai_tool)
```

### 5. Email Processing Agent
```
Email Trigger → AI Agent → Email (auto-response) → Slack (notify team)
                ├─ Chat Model (ai_languageModel)
                ├─ Vector Store Tool — similar tickets (ai_tool)
                └─ HTTP Request Tool — create Jira ticket (ai_tool)
```

---

## Security note

**Any tool that fetches third-party content** (HTTP Request, web search, external tool servers, scrapers) can return attacker-controlled text that reaches the agent's context — indirect prompt injection. If the agent can both *read the internet* AND *take an action the user can't undo*, put a guardrail (human review, read-only scopes) between them. For error handling in a first prototype keep it simple; wire an error output only where a node can fail (a model call or a tool call).

---

## Checklist for AI Agent Workflows

Architecture-level checks:

- [ ] Trigger feeds the agent's **main** input
- [ ] Language model wired via **`ai_languageModel`** (required)
- [ ] Tools wired via **`ai_tool`** ports — NOT `main` (a tool on `main` is disconnected from the agent)
- [ ] Memory wired via **`ai_memory`**, keyed on a stable `sessionKey` from the trigger — when conversation context is needed
- [ ] Output parser wired via **`ai_outputParser`** — when downstream needs strict JSON
- [ ] Downstream nodes read the response from **`{{ $json.output }}`**
- [ ] Parallel agents collected with **Aggregate**, not Merge `combineAll`
- [ ] Imports without red nodes, and every sub-node hangs under the agent (on `ai_*`, not `main`)
- [ ] Run with Execute workflow; open the agent and check its INPUT and OUTPUT panels (see SKILL.md "Workflow lifecycle" section)
- [ ] An administrator activates/publishes it; the lead does not

---

## Summary

**Key Points**:
1. An agent is **one node** with a main input/output plus `ai_*` sub-node slots — it fits the standard trigger → process → deliver spine.
2. **8 AI connection types** — wire the model with `ai_languageModel`, tools with `ai_tool`, memory with `ai_memory`, parsers with `ai_outputParser`. Never `main`.
3. **ANY node can be a tool** — connect it via the `ai_tool` port.
4. The response is in **`$json.output`**.
5. Only build the AI step when the lead has an AI connection in n8n; otherwise a No Operation placeholder with a note.

**Pattern**: Trigger → AI Agent (Model + Tools + Memory + optional Parser) → Output

**Related**:
- `ai-lead-workflow-n8n` — when to build an AI step, and the placeholder when there is no AI connection
- [webhook_processing.md](webhook_processing.md) — receiving chat messages
- [http_api_integration.md](http_api_integration.md) — tools that call APIs
- [database_operations.md](database_operations.md) — database tools for agents
- SKILL.md "Workflow lifecycle" section — import, run and check the workflow
