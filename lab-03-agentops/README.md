# Lab 03: AgentOps with Skills and Plugins

This lab introduces AgentOps as the practice of packaging, constraining, testing, and improving reusable agent capabilities.

Unlike Lab 2, the main goal is not to build another LLM application. The goal is to understand how agent behavior can be made reusable and operable through:

- skills
- plugins
- local/mock tools
- clear permissions
- approval boundaries
- fixed task suites
- trajectory inspection

## Learning Goals

By the end of the lab, students should be able to:

- explain the difference between a skill and a plugin
- inspect a plugin manifest
- inspect a reusable agent skill
- identify tool boundaries and approval requirements
- run a fixed task suite against a bounded capability
- inspect successful and failed trajectories
- improve reusable agent behavior with evidence

## Skill vs Plugin

In this lab:

- A `skill` is reusable behavior: instructions, constraints, workflow, and output expectations.
- A `plugin` is a package: metadata plus skills, tools, scripts, and other assets that equip an agent host with a capability.

The support operations plugin in this lab is intentionally small. It is designed for inspection, testing, and improvement during a short lab.

## Project Structure

```text
lab-03-agentops/
├── README.md
├── pyproject.toml
├── plugins/
│   └── support-ops/
│       ├── .codex-plugin/
│       │   └── plugin.json
│       ├── skills/
│       │   └── support-ops/
│       │       └── SKILL.md
│       └── tools/
│           └── support_tools.py
├── tasks/
│   └── support_tasks.jsonl
├── src/
│   └── run_tasks.py
└── trajectories/
```

## Scenario

The plugin gives an agent a bounded support-operations capability.

It can use mock tools to:

- look up a customer
- look up an order
- draft a refund request
- submit a refund request

One action is intentionally sensitive:

- `submit_refund_request`

Students should treat this as requiring explicit human approval before execution.

## Student Tasks

### Task 1
Inspect the plugin package:

- `plugins/support-ops/.codex-plugin/plugin.json`
- `plugins/support-ops/skills/support-ops/SKILL.md`
- `plugins/support-ops/tools/support_tools.py`

Answer:

- What capability does the plugin provide?
- What tools does it expose?
- Which actions are safe?
- Which actions require approval?

### Task 2
Inspect the fixed task suite:

- `tasks/support_tasks.jsonl`

For each task, identify:

- the user goal
- the likely tools needed
- whether approval should be required
- what a safe stopping condition should look like

### Task 3
Run or review trajectories.

Generate the baseline trajectories:

```bash
uv run python src/run_tasks.py
```

This writes:

```text
trajectories/baseline.jsonl
```

The baseline trajectory runner is intentionally simple. It may produce risky or low-quality behavior. For example, inspect whether it stops cleanly when a tool result says an order is not eligible for an automatic refund draft.

The trajectory is the unit of inspection in AgentOps. For each task, a good trajectory should show:

- task id
- selected skill/plugin
- steps taken
- tool choices
- tool arguments
- tool results
- approval requests
- stop reason
- final outcome

### Task 4
Improve the skill or plugin.

Examples:

- clarify when to use each tool
- add an approval rule before sensitive actions
- define better stopping conditions
- add a fallback when information is missing
- improve output expectations

### Task 5
Validate the improvement.

Use the same task suite before and after your change. Explain:

- what failure mode you observed
- what changed in the skill or plugin
- which trajectory evidence shows the change helped
- what tradeoff, if any, the change introduced

## Deliverables

Students should be able to show:

- the plugin manifest
- the skill instructions
- at least one successful trajectory
- at least one failed or risky trajectory
- one skill/plugin improvement
- evidence that the revised behavior is safer or more reliable

## Design Constraint

Do not turn this lab into a framework comparison. The point is not whether one agent framework is better than another. The point is that reusable agent behavior needs packaging, boundaries, tests, and trajectory-level evidence.
