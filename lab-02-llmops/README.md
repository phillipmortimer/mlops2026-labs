# Lab 02: LLMOps Foundations with Langfuse

This lab introduces operational practices for LLM-powered systems:

- trace-first debugging
- prompt and configuration comparison
- small eval sets
- latency, token, and cost visibility
- evidence-based iteration

The lab uses a public customer-support dataset from Bitext as the source for support-triage examples.

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

## Prepare The Data

From this lab directory:

```bash
python3 scripts/prepare_data.py
```

This downloads the Bitext CSV from Hugging Face and creates:

- `data/support_tickets.jsonl`: a deterministic sample for app development
- `data/eval_set.jsonl`: a smaller deterministic eval set
- `data/raw/Bitext_Sample_Customer_Support_Training_Dataset_27K_responses-v11.csv`: the downloaded source CSV

You can change the sample sizes:

```bash
python3 scripts/prepare_data.py --support-size 60 --eval-size 20
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

## Intended Lab Direction

Students will build on this data to:

1. run a baseline support-triage LLM system
2. instrument it with Langfuse
3. inspect traces for prompt, model, latency, tokens, cost, and output behavior
4. run a small eval set
5. compare at least two prompt or model variants
6. identify one failure mode
7. improve the system once and verify the improvement

The main learning objective is trace-first debugging and evidence-based iteration. The system may include light agentic behavior, but this lab should not become a full agent-framework exercise.
