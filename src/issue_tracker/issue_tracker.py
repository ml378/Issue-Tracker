from __future__ import annotations
from datetime import datetime
from collections import OrderedDict
from typing import Any


class Comment:
    """Represents a comment attached to an issue."""

    def __init__(self, author: str, message: str, timestamp: datetime | None = None):
        """Creates an instance of a comment."""
        self.author = author
        self.message = message
        self.timestamp = timestamp or datetime.utcnow()

    def __repr__(self) -> str:
        """Returns a string representing each field of a comment."""
        return (
            f"Comment(author='{self.author}', timestamp='{self.timestamp}', message='{self.message}')"
        )


class Issue:
    """Represents an issue with a title, description, optional labels, and comments."""

    def __init__(self, title: str, description: str, labels: list[str] | None = None):
        """Creates an instance of an issue."""
        self.title = title
        self.description = description
        self.labels = labels or []
        self.comments: list[Comment] = []

    def add_comment(self, comment: Comment) -> None:
        """Attaches a comment to this issue."""
        self.comments.append(comment)

    def __repr__(self) -> str:
        """Returns a string representing each field of an issue."""
        return f"Issue(title='{self.title}', labels={self.labels}, comments={len(self.comments)})"


class IssueTrackerClient:
    """An in-memory implementation of an issue tracker client."""

    def __init__(self) -> None:
        """Creates in instance of an IssueTrackerClient."""
        self.issues: dict[str, Issue] = OrderedDict()
        self.counter: int = 1

    def create_issue(self, issue: Issue) -> str:
        """Creates a new issue and return its ID."""
        issue_id = str(self.counter)
        self.issues[issue_id] = issue
        self.counter += 1
        return issue_id

    def get_issue(self, issue_id: str) -> Issue:
        """Retrieves an issue by ID and raises a ValueError if not found."""
        issue = self.issues.get(issue_id)
        if issue is None:
            msg = f"Issue {issue_id} not found."
            raise ValueError(msg)
        return issue

    def update_issue(self, issue_id: str, updates: dict[str, str]) -> None:
        """Update title or description of an issue."""
        issue = self.get_issue(issue_id)
        if "title" in updates:
            issue.title = updates["title"]
        if "description" in updates:
            issue.description = updates["description"]

    def close_issue(self, issue_id: str) -> None:
        """Removes an issue from the tracker."""
        if issue_id not in self.issues:
            msg = f"Issue '{issue_id}' not found."
            raise ValueError(msg)
        del self.issues[issue_id]

    def add_comment(self, issue_id: str, comment: Comment) -> None:
        """Adds a comment to an existing issue."""
        issue = self.get_issue(issue_id)
        issue.add_comment(comment)
