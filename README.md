# PawPal+ (Module 2 Project)

PawPal+ is a Streamlit app that helps a pet owner build a daily care plan for a pet.
The user enters owner details, pet details, available care time, and a list of care
tasks. The app then schedules the tasks based on priority, duration, and the amount
of time available.

## Scenario

A busy pet owner needs help staying consistent with pet care. PawPal+ helps with:

- Tracking pet care tasks such as walks, feeding, medication, enrichment, and grooming
- Considering constraints such as available time, priority, and owner preferences
- Producing a daily plan with short explanations for each scheduled or skipped task

## Project Structure

- `app.py` - Streamlit user interface
- `pawpal_system.py` - domain classes and scheduling logic
- `tests/test_scheduler.py` - pytest tests for the scheduler
- `diagrams/uml.mmd` - Mermaid UML class diagram
- `reflection.md` - project reflection
- `ai_interactions.md` - optional AI workflow notes

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run the App

```bash
streamlit run app.py
```

## Sample Output

Example schedule for a pet named Mochi with 75 available minutes:

```text
Daily Plan for Mochi

08:00 - 08:10  Breakfast       10 min  high    Chosen early because it is high priority.
08:10 - 08:40  Morning walk    30 min  high    Chosen early because it is high priority.
08:40 - 08:55  Puzzle toy      15 min  medium  Chosen after higher-priority care needs.
08:55 - 09:15  Brush coat      20 min  low     Included because there was enough time after higher-priority tasks.

Scheduled: 4 tasks
Care time: 75 min
Time left: 0 min
```

If a task does not fit, PawPal+ records it as skipped and explains why:

```text
Grooming was skipped because it needs 25 minutes but only 0 minutes were left.
```

## Testing PawPal+

Run the full test suite:

```bash
python -m pytest
```

Latest test output:

```text
collected 6 items

tests/test_scheduler.py ......                                           [100%]

6 passed in 0.01s
```

## Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_tasks` | Sorts by priority first: high, medium, low. |
| Tie-breaking | `Scheduler.sort_tasks` | If enabled, shorter tasks with the same priority are scheduled first. |
| Filtering | `Scheduler.build_daily_plan` | Skips tasks that do not fit in the remaining available time. |
| Conflict handling | `Scheduler.build_daily_plan` | Tasks are scheduled sequentially, so generated plan items do not overlap. |
| Explanation | `Scheduler._reason_for_scheduled_task` | Adds a reason for scheduled tasks and skipped tasks. |
| UI editing | `st.data_editor` in `app.py` | The user can add, remove, or edit task rows before scheduling. |

## Demo Walkthrough

1. Open the app with `streamlit run app.py`.
2. Enter the owner name, available care time, and start time.
3. Enter the pet name and species.
4. Add or edit care tasks in the task table.
5. Click `Generate schedule`.
6. Review the generated daily plan, total scheduled care time, remaining time, and skipped task explanations.
