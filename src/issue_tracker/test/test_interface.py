from __future__ import annotations
import unittest
from typing import Dict
from src.issue_tracker.issue_tracker_interface import Issue, IssueTrackerClient


class MockIssueTrackerClient(IssueTrackerClient):
    """A mock implementation for testing the IssueTrackerClient interface.
    It stores issues in a dictionary and simulates create, read, update,
    and delete (close) operations.
    """

    def __init__(self):
        """Initializes the mock IssueTrackerClient."""
        self.issues = {}
        self.counter = 1

    def create_issue(self, issue: Issue) -> str:
        """Creates a sample instance of an issue."""
        issue_id = str(self.counter)
        self.issues[issue_id] = issue
        self.counter += 1
        return issue_id

    def get_issue(self, issue_id: str) -> Issue:
        """Simulates returning a sample issue's ID."""
        return self.issues.get(issue_id)

    def update_issue(self, issue_id: str, updates: Dict[str, str]) -> None:
        """Simulates updating an issue's title or description."""
        issue = self.issues.get(issue_id)
        if not issue:
            return
        if "title" in updates:
            issue.title = updates["title"]
        if "description" in updates:
            issue.description = updates["description"]

    def close_issue(self, issue_id: str) -> None:
        """Simulates closing an issue by removing it from storage."""
        self.issues.pop(issue_id, None)


class TestIssueTrackerClient(unittest.TestCase):
    """A class for testing the IssueTrackerClient using a mock implemntation that
    stores issues in memory.
    """

    def setUp(self):
        """Sets up a sample issue using the mock client."""
        self.client = MockIssueTrackerClient()
        self.issue = Issue(title="Bug", description="Something broke", labels=["bug"])

    def test_create_and_get_issue(self):
        """Tests the creation of an issue and retrieval of its ID."""
        issue_id = self.client.create_issue(self.issue)
        fetched = self.client.get_issue(issue_id)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.title, "Bug")

    def test_update_issue(self):
        """Tests the updating of a title and description of an issue."""
        issue_id = self.client.create_issue(self.issue)
        self.client.update_issue(issue_id, {"title": "Updated Bug", "description": "New description"})
        updated = self.client.get_issue(issue_id)
        self.assertEqual(updated.title, "Updated Bug")
        self.assertEqual(updated.description, "New description")

    def test_close_issue(self):
        """Verifies that closing an issue removes it from memory."""
        issue_id = self.client.create_issue(self.issue)
        self.client.close_issue(issue_id)
        self.assertIsNone(self.client.get_issue(issue_id))


if __name__ == "__main__":
    unittest.main()
