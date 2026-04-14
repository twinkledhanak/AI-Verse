# AI-Verse

AI-Verse is a lightweight backend playground to compare responses from multiple LLM providers using the same user prompt.

## Description

- AI-Verse currently focuses on **LLM API Integration** by connecting the backend to OpenAI and Anthropic through clean provider-specific modules.
- It also establishes the base for **Multi Model Orchestration** by sending the same prompt to multiple providers in parallel and returning their outputs together for comparison.
- The current implementation provides a simple foundation for prompt experimentation, including app-level input limits and model-level output token limits.

## Project Status

### Phase 1 (Completed)

- **LLM API Integration**: OpenAI and Anthropic are integrated through modular provider code.
- **Multi Model Orchestration**: Same prompt is sent to multiple models in parallel and results are returned together.

### Phase 2 (In Progress)

- **Prompt Engineering**: Add reusable prompt templates, system prompts, prompt versioning, and structured prompt testing.
- Add conversation history support for multi-turn interactions.
- Add provider-specific context and token budgeting by model.

### Phase 3 (Planned)

- **RAG Pipeline**: Add document ingestion, chunking, embeddings, vector search, and context injection before model calls.
- Add streaming responses and observability for latency and token usage metrics.

## How to Run Locally