# AI Interactions Log

## Agent Workflow (SF7)

**What task did you give the agent?**

I asked the AI agent to inspect the PawPal+ project, explain what the starter code was,
and then complete it as a working project while explaining the choices in a way I could
understand and defend.

**What did the agent do?**

The agent first read the project files and identified that the repo was mostly a
Streamlit starter app with placeholder documentation. Then it created a backend module
called `pawpal_system.py` with dataclasses for `Owner`, `Pet`, `CareTask`,
`ScheduledItem`, `SkippedTask`, and `DailyPlan`, plus a `Scheduler` class. The scheduler
sorts tasks by priority, optionally breaks ties by shorter duration, schedules tasks
sequentially from the start time, and skips tasks that do not fit.

The agent also replaced the starter Streamlit UI in `app.py` with a working interface.
The app now accepts owner and pet information, lets the user edit task rows, generates a
schedule, displays metrics, shows the scheduled tasks, and explains skipped tasks. After
that, the agent added pytest tests for the scheduler, updated the Mermaid UML diagram,
filled in the README, and wrote the project reflection in first person.

**What did you have to verify or fix manually?**

The main thing to verify was that the AI-generated logic actually matched the project
requirements. I checked that the app handled owner and pet info, editable tasks, priority,
duration, available time, skipped tasks, and explanations. I also verified the scheduler
with `python -m pytest`, which passed all six tests.

## Prompt Comparison (SF11)

I did not complete a full prompt comparison stretch feature for this project.
