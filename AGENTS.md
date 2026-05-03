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
training run -> application trace -> reusable agent capability
```

The operational mindset is consistent across the course, but the unit of management changes:

- Block 1 manages `training runs`, model artifacts, metrics, and registry entries.
- Block 2 manages `traces`, prompt/config versions, model calls, evals, latency, tokens, and cost.
- Block 3 manages reusable agent capabilities: `skills`, `plugins`, tool boundaries, operating instructions, tests, and observed trajectories.

There will be some conceptual overlap between Labs 2 and 3. That is intentional. Most practical LLM applications now include agentic elements such as retrieval, tool calls, routing, validation, retries, or structured workflows. Do not force a false separation between "LLM applications" and "agents." Instead, separate the labs by what students are learning to operate:

- Lab 2 teaches students to observe and improve an LLM system through traces and evals.
- Lab 3 teaches students to package, constrain, version, and test reusable agent behavior through skills/plugins.

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

- Instrument and improve a small LLM system with Langfuse.
- Suggested scenarios: document Q&A, support triage, or structured extraction.
- The system may include light agentic behavior such as retrieval, tool calls, validation, routing, or retries.
- Baseline should produce outputs but lack proper observability and evals.
- The main learning objective is trace-first debugging and evidence-based iteration, not building an agent framework.

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
- What changed in the prompt, context, model choice, retrieval, validation, or tool behavior?
- What evidence suggests the change is better rather than merely different?

## Lab 03: AgentOps

Course intent:

- Build, test, and package a bounded reusable agent capability.
- Prefer creating or improving `skills` and `plugins` over asking students to write a full agentic application loop from scratch.
- Use local or mock tools only.
- Suggested scenarios: local document research skill, support operations plugin with mock lookup/update tools, or structured operations skill with approval checkpoints.
- The capability should be small enough to inspect, version, test, and improve during the lab.

Students should:

- run a provided agent host or CLI scaffold that can load the skill/plugin
- inspect the skill/plugin instructions, tool interfaces, permissions, and stopping rules
- trace behavior or review captured trajectories in `Langfuse`
- test against a small fixed task suite
- identify one concrete failure mode
- improve the skill/plugin by refining instructions, tool descriptions, prompts, stopping logic, approval checkpoints, or guardrails
- validate the improvement on the same task suite

Expected deliverables:

- a skill or plugin package with clear operating instructions
- one to three local/mock tools exposed to the agent capability
- a small fixed task suite
- traces or trajectory records showing successful and failed behavior
- one documented reliability improvement based on observed evidence

Cost controls:

- avoid open web search
- cap allowed reasoning/tool steps
- keep task suites small and fixed
- default to `GPT-5 mini`
- use `GPT-5 nano` for simple variants or repeated retries

Teaching emphasis:

- What capability is being packaged for reuse?
- What boundaries make the capability safe and testable?
- What exactly went wrong in the failing trajectory?
- Was the issue caused by skill instructions, tool design, prompt design, missing control logic, or missing approval boundaries?
- How do we know the revised system is better behaved?

## Tooling Choices

- Block 1 should use local `MLflow`.
- Blocks 2 and 3 should use `Langfuse`.
- Block 3 may use a local agent host or CLI-style scaffold for loading skills/plugins. Keep the host simple; the lab focus is the reusable capability, not framework mechanics.
- Use `uv` for Python environment management when consistent with the existing lab.
- Keep generated outputs out of Git: `.venv`, `.cache`, `artifacts`, and `mlruns` should remain ignored.

## Design Principles

- Labs should be bounded, cheap, and teachable.
- Prefer fixed datasets, fixed eval sets, and mock/local tools over open-ended exploration.
- Students may use AI coding assistants, but grading should reward operational understanding, empirical validation, and interpretation of traces/evals/failures.
- Do not turn Block 3 into a framework comparison or speculative autonomy lecture. Keep it practical: skills, plugins, tools, permissions, guardrails, trajectories, cost, and evaluation.
- Avoid making Lab 3 feel like a repeat of Lab 2. Lab 2 is about observing and improving system behavior. Lab 3 is about packaging bounded behavior so an agent can reuse it safely.

## GitHub Remote

Remote repository:

- `git@github.com:phillipmortimer/mlops2026-labs.git`
- Public URL: `https://github.com/phillipmortimer/mlops2026-labs`
