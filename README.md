# LangGraph + Ollama — Basic Agent

A small LangGraph project built with a local Ollama model.

This is project-based LangGraph learning series. The goal is to understand how LangGraph moves state through nodes, follows edges, makes routing decisions, and handles a retry loop.

## Architecture

```text
                    START
                      │
                      ▼
                     LLM
                      │
                      ▼
                   SECOND
                      │
                      ▼
                   ROUTER
                  /      \
             retry        done
               │            │
               ▼            ▼
             RETRY         END
               │
               ▼
              LLM
```

The graph can loop back to the LLM when the router chooses `retry`.

## What We Built

* Local LLM inference with Ollama
* LangGraph `StateGraph`
* Graph state using `TypedDict`
* Multiple graph nodes
* Normal edges
* Conditional edges
* Runtime routing
* A retry loop
* State updates between nodes

## Core Concepts

### State

The state is the information carried through the graph.

```python
class AgentState(TypedDict):
    message: str
    response: str
    status: str
    retry_count: int
```

### Nodes

Nodes perform work.

```text
LLM    → call_model()
SECOND → second_node()
RETRY  → retry_node()
```

### Edges

Edges determine where execution goes next.

```text
START → LLM
LLM   → SECOND
RETRY → LLM
```

### Conditional Routing

The router determines whether the workflow should retry or finish.

```text
SECOND
   │
   ▼
ROUTER
 /    \
retry  done
 ↓      ↓
RETRY  END
```

## Run Locally

Make sure Ollama is running and that the model configured in `agent.py` is available locally.

Check installed models:

```bash
ollama list
```

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python agent.py
```

## Important Observation

The retry logic in this first project is intentionally simple.

The router currently uses `retry_count` rather than determining whether the LLM response is actually valid.

So this project demonstrates the **LangGraph mechanism**, not a production-quality validation system.

A later project will replace this artificial retry condition with real validation and recovery logic.

## Project Goal

The purpose of this project is not to build a sophisticated agent.

It is to understand the basic execution model:

```text
State
  ↓
Node
  ↓
State Update
  ↓
Edge
  ↓
Next Node
```

This foundation will be used for the later production-style projects in this learning series.
