# AGENTS.md

## Repository Purpose

This repository contains the practical lab sessions for the 2026 PDPSL course, which has been reframed from a mostly MLOps course into a progression across:

- `MLOps`: operating trained ML systems
- `LLMOps`: operating LLM-powered applications
- `AgentOps`: operating bounded, tool-using, multi-step AI systems

The revised course source of truth is the markdown course pack at:

- `/Users/phillipmortimer/projects/mlops2026/2026/revised-course`

The 2026 slide decks are useful supporting context, but the markdown is cleaner and should drive lab design.

## Course Spine

Use this through-line when designing or extending labs:

```text
training run -> application trace -> agent trajectory
```

The operational mindset is consistent across the course, but the unit of management changes:

- Block 1 manages `training runs`, model artifacts, metrics, and registry entries.
- Block 2 manages `traces`, prompt/config versions, model calls, evals, latency, tokens, and cost.
- Block 3 manages `trajectories`, tool calls, state, stopping rules, approvals, and bounded autonomy.

## Intended Lab Structure

Expected repository shape:

```text
labs/
├── lab-01-mlops/
├── lab-02-llmops/
└── lab-03-agentops/
```

## Lab 01: MLOps

Current scaffold:

- `/Users/phillipmortimer/projects/mlops2026/labs/lab-01-mlops`

Course intent:

- Add MLflow tracking and registry support to a simple training workflow.
- Students start with code that already trains successfully without tracking.
- Students add experiment tracking, log parameters/metrics/artifacts, run variants, compare runs, register the best model, and keep a minimal prediction path working.

Teaching emphasis:

- What exactly is being tracked?
- How would another person reproduce the selected run?
- Why is the selected model better?
- What is the operational difference between a run and a registered model?

The existing scikit-learn digits scaffold is aligned with this direction.

## Lab 02: LLMOps

Course intent:

- Instrument and improve a small LLM application with Langfuse.
- Suggested scenarios: document Q&A, support triage, or structured extraction.
- Baseline should produce outputs but lack proper observability and evals.

Students should:

- run the baseline app with `GPT-5 mini`
- instrument it with `Langfuse`
- inspect traces for prompt, latency, token, cost, and output behavior
- create a small eval set
- compare at least two prompt or model variants
- identify one failure mode
- improve the system once and verify the improvement

Cost controls:

- keep eval sets around `10-20` examples
- use short prompts and short outputs
- avoid unnecessary retries
- use `GPT-5 nano` for simple or retry-heavy cases

Teaching emphasis:

- What does the trace reveal that output inspection alone does not?
- What failure mode was observed?
- What changed in the prompt, context, or model choice?
- What evidence suggests the change is better rather than merely different?

## Lab 03: AgentOps

Course intent:

- Build and debug a bounded agent with Langfuse tracing.
- Use local or mock tools only.
- Suggested scenarios: local document research, support assistant with mock lookup/update tools, or structured operations assistant with approval checkpoints.

Students should:

- run the provided bounded agent scaffold
- inspect tool interfaces and stopping rules
- trace behavior in `Langfuse`
- test against a small fixed task suite
- identify one concrete failure mode
- improve tool descriptions, prompts, stopping logic, or guardrails
- validate the improvement on the same task suite

Cost controls:

- avoid open web search
- cap allowed reasoning/tool steps
- keep task suites small and fixed
- default to `GPT-5 mini`
- use `GPT-5 nano` for simple variants or repeated retries

Teaching emphasis:

- Why is this an agent rather than just a workflow?
- What exactly went wrong in the failing trajectory?
- Was the issue caused by tool design, prompt design, or missing control logic?
- How do we know the revised system is better behaved?

## Tooling Choices

- Block 1 should use local `MLflow`.
- Blocks 2 and 3 should use `Langfuse`.
- Use `uv` for Python environment management when consistent with the existing lab.
- Keep generated outputs out of Git: `.venv`, `.cache`, `artifacts`, and `mlruns` should remain ignored.

## Design Principles

- Labs should be bounded, cheap, and teachable.
- Prefer fixed datasets, fixed eval sets, and mock/local tools over open-ended exploration.
- Students may use AI coding assistants, but grading should reward operational understanding, empirical validation, and interpretation of traces/evals/failures.
- Do not turn Block 3 into a framework comparison or speculative autonomy lecture. Keep it practical: tools, state, guardrails, trajectories, cost, and evaluation.

## GitHub Remote

Remote repository:

- `git@github.com:phillipmortimer/mlops2026-labs.git`
- Public URL: `https://github.com/phillipmortimer/mlops2026-labs`

