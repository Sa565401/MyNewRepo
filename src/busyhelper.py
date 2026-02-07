"""BusyHelper AI assistant core primitives."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Iterable


@dataclass
class Task:
    """Represents a single user task."""

    title: str
    notes: str | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: datetime | None = None

    @property
    def is_complete(self) -> bool:
        return self.completed_at is not None

    def complete(self, when: datetime | None = None) -> None:
        """Mark the task complete."""

        self.completed_at = when or datetime.utcnow()


@dataclass
class BusyHelper:
    """Lightweight task assistant for busy users."""

    owner: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, title: str, notes: str | None = None) -> Task:
        """Add a new task for the owner."""

        task = Task(title=title, notes=notes)
        self.tasks.append(task)
        return task

    def complete_task(self, title: str) -> Task:
        """Complete the first task that matches the provided title."""

        task = self._find_task(title)
        if task is None:
            raise ValueError(f"No task found with title '{title}'.")
        task.complete()
        return task

    def pending_tasks(self) -> list[Task]:
        """Return all tasks that are not completed."""

        return [task for task in self.tasks if not task.is_complete]

    def completed_tasks(self) -> list[Task]:
        """Return all tasks that are completed."""

        return [task for task in self.tasks if task.is_complete]

    def summary(self) -> str:
        """Create a summary of pending and completed tasks."""

        pending = self.pending_tasks()
        completed = self.completed_tasks()
        lines = [f"BusyHelper summary for {self.owner}:"]
        lines.append(f"- Pending tasks: {len(pending)}")
        lines.append(f"- Completed tasks: {len(completed)}")
        if pending:
            lines.append("Pending task list:")
            lines.extend(self._format_tasks(pending))
        if completed:
            lines.append("Completed task list:")
            lines.extend(self._format_tasks(completed))
        return "\n".join(lines)

    def _find_task(self, title: str) -> Task | None:
        for task in self.tasks:
            if task.title == title:
                return task
        return None

    @staticmethod
    def _format_tasks(tasks: Iterable[Task]) -> list[str]:
        return [f"  - {task.title}" for task in tasks]
