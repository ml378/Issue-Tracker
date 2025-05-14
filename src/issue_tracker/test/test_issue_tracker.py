from __future__ import annotations
import unittest
from datetime import datetime
from src.issue_tracker.issue_tracker import Comment, Issue, IssueTrackerClient


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

    def test_add_comment(self):
        issue_id = self.client.create_issue(self.issue)
        comment = Comment(author="Name", message="Working on it.")
        self.client.add_comment(issue_id, comment)
        retrieved = self.client.get_issue(issue_id)
        self.assertEqual(len(retrieved.comments), 1)
        self.assertEqual(retrieved.comments[0].author, "Name")
        self.assertEqual(retrieved.comments[0].message, "Working on it.")
        self.assertIsInstance(retrieved.comments[0].timestamp, datetime)

    def test_close_issue(self):
        """Verifies that closing an issue removes it from memory."""
        issue_id = self.client.create_issue(self.issue)
        self.client.close_issue(issue_id)
        self.assertIsNone(self.client.get_issue(issue_id))


if __name__ == "__main__":
    unittest.main()
