# Sample Interface for an Issue Tracker Client

This project includes a sample interface for building an issue tracker client using python.

## Features
- A generic issue model in class 'Issue'
- An abstract base class 'IssueTrackerClient'
- A mock implementation for testing 'MockIssueTrackerClient'
- Unit tests validating the interface contract

## Use Cases
- Build interchangeable clients for services like GitHub, GitLab, Trello, or Jira
- Plug issue tracking logic into apps using dependency injection
- Write reliable, backend-agnostic tests using the mock client

## Project Structure
- issue_tracker_interface.py      # Abstract base class and data model
- test_issue_tracker_interface.py # Unit tests using unittest

## Sample Usage
    # Dependency-injected client
    tracker = MockIssueTrackerClient()

    # Create a new issue
    issue = Issue(
        title="Login button not working",
        description="Clicking the login button does nothing on Firefox.",
        labels=["bug", "frontend"]
    )
    issue_id = tracker.create_issue(issue)

    # Retrieve and print the issue
    retrieved = tracker.get_issue(issue_id)
    print("Retrieved:", retrieved)

    # Update the issue
    tracker.update_issue(issue_id, {
        "title": "Login fails on Firefox 117+",
        "description": "Button click does not trigger login on latest version."
    })

    # Close the issue
    tracker.close_issue(issue_id)

# Prerequisite
- Python 3.8 or higher
- UV for Python dependency management

# Setup & Installation
Clone the repository:
    ```sh
    git clone https://github.com/ml378/Issue-Tracker.git
    cd Issue_Tracker
    ```
Install dependencies:
    ```sh
    python -m venv venv
    source venv/bin/activate
    pip install uv
    uv pip install -r requirements.txt
    ```
Run tests:
    ```sh
    pytest --cov=src --cov-report=html
    ```

    ```sh
    nose2 -v nose2_tests
    ```

    View test coverage:

    ```sh open htmlcov/index.html  # macOS
    xdg-open htmlcov/index.html  # Linux
    ```
