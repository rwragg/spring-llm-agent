# Spring Boot + Python LLM Agent — hybrid project scaffold

A single project that proves **both** sides of Robert's locked positioning in one artifact:
- **Spring Boot** (the hireable, bankable skill — Java/Spring shops)
- **Python + LLM agent** (the differentiator — AI-assisted development)

Architecture: a Spring Boot REST service that calls a Python agent service over HTTP. The
Python side runs a local LLM via [Ollama](https://ollama.com) and returns the result.

```
spring-llm-agent/
├── backend/                 # Spring Boot (Java 17+, Maven)
│   ├── pom.xml
│   └── src/main/java/com/rwragg/agent/
│       ├── AgentApplication.java
│       ├── controller/AgentController.java
│       ├── client/AgentClient.java
│       └── config/AppConfig.java
├── agent/                   # Python LLM agent (FastAPI + Ollama)
│   ├── requirements.txt
│   ├── main.py              # FastAPI app exposing /agent/ask
│   └── agent.py             # Ollama call + prompt logic
├── docker-compose.yml       # optional: run both together
├── .gitignore
└── README.md
```

## Run it

### Python agent (works now — verified)
```bash
cd agent
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# install Ollama first: https://ollama.com  then:
ollama pull llama3.2
python main.py            # stdlib http.server on :8000 (no FastAPI needed)
# test:
curl -X POST localhost:8000/agent/ask -H 'Content-Type: application/json' \
  -d '{"prompt":"Explain Spring Boot in one sentence"}'
```

> Note: the web layer uses Python's stdlib `http.server` (not FastAPI) because
> Python 3.14 lacks a `pydantic-core` wheel. Only `httpx` is required.

### Spring Boot backend (needs JDK 17+ and Maven)
```bash
cd backend
mvn spring-boot:run
# then:
curl -X POST localhost:8080/api/agent/ask -H 'Content-Type: application/json' \
  -d '{"prompt":"What is dependency injection?"}'
```

### Both together (needs Docker)
```bash
docker compose up --build
```

## The point of this project (for the resume)
- Proves hands-on **Spring Boot** development.
- Proves **AI-assisted / agentic** fluency (local LLM, agent pipeline).
- One public GitHub repo closes the "current projects / upskilling" resume gap.