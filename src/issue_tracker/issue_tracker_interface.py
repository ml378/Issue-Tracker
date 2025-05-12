from abc import ABC, abstractmethod
from typing import List, Dict, Optional


class Issue:
    """
    Represents a generic issue with a title, description, and optional labels.
    """
    def __init__(self, title: str, description: str, labels: Optional[List[str]] = None):
        """Initializes a new issue."""
        self.title = title
        self.description = description
        self.labels = labels or []

    def __repr__(self):
        return f"Issue(title='{self.title}', labels={self.labels})"


class IssueTrackerClient(ABC):
    """
    An abstract base class that defines a standard interface for an issue tracker client.
    """
    @abstractmethod
    def create_issue(self, issue: Issue) -> str:
        """Creates an issue and returns its ID or URL"""
        pass

    @abstractmethod
    def get_issue(self, issue_id: str) -> Issue:
        """Fetches an issue by its ID."""
        pass

    @abstractmethod
    def update_issue(self, issue_id: str, updates: Dict[str, str]) -> None:
        """Updates an issue with given fields."""
        pass

    @abstractmethod
    def close_issue(self, issue_id: str) -> None:
        """Closes an issue."""
        pass
