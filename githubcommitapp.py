import sys
import requests
import json
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QTextBrowser,
)


class CommitLinksApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create the input field for the repository URL
        self.repo_url_label = QLabel("Enter a GitHub repository URL:")
        self.repo_url_edit = QLineEdit()

        # Create the input field for the security token
        self.token_label = QLabel("Enter your GitHub personal access token:")
        self.token_edit = QLineEdit()

        # Create the input fields for the start and end dates
        self.start_date_label = QLabel("Enter start date (YYYY-MM-DD):")
        self.start_date_edit = QLineEdit()
        self.end_date_label = QLabel("Enter end date (YYYY-MM-DD):")
        self.end_date_edit = QLineEdit()

        # Create the button to fetch the commit links
        self.fetch_button = QPushButton("Fetch Commit Links")
        self.fetch_button.clicked.connect(self.fetch_commit_links)

        # Create the text browser to display the commit links
        self.commit_links_browser = QTextBrowser()
        self.commit_links_browser.setOpenExternalLinks(True)

        # Create the layout
        layout = QVBoxLayout()
        layout.addWidget(self.repo_url_label)
        layout.addWidget(self.repo_url_edit)
        layout.addWidget(self.start_date_label)
        layout.addWidget(self.start_date_edit)
        layout.addWidget(self.end_date_label)
        layout.addWidget(self.end_date_edit)
        layout.addWidget(self.token_label)
        layout.addWidget(self.token_edit)
        layout.addWidget(self.fetch_button)
        layout.addWidget(self.commit_links_browser)
        self.setLayout(layout)
        self.setLayout(layout)

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle("Commit Links")
        self.show()

    def fetch_commit_links(self):
        # Clear the text browser
        self.commit_links_browser.clear()

        # Get the repository URL from the input field
        repo_url = self.repo_url_edit.text()

        # Extract the repository owner and name from the URL
        parts = repo_url.split("/")
        owner = parts[3]
        repo = parts[4]

        # Get the security token from the input field
        token = self.token_edit.text()

        # Get the start and end dates for the commit search
        start_date = self.start_date_edit.text()
        end_date = self.end_date_edit.text()

        if self.token_edit.text() != "":
            # Add the Authorization header with the bearer token
            headers = {"Authorization": f"Bearer {token}"}
        else:
            # Don't include the Authorization header
            headers = {}

        # Make a request to the GitHub API to get the list of commits
        api_url = f"https://api.github.com/repos/{owner}/{repo}/commits"
        params = {"since": start_date, "until": end_date}
        response = requests.get(api_url, headers=headers, params=params)

        # Check if the request was successful
        if response.status_code != 200:
            print("Error: Could not fetch commits for the repository")
        else:
            # Parse the response as JSON
            data = json.loads(response.text)

            # Add a clickable link for each commit to the text browser
            for i, commit in enumerate(data[:10]):
                commit_sha = commit["sha"]
                commit_url = f"https://github.com/{owner}/{repo}/commit/{commit_sha}"
                self.commit_links_browser.append(
                    f"<a href='{commit_url}'>{commit_url}</a>"
                )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = CommitLinksApp()
    sys.exit(app.exec_())
