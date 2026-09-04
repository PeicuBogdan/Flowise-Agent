# Flowise Agent — Industrial Assistant

An AI agent that answers questions about a production line by combining live
machine data with the maintenance manual. Built with Flowise, running locally
against Ollama.

Ask it "station ST-02 is down, what do I do?" and it calls the monitoring API,
gets error code E-233 back, looks that code up in the manual, and answers with
both.

I built this to learn the stack behind agent platforms: tool calling, retrieval,
sandboxing, and how these systems fail. The troubleshooting notes in `docs/` are
the most useful part of the repo.

## What's in here

```
mock-api/       FastAPI service returning station status (the "live data")
docs/           Maintenance manual used for retrieval, plus troubleshooting notes
flows/          Exported Flowise agentflow and custom tool
tests/          Golden prompt suite
docker-compose.yml
```

## Architecture

```
                    ┌─────────────┐
   question ──────► │  Flowise    │
                    │  Agent      │
                    └──┬───────┬──┘
                       │       │
         tool call ────┘       └──── retrieval
              │                          │
     ┌────────▼────────┐        ┌────────▼────────┐
     │  mock-api       │        │  Faiss          │
     │  station status │        │  manual chunks  │
     └─────────────────┘        └─────────────────┘

   chat + embeddings: Ollama on the host
```

The agent decides on its own whether it needs the API, the manual, both, or
neither. Nothing is hardcoded into the flow.

## Running it

Needs Docker and Ollama.

```bash
ollama pull qwen2.5:7b
ollama pull nomic-embed-text
```

Turn on "Expose Ollama to the network" in Ollama's settings, otherwise it only
listens on loopback and the container can't reach it.

```bash
docker compose up -d
```

Flowise comes up on http://localhost:3100. Import the flow from `flows/`, then
create a Document Store from `docs/station-maintenance-manual.md`. Splitter set
to recursive, chunk size 1000, overlap 150, Ollama embeddings pointed at
`http://host.docker.internal:11434`, Faiss as the store.

Ollama stays on the host rather than in a container so it keeps GPU access.
Everything else talks over the compose network.

## Tests

Five golden prompts covering the two data sources, a healthy station, an unknown
station, and a question the manual doesn't answer.

```bash
cd tests
python -m pip install -r requirements.txt
export FLOW_ID=<agentflow id from the canvas url>
export FLOWISE_API_KEY=<key>
pytest -v
```

You can't assert on exact output here, since the same prompt gives different
wording every time. The tests check properties instead: does the real error code
appear, is a healthy station left alone, does the agent admit when something
isn't covered.

The assertions are looser than I'd like. `test_manual_lookup_bit_replacement`
only looks for "50" in the answer, which would also pass if the model got there
by accident. Tightening them means matching on the manual's actual vocabulary
(feeder, bit, thread, calibration) rather than a number.

## Known limitation

qwen2.5:7b at 4-bit has weak context adherence. Retrieval returns the right
chunks — I checked them against the query directly in the Document Store — but
the model often reads the section heading and then answers from its own general
knowledge of industrial equipment instead of the manual's actual steps. On E-233
it invented sensor faults and cabling issues; the manual says feeder jam, worn
bit, cross-threaded insert, torque drift.

This is the model, not the architecture. Swapping the chat model node for a
hosted API fixes it without touching anything else.

## Security notes

The test API key is scoped to `agentflows:view` and `executions:view`. It can't
touch credentials, tools or document stores.

SSRF protection is disabled locally (`HTTP_SECURITY_CHECK=false`) so the tool can
reach the API, with the cloud metadata endpoint still denied explicitly. See
`docs/troubleshooting.md` for why `HTTP_DENY_LIST` alone doesn't do the job. On a
real deployment the check stays on.

Custom tool code runs in a vm2 sandbox with imports restricted by default. axios
is allowlisted through `TOOL_FUNCTION_EXTERNAL_DEP`.
