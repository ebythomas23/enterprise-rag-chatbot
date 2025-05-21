# Enterprise RAG Chatbot

A local document-based chatbot that uses Retrieval-Augmented Generation (RAG) to answer questions from PDF files. Powered by Ollama, ChromaDB, and Gradio, this project demonstrates how to combine vector search with a local LLM to enable private, context-aware question answering.

---

## Features

- Upload any PDF document
- Automatic text extraction and chunking
- Embedding and vector storage with ChromaDB
- Contextual retrieval based on user questions
- Local LLM-powered answer generation using Ollama
- Clean Gradio interface
- Fully containerized with Docker

---

## Tech Stack

| Component         | Description                             |
|------------------|-----------------------------------------|
| Python           | Core logic and backend pipeline         |
| Gradio           | Interactive user interface              |
| ChromaDB         | Vector store for semantic search        |
| Ollama           | Local LLM runtime (e.g., LLaMA 3)       |
| Docker           | Containerized deployment environment    |

---

## Project Structure


---

## Getting Started

### 1. Install Ollama (once)
Download from [https://ollama.com/download](https://ollama.com/download) and run a model:
```bash
ollama run llama3
```

### 2. Clone and run
```bash
git clone https://github.com/yourusername/enterprise-rag-chatbot.git
cd enterprise-rag-chatbot
```

### 3. Build the Docker container
```bash
ollama run llama3
```

###  Run the app
```bash
docker run -p 7860:7860 \
  -v $(pwd)/docs:/app/docs \
  -e OLLAMA_HOST=http://host.docker.internal:11434 \
  enterprise-rag-chatbot
  ```