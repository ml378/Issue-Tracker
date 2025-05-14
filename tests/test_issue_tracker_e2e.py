from __future__ import annotations
import unittest
from src.issue_tracker.issue_tracker import Comment, Issue, IssueTrackerClient


class TestIssueLifecycle(unittest.TestCase):
    """Tests the full lifecycle and each function of the in-memory IssueTrackerClient."""

    def test_full_issue_lifecycle(self):
        """Goes through each step of an issue's lifecycle and verifies its functionality."""
        client = IssueTrackerClient()
        # Create an issue
        issue = Issue("Feature request", "Add dark mode", labels=["feature"])
        issue_id = client.create_issue(issue)
        self.assertIsNotNone(issue_id)
        # Add a comment
        comment = Comment("Name", "We need this for Q3.")
        client.add_comment(issue_id, comment)
        # Verify everything
        fetched = client.get_issue(issue_id)
        self.assertEqual(fetched.title, "Feature request")
        self.assertEqual(len(fetched.comments), 1)
        self.assertEqual(fetched.comments[0].author, "Name")
        # Close the issue
        client.close_issue(issue_id)
        # Try to fetch the closed issue
        with self.assertRaises(ValueError):
            client.get_issue(issue_id)


if __name__ == "__main__":
    unittest.main()
