# AGENTS.md

This file defines the working rules for agents modifying this repository.

## Core rules

- Type hints are required for new and modified Python code.
- Business logic must not be placed in FastAPI routers. Routers should be limited to HTTP concerns such as request parsing, dependency injection, response construction, and status-code mapping.
- New functionality must include tests. Bug fixes should include a regression test when practical.
- Prefer simple architecture over unnecessary abstraction. Add a new layer only when it has a clear responsibility and immediate value.

## Learning policy

The repository owner is learning software engineering. Before making a large architectural change, explain:

- the problem the change solves;
- the proposed structure;
- why the change is preferable to a smaller alternative;
- the main trade-offs.

Wait for the owner's agreement before implementing a large architectural change. For small, local changes, keep explanations concise and proceed normally.

## Learning-first collaboration

The repository owner is using this project to learn programming and software engineering. Optimize not only for task completion, but also for the owner's understanding.

### Working modes

Infer the working mode from the owner's request:

- If the owner asks for an explanation, review, diagnosis, plan, or procedure, do not modify files unless explicitly asked.
- If the owner asks to implement or fix something, perform the work, but explain important decisions and verification results.
- If the owner asks to learn or practice, prefer hints and incremental guidance before providing a complete solution.

When the intended mode is unclear, prefer a brief explanation followed by a proposed next step.

### Before implementation

For non-trivial changes, briefly explain:

- what is currently happening;
- what will change;
- which files or responsibilities are involved;
- what the owner should pay attention to while reviewing the change.

Do not require approval for ordinary local changes. Approval is required only for large architectural changes or decisions with meaningful trade-offs.

### After implementation

Explain:

- the root cause or requirement addressed;
- the important implementation decisions;
- how the tests demonstrate correctness;
- one or two concepts the owner can learn from the change;
- any remaining limitations or reasonable next steps.

Avoid explaining every line of straightforward code.

### Decision-making

When there are multiple reasonable implementations:

- present the main alternatives briefly;
- state which option is recommended and why;
- mention the most important trade-off;
- prefer the simplest option that satisfies the current requirement.

Do not introduce a dependency without explaining what problem it solves and whether the same result could reasonably be achieved without it.

### Debugging

When diagnosing a problem:

- distinguish observed facts from hypotheses;
- show the evidence used to identify the cause;
- explain why the selected fix addresses that cause;
- avoid unrelated changes while debugging.

### Testing for learning

Before implementing non-trivial functionality, state the behaviors that should be tested.

Tests should emphasize observable behavior rather than implementation details. Explain what failure each important test is intended to catch.

### Reviews

When reviewing the owner's code:

- identify what is already working;
- prioritize issues by impact;
- explain the reason behind each important recommendation;
- avoid rewriting the code unless requested;
- include a small, actionable next step.

## Implementation guidance

- Keep functions small and give them names that describe their intent.
- Follow the existing project structure unless the task justifies changing it.
- Put reusable business logic in a focused module outside `app/routers/`; avoid introducing frameworks or broad service layers for a single simple operation.
- Validate input at system boundaries. File uploads must validate file type and size, use safe generated filenames, and avoid trusting user-provided paths.
- Do not commit secrets, credentials, `.env`, virtual environments, generated build output, or uploaded user files.
- Do not change unrelated code or overwrite existing uncommitted work.

## Verification

- Run the smallest relevant tests during development, then run the affected test suite before finishing.
- For backend changes, at minimum verify that `app.main` imports successfully and that modified Python files compile.
- For frontend changes, run the relevant checks and `npm run build` when the change can affect the production bundle.
- If a check cannot be run, state what was not verified and why.

## Documentation

- Update setup instructions when dependencies, environment variables, database initialization, or run commands change.
- Comments should explain non-obvious decisions, not restate the code.
