# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a TCC (Trabalho de Conclusão de Curso) project implementing a RAG system for querying CBMGO (Corpo de Bombeiros Militar do Estado de Goiás) technical norms. The application is a Streamlit-based chatbot that helps users consult fire safety technical standards using LLM technology.

## Architecture

**RAG System Components:**
- **Document Corpus**: 44 CBMGO technical norms in `parsed_docs/` (NT-01 through NT-44 in Markdown format)
- **Prompt Loading**: `src/prompt_loader.py` aggregates all documents into single context string for LLM
- **Chat Interface**: `src/app.py` provides Streamlit UI with streaming responses
- **LLM Integration**: `src/chat.py` handles OpenAI SDK with custom base URL support and Langfuse monitoring

**Data Flow**: User question → Document aggregation → LLM query with full context → Streaming response

## Development Commands

```bash
# Install dependencies
uv sync

# Run application locally
uv run streamlit run src/app.py
```

## Key Technologies

- **Python 3.12+** with uv package manager
- **Streamlit** for web interface
- **OpenAI SDK** with custom endpoint support
- **Langfuse** for LLM observability
- **Google GenAI** as alternative LLM provider

## Environment Configuration

Required environment variables:
- `LLM_API_KEY` - API key for LLM service
- `LLM_BASE_URL` - Custom LLM endpoint URL
- `LANGFUSE_SECRET_KEY`, `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_HOST` - Monitoring setup

## Deployment

- **Production**: Fly.io with automated GitHub Actions deployment
- **Docker**: Multi-stage build optimized for production
- **CI/CD**: `.github/workflows/fly-deploy.yml` handles automatic deployment

## Project Structure Notes

- All technical norms are pre-processed and stored in `parsed_docs/`
- Tests are located in `src/tests/`
- Portuguese documentation in root directory (Plano.md, Tarefas.md, Críticas.md)
- Academic project comparing document fragmentation and LLM performance strategies