from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, time, timedelta


PRIORITY_SCORES = {
    "high": 3,
    "medium": 2,
    "low": 1,
}


@dataclass
class Owner:
    name: str
    available_minutes: int
    day_start: time = time(hour=8, minute=0)
    prefer_shorter_tasks_when_tied: bool = True

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Owner name is required.")
        if self.available_minutes <= 0:
            raise ValueError("Available minutes must be greater than zero.")


@dataclass
class Pet:
    name: str
    species: str

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Pet name is required.")
        if not self.species.strip():
            raise ValueError("Species is required.")


@dataclass
class CareTask:
    title: str
    duration_minutes: int
    priority: str
    notes: str = ""

    def __post_init__(self) -> None:
        self.priority = self.priority.lower().strip()

        if not self.title.strip():
            raise ValueError("Task title is required.")
        if self.duration_minutes <= 0:
            raise ValueError("Task duration must be greater than zero.")
        if self.priority not in PRIORITY_SCORES:
            allowed = ", ".join(PRIORITY_SCORES)
            raise ValueError(f"Priority must be one of: {allowed}.")

    @property
    def priority_score(self) -> int:
        return PRIORITY_SCORES[self.priority]


@dataclass
class ScheduledItem:
    task: CareTask
    start: datetime
    end: datetime
    reason: str

    @property
    def time_range(self) -> str:
        return f"{self.start:%H:%M} - {self.end:%H:%M}"


@dataclass
class SkippedTask:
    task: CareTask
    reason: str


@dataclass
class DailyPlan:
    owner: Owner
    pet: Pet
    scheduled_items: list[ScheduledItem] = field(default_factory=list)
    skipped_tasks: list[SkippedTask] = field(default_factory=list)

    @property
    def total_scheduled_minutes(self) -> int:
        return sum(item.task.duration_minutes for item in self.scheduled_items)

    @property
    def remaining_minutes(self) -> int:
        return self.owner.available_minutes - self.total_scheduled_minutes

    def as_rows(self) -> list[dict[str, str | int]]:
        return [
            {
                "Time": item.time_range,
                "Task": item.task.title,
                "Minutes": item.task.duration_minutes,
                "Priority": item.task.priority,
                "Reason": item.reason,
            }
            for item in self.scheduled_items
        ]


class Scheduler:
    def sort_tasks(self, tasks: list[CareTask], owner: Owner) -> list[CareTask]:
        if owner.prefer_shorter_tasks_when_tied:
            return sorted(tasks, key=lambda task: (-task.priority_score, task.duration_minutes))

        return sorted(tasks, key=lambda task: -task.priority_score)

    def build_daily_plan(self, owner: Owner, pet: Pet, tasks: list[CareTask]) -> DailyPlan:
        plan = DailyPlan(owner=owner, pet=pet)
        current_time = datetime.combine(datetime.today(), owner.day_start)
        remaining_minutes = owner.available_minutes

        for task in self.sort_tasks(tasks, owner):
            if task.duration_minutes <= remaining_minutes:
                start = current_time
                end = start + timedelta(minutes=task.duration_minutes)
                plan.scheduled_items.append(
                    ScheduledItem(
                        task=task,
                        start=start,
                        end=end,
                        reason=self._reason_for_scheduled_task(task),
                    )
                )
                current_time = end
                remaining_minutes -= task.duration_minutes
            else:
                plan.skipped_tasks.append(
                    SkippedTask(
                        task=task,
                        reason=(
                            f"Skipped because it needs {task.duration_minutes} minutes "
                            f"but only {remaining_minutes} minutes were left."
                        ),
                    )
                )

        return plan

    def _reason_for_scheduled_task(self, task: CareTask) -> str:
        if task.priority == "high":
            return "Chosen early because it is high priority."
        if task.priority == "medium":
            return "Chosen after higher-priority care needs."
        return "Included because there was enough time after higher-priority tasks."


def build_tasks_from_rows(rows: list[dict[str, object]]) -> tuple[list[CareTask], list[str]]:
    tasks: list[CareTask] = []
    errors: list[str] = []

    for row_number, row in enumerate(rows, start=1):
        raw_title = row.get("title", "")
        title = "" if raw_title is None else str(raw_title).strip()
        if not title:
            continue

        try:
            duration = int(row.get("duration_minutes", 0))
            raw_priority = row.get("priority", "medium")
            priority = "medium" if raw_priority is None else str(raw_priority)
            raw_notes = row.get("notes", "")
            notes = "" if raw_notes is None else str(raw_notes)
            tasks.append(
                CareTask(
                    title=title,
                    duration_minutes=duration,
                    priority=priority,
                    notes=notes,
                )
            )
        except (TypeError, ValueError) as error:
            errors.append(f"Row {row_number}: {error}")

    return tasks, errors


def sample_tasks() -> list[dict[str, object]]:
    return [
        {
            "title": "Morning walk",
            "duration_minutes": 30,
            "priority": "high",
            "notes": "Energy and bathroom break",
        },
        {
            "title": "Breakfast",
            "duration_minutes": 10,
            "priority": "high",
            "notes": "Food and fresh water",
        },
        {
            "title": "Puzzle toy",
            "duration_minutes": 15,
            "priority": "medium",
            "notes": "Enrichment",
        },
        {
            "title": "Brush coat",
            "duration_minutes": 20,
            "priority": "low",
            "notes": "Grooming if time allows",
        },
    ]
