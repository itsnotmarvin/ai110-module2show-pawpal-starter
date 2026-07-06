from datetime import time

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, build_tasks_from_rows, sample_tasks


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

if "task_rows" not in st.session_state:
    st.session_state.task_rows = sample_tasks()

st.title("🐾 PawPal+")
st.caption("Daily pet-care planning based on priority, duration, and available time.")

with st.container(border=True):
    st.subheader("Owner and Pet")
    owner_col, pet_col = st.columns(2)

    with owner_col:
        owner_name = st.text_input("Owner name", value="Jordan")
        available_minutes = st.number_input(
            "Available care time today",
            min_value=15,
            max_value=720,
            value=75,
            step=15,
            help="Minutes available for pet-care tasks today.",
        )
        day_start = st.time_input("Start time", value=time(hour=8, minute=0))
        prefer_shorter_tasks = st.toggle(
            "Fit shorter tied-priority tasks first",
            value=True,
            help="When two tasks have the same priority, schedule the shorter one first.",
        )

    with pet_col:
        pet_name = st.text_input("Pet name", value="Mochi")
        species = st.selectbox("Species", ["dog", "cat", "rabbit", "bird", "other"])

st.subheader("Care Tasks")
edited_rows = st.data_editor(
    st.session_state.task_rows,
    num_rows="dynamic",
    hide_index=True,
    use_container_width=True,
    column_config={
        "title": st.column_config.TextColumn("Task", required=True),
        "duration_minutes": st.column_config.NumberColumn(
            "Minutes",
            min_value=1,
            max_value=240,
            step=5,
            required=True,
        ),
        "priority": st.column_config.SelectboxColumn(
            "Priority",
            options=["high", "medium", "low"],
            required=True,
        ),
        "notes": st.column_config.TextColumn("Notes"),
    },
    key="task_editor",
)
st.session_state.task_rows = edited_rows

button_col, reset_col = st.columns([1, 1])
with button_col:
    generate_clicked = st.button("Generate schedule", type="primary", use_container_width=True)
with reset_col:
    if st.button("Reset sample tasks", use_container_width=True):
        st.session_state.task_rows = sample_tasks()
        st.rerun()

if generate_clicked:
    tasks, task_errors = build_tasks_from_rows(edited_rows)

    if task_errors:
        for error in task_errors:
            st.error(error)
    elif not tasks:
        st.warning("Add at least one care task before building the schedule.")
    else:
        try:
            owner = Owner(
                name=owner_name,
                available_minutes=int(available_minutes),
                day_start=day_start,
                prefer_shorter_tasks_when_tied=prefer_shorter_tasks,
            )
            pet = Pet(name=pet_name, species=species)
            plan = Scheduler().build_daily_plan(owner=owner, pet=pet, tasks=tasks)
        except ValueError as error:
            st.error(str(error))
        else:
            st.divider()
            st.subheader(f"Daily Plan for {plan.pet.name}")

            metric_col1, metric_col2, metric_col3 = st.columns(3)
            metric_col1.metric("Scheduled", f"{len(plan.scheduled_items)} tasks")
            metric_col2.metric("Care time", f"{plan.total_scheduled_minutes} min")
            metric_col3.metric("Time left", f"{plan.remaining_minutes} min")

            if plan.scheduled_items:
                st.table(plan.as_rows())
            else:
                st.info("No tasks fit into the available care time.")

            if plan.skipped_tasks:
                st.markdown("#### Skipped Tasks")
                for skipped in plan.skipped_tasks:
                    st.write(
                        f"- **{skipped.task.title}** "
                        f"({skipped.task.duration_minutes} min, {skipped.task.priority}): "
                        f"{skipped.reason}"
                    )

            st.markdown("#### Scheduling Logic")
            st.write(
                "PawPal+ sorts tasks by priority first. If two tasks have the same priority, "
                "it can place shorter tasks first so more care fits into the available time. "
                "Tasks are then scheduled one after another starting at the selected start time."
            )
