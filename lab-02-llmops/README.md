# Lab 02: LLMOps Foundations with Langfuse

This lab introduces operational practices for LLM-powered systems:

- trace-first debugging
- prompt and configuration comparison
- small eval sets
- latency, token, and cost visibility
- evidence-based iteration

The lab uses a public customer-support dataset from Bitext as the source for support-triage examples.

## Learning Goals

By the end of the lab, students should be able to:

- run a baseline LLM application
- explain what an application trace captures
- instrument an LLM workflow with `Langfuse`
- run a small eval set
- compare prompt or model variants
- identify one concrete failure mode
- verify whether a change improved behavior

## Project Structure

```text
lab-02-llmops/
├── README.md
├── pyproject.toml
├── scripts/
│   └── prepare_data.py
└── src/
    ├── app.py
    ├── data.py
    ├── eval.py
    ├── prompts.py
    └── triage.py
```

## Dataset

Dataset source:

- `bitext/Bitext-customer-support-llm-chatbot-training-dataset`
- URL: https://huggingface.co/datasets/bitext/Bitext-customer-support-llm-chatbot-training-dataset
- License: `cdla-sharing-1.0`

The full dataset is small enough to download during setup. It contains customer-support instructions with labels such as `category` and `intent`, plus an example support response.

This lab prepares two local JSONL files:

```text
data/
├── support_tickets.jsonl
└── eval_set.jsonl
```

These files are generated locally and are not committed to Git.

## Setup

Install dependencies:

```bash
uv sync
```

This creates a local `.venv` and installs the dependencies listed in `pyproject.toml`, including:

- `openai`
- `langfuse`
- `python-dotenv`

Check the OpenAI SDK is available:

```bash
uv run python -c "import openai; print(openai.__version__)"
```

## Prepare The Data

From this lab directory:

```bash
uv run python scripts/prepare_data.py
```

This downloads the Bitext CSV from Hugging Face and creates:

- `data/support_tickets.jsonl`: a deterministic sample for app development
- `data/eval_set.jsonl`: a smaller deterministic eval set
- `data/raw/Bitext_Sample_Customer_Support_Training_Dataset_27K_responses-v11.csv`: the downloaded source CSV

You can change the sample sizes:

```bash
uv run python scripts/prepare_data.py --support-size 60 --eval-size 20
```

## Configure API Keys

Copy the example environment file:

```bash
cp .env.example .env
```

Then edit `.env` and fill in:

- `OPENAI_API_KEY`
- `LANGFUSE_PUBLIC_KEY`
- `LANGFUSE_SECRET_KEY`
- `LANGFUSE_BASE_URL`
- `GROUP_ID`

Use a stable `GROUP_ID`, such as `group-03`, so traces can be filtered in Langfuse.

The `.env` file contains secrets and is ignored by Git.

The default model in `.env.example` is `gpt-4o-mini` because it is low cost and works well for structured triage tasks. If your OpenAI organization is verified and has access to GPT-5 models, you can try `gpt-5-mini` or `gpt-5-nano` as model variants.

## Run The Baseline App

First check the app without spending API tokens:

```bash
uv run python src/app.py --ticket-id support-001 --mock
```

Then run the real model call:

```bash
uv run python src/app.py --ticket-id support-001
```

The app prints a structured support-triage result with:

- predicted `category`
- predicted `intent`
- `priority`
- `draft_response`
- short `rationale`

At this point, the app works but is operationally blind. It does not yet send traces to Langfuse.

## Run The Eval Set

Check the eval workflow without spending API tokens:

```bash
uv run python src/eval.py --mock
```

Run a small real eval:

```bash
uv run python src/eval.py --limit 5
```

The eval runner writes per-example outputs to:

```text
outputs/eval_results.jsonl
```

It reports:

- category accuracy
- intent accuracy
- valid priority rate
- elapsed time

## Student Tasks

Students will build on this data to:

### Task 1
Run the baseline support-triage system and inspect its outputs.

Use both:

```bash
uv run python src/app.py --ticket-id support-001
uv run python src/eval.py --limit 5
```

### Task 2
Instrument the app with `Langfuse`.

Capture:

- `GROUP_ID`
- ticket id
- prompt version
- model
- input message
- structured output
- expected category and intent
- latency
- token usage and cost, if available
- eval metadata

Suggested files to inspect:

- `src/app.py`
- `src/eval.py`
- `src/triage.py`

### Task 3
Run the eval set and inspect traces in Langfuse.

Look for:

- wrong category
- wrong intent
- invalid or unhelpful priority
- overlong response
- hallucinated policy or account details
- unnecessary latency or token usage

### Task 4
Create and compare one variant.

Examples:

- improve the system prompt in `src/prompts.py`
- change the model from `OPENAI_MODEL` to `OPENAI_FALLBACK_MODEL`
- add stricter response guidance
- add a small validation or retry rule

### Task 5
Document one improvement.

Explain:

- what failure mode you observed
- what you changed
- what evidence suggests the change helped
- what tradeoff, if any, the change introduced

## Deliverables

Students should be able to show:

- a baseline support-triage run
- a Langfuse trace for at least one single-ticket run
- Langfuse traces or scores for a small eval run
- a comparison between two variants
- one documented improvement supported by evidence

The main learning objective is trace-first debugging and evidence-based iteration. The system may include light agentic behavior, but this lab should not become a full agent-framework exercise.

## Stretch Goals

If students complete the core tasks quickly, they can extend the lab with one or more of these challenges:

- compare answers with and without retrieved context, then decide whether failures come from retrieval quality, prompt design, or model behavior
- require structured JSON output, log validation failures in Langfuse, and add a simple repair or retry step
- compare `gpt-5-mini` and `gpt-5-nano` on the same eval set for quality, latency, and cost
- add a simple router that sends easy cases to a cheaper model and harder cases to a stronger model
- track cost per successful answer, not just total cost
- label failures by type, such as retrieval, prompt ambiguity, hallucination, formatting, latency, or cost
- add edge-case evals for ambiguous requests, missing information, conflicting context, malformed inputs, or unsupported requests
- improve refusal or uncertainty behavior when the answer is not supported by the provided context
- rerun the original eval set after each improvement to check for regressions
- write a short ops memo summarizing what changed, what evidence improved, what risk remains, and what should be monitored next
