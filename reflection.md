# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

My initial design was centered around the main objects in the scenario: an owner, a pet,
care tasks, and a scheduler. I wanted each class to have one clear responsibility. The
`Owner` class stores the owner's name, available time, start time, and scheduling
preference. The `Pet` class stores the pet's name and species. The `CareTask` class
stores the task title, duration, priority, and notes. The `Scheduler` class is the
"brain" of the app because it decides which tasks fit into the day and what order they
should happen in.

**b. Design changes**

My design changed once I started thinking about how to display results in Streamlit. At
first I only thought about tasks, pets, and the scheduler. During implementation, I added
`ScheduledItem`, `SkippedTask`, and `DailyPlan` classes. These made the result easier to
understand because the app can show not only what was scheduled, but also the time range,
the reason each task was selected, and why any task was skipped.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers available time, task duration, task priority, and one owner
preference. The main rule is that high-priority tasks should be considered before
medium-priority and low-priority tasks. If two tasks have the same priority, the owner can
choose to schedule the shorter task first. I decided that priority mattered most because
pet care tasks like feeding, medication, or walks are usually more important than optional
tasks like extra grooming or enrichment.

**b. Tradeoffs**

One tradeoff is that the scheduler uses a simple greedy approach instead of trying every
possible task combination. It sorts the tasks, then schedules each task if it fits in the
remaining time. This is reasonable for this project because the app is meant to be easy to
understand and explain. A more complex optimizer might fit more total minutes, but it
would also be harder to debug and harder for a user to trust.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI to help turn the starter project into a complete version of the app. The AI
first inspected the existing files and explained that the repo was mostly a scaffold. Then
it helped create the backend classes, connect the scheduler to the Streamlit UI, write the
tests, update the UML diagram, and fill in the project documentation. The most useful
prompt was asking the AI to explain the project back to me first, because that made the
missing pieces clearer before any code was written.

**b. Judgment and verification**

I did not treat the AI output as automatically correct. I checked that the implementation
matched the assignment requirements: user inputs, editable tasks, scheduling by priority
and time, explanations, UML, and tests. I also verified the logic with pytest. The tests
confirmed that tasks are ordered correctly, tasks that do not fit are skipped, start and
end times are sequential, blank editor rows are ignored, and invalid task data is handled
with errors.

---

## 4. Testing and Verification

**a. What you tested**

I tested the most important scheduler behaviors. One test checks that tasks are sorted by
priority and then by shorter duration when priorities match. Another test checks that a
task is skipped if it cannot fit into the remaining available time. I also tested that the
scheduled start and end times are sequential, that invalid priorities are rejected, and
that blank rows from the UI are ignored and bad task rows return useful errors instead of
crashing the app.

**b. Confidence**

I am confident that the scheduler works for the main project requirements. It handles the
core cases of prioritizing care tasks, fitting them into a time limit, and explaining the
plan. If I had more time, I would test more edge cases, such as blank task rows, very long
task lists, multiple pets, recurring tasks, and tasks with specific required time windows.

---

## 5. Reflection

**a. What went well**

The part I am most satisfied with is separating the scheduling logic from the Streamlit
interface. The UI collects inputs and displays results, but the actual decisions happen in
`pawpal_system.py`. That made the code easier to test and easier to explain.

**b. What you would improve**

In another iteration, I would add support for recurring tasks and preferred time windows.
For example, feeding might need to happen around a certain time, while brushing could
happen whenever there is extra time. I would also consider supporting multiple pets in one
plan.

**c. Key takeaway**

My biggest takeaway is that designing the classes first makes the implementation much
clearer. Once I knew what `Owner`, `Pet`, `CareTask`, and `Scheduler` were responsible
for, the Streamlit app became easier to build because it only had to collect inputs and
display the scheduler's result.
