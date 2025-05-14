from __future__ import annotations
import unittest
from datetime import datetime
from src.issue_tracker.issue_tracker import Comment, Issue, IssueTrackerClient


class MockIssueTrackerClient(IssueTrackerClient):
    """A mock implementation for testing the IssueTrackerClient.

    It stores issues in a dictionary and simulates create, read, update, add comment,
    and delete (close) operations.
    """

    def __init__(self):
        """Initializes the mock IssueTrackerClient."""
        self.issues: dict[str, Issue] = {}
        self.counter = 1

    def create_issue(self, issue: Issue) -> str:
        """Creates a sample instance of an issue."""
        issue_id = str(self.counter)
        self.issues[issue_id] = issue
        self.counter += 1
        return issue_id

    def get_issue(self, issue_id: str) -> Issue:
        """Simulates returning a sample issue's ID."""
        issue = self.issues.get(issue_id)
        if issue is None:
            msg = f"Issue {issue_id} not found."
            raise ValueError(msg)
        return issue

    def update_issue(self, issue_id: str, updates: dict[str, str]) -> None:
        """Simulates updating an issue's title or description."""
        issue = self.issues.get(issue_id)
        if not issue:
            return
        if "title" in updates:
            issue.title = updates["title"]
        if "description" in updates:
            issue.description = updates["description"]

    def add_comment(self, issue_id: str, comment: Comment) -> None:
        """Simulates adding a comment to an existing issue."""
        issue = self.get_issue(issue_id)
        issue.add_comment(comment)

    def close_issue(self, issue_id: str) -> None:
        """Simulates closing an issue by removing it from memory."""
        if issue_id not in self.issues:
            msg = f"Issue {issue_id} not found."
            raise ValueError(msg)
        del self.issues[issue_id]


class TestIntegration(unittest.TestCase):
    """Integration test simulating full lifecycle of an issue using the mock client."""

    def setUp(self):
        """Creates an instance of the mock issue tracker client."""
        self.client = MockIssueTrackerClient()

    def test_issue(self):
        """Verifies the correct functionality of issue creation, retrieval from
        memory, issue updates, and closing.
        """
        issue = Issue("Crash on submit", "App crashes on clicking submit")
        issue_id = self.client.create_issue(issue)
        # Update the issue
        self.client.update_issue(issue_id, {
            "title": "Submit crash",
            "description": "Crash after form submission"
        })
        updated = self.client.get_issue(issue_id)
        self.assertEqual(updated.title, "Submit crash")
        self.assertEqual(updated.description, "Crash after form submission")
        # Add comments
        self.client.add_comment(issue_id, Comment("John", "I can reproduce this."))
        self.client.add_comment(issue_id, Comment("Jane", "This happens on iOS."))
        retrieved = self.client.get_issue(issue_id)
        self.assertEqual(len(retrieved.comments), 2)
        self.assertEqual(retrieved.comments[0].author, "John")
        self.assertEqual(retrieved.comments[1].message, "This happens on iOS.")
