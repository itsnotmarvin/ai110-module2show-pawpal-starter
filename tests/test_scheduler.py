from datetime import time

import pytest

from pawpal_system import CareTask, Owner, Pet, Scheduler, build_tasks_from_rows


def make_owner(available_minutes=60, prefer_shorter_tasks_when_tied=True):
    return Owner(
        name="Jordan",
        available_minutes=available_minutes,
        day_start=time(hour=8, minute=0),
        prefer_shorter_tasks_when_tied=prefer_shorter_tasks_when_tied,
    )


def make_pet():
    return Pet(name="Mochi", species="dog")


def test_scheduler_orders_tasks_by_priority_then_shorter_duration():
    tasks = [
        CareTask("Brush coat", 20, "low"),
        CareTask("Long walk", 45, "high"),
        CareTask("Breakfast", 10, "high"),
        CareTask("Puzzle toy", 15, "medium"),
    ]

    plan = Scheduler().build_daily_plan(make_owner(available_minutes=120), make_pet(), tasks)

    titles = [item.task.title for item in plan.scheduled_items]
    assert titles == ["Breakfast", "Long walk", "Puzzle toy", "Brush coat"]


def test_scheduler_skips_tasks_that_do_not_fit_remaining_time():
    tasks = [
        CareTask("Medication", 10, "high"),
        CareTask("Morning walk", 30, "high"),
        CareTask("Grooming", 25, "medium"),
    ]

    plan = Scheduler().build_daily_plan(make_owner(available_minutes=40), make_pet(), tasks)

    assert [item.task.title for item in plan.scheduled_items] == [
        "Medication",
        "Morning walk",
    ]
    assert [skipped.task.title for skipped in plan.skipped_tasks] == ["Grooming"]
    assert "only 0 minutes were left" in plan.skipped_tasks[0].reason


def test_scheduler_assigns_sequential_start_and_end_times():
    tasks = [
        CareTask("Breakfast", 10, "high"),
        CareTask("Walk", 30, "high"),
    ]

    plan = Scheduler().build_daily_plan(make_owner(available_minutes=60), make_pet(), tasks)

    assert plan.scheduled_items[0].time_range == "08:00 - 08:10"
    assert plan.scheduled_items[1].time_range == "08:10 - 08:40"
    assert plan.total_scheduled_minutes == 40
    assert plan.remaining_minutes == 20


def test_task_validation_rejects_unknown_priority():
    with pytest.raises(ValueError, match="Priority must be one of"):
        CareTask("Mystery task", 10, "urgent")


def test_build_tasks_from_rows_returns_errors_without_crashing():
    rows = [
        {"title": "Medication", "duration_minutes": 5, "priority": "high", "notes": ""},
        {"title": "Broken task", "duration_minutes": 0, "priority": "medium", "notes": ""},
    ]

    tasks, errors = build_tasks_from_rows(rows)

    assert [task.title for task in tasks] == ["Medication"]
    assert len(errors) == 1
    assert "Task duration must be greater than zero" in errors[0]


def test_build_tasks_from_rows_ignores_blank_editor_rows():
    rows = [
        {"title": None, "duration_minutes": None, "priority": None, "notes": None},
        {"title": "", "duration_minutes": 10, "priority": "high", "notes": ""},
        {"title": "Breakfast", "duration_minutes": 10, "priority": "high", "notes": None},
    ]

    tasks, errors = build_tasks_from_rows(rows)

    assert errors == []
    assert [task.title for task in tasks] == ["Breakfast"]
    assert tasks[0].notes == ""
