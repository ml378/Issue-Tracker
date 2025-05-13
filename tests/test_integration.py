from __future__ import annotations
import unittest
from src.issue_tracker.issue_tracker_interface import Issue, IssueTrackerClient


class MockIssueTrackerClient(IssueTrackerClient):
    """A mock implementation for testing the IssueTrackerClient interface.

    It stores issues in a dictionary and simulates create, read, update,
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
        # Create
        issue = Issue("Integration test", "Testing full flow", labels=["test"])
        issue_id = self.client.create_issue(issue)
        self.assertIsNotNone(issue_id)

        # Retrieve
        retrieved = self.client.get_issue(issue_id)
        self.assertEqual(retrieved.title, "Integration test")

        # Update
        self.client.update_issue(issue_id, {"title": "Updated title"})
        updated = self.client.get_issue(issue_id)
        self.assertEqual(updated.title, "Updated title")

        # Close
        self.client.close_issue(issue_id)
        with self.assertRaises(ValueError):
            self.client.get_issue(issue_id)
