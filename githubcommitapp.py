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
    QFileDialog,
    QCalendarWidget,
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

        # Create the calendar widgets for selecting the start and end dates
        self.start_date_label = QLabel("Select start date:")
        self.start_date_calendar = QCalendarWidget()
        self.end_date_label = QLabel("Select end date:")
        self.end_date_calendar = QCalendarWidget()

        # Create the button to fetch the commit links
        self.fetch_button = QPushButton("Fetch Commit Links")
        self.fetch_button.clicked.connect(self.fetch_commit_links)

        # Create the text browser to display the commit links
        self.commit_links_browser = QTextBrowser()
        self.commit_links_browser.setOpenExternalLinks(True)

        # Create the export button
        self.export_button = QPushButton("Export Results")
        self.export_button.clicked.connect(self.export_results)

        # Create the layout
        layout = QVBoxLayout()
        layout.addWidget(self.repo_url_label)
        layout.addWidget(self.repo_url_edit)
        layout.addWidget(self.token_label)
        layout.addWidget(self.token_edit)
        layout.addWidget(self.start_date_label)
        layout.addWidget(self.start_date_calendar)
        layout.addWidget(self.end_date_label)
        layout.addWidget(self.end_date_calendar)
        layout.addWidget(self.fetch_button)
        layout.addWidget(self.commit_links_browser)
        layout.addWidget(self.export_button)
        self.setLayout(layout)
        self.setLayout(layout)

        self.setGeometry(700, 250, 300, 150)
        self.setWindowTitle("Github Commit Search")
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
        start_date = self.start_date_calendar.selectedDate().toString("yyyy-MM-dd")
        end_date = self.end_date_calendar.selectedDate().toString("yyyy-MM-dd")

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
            for i, commit in enumerate(data[:500]):
                commit_sha = commit["sha"]
                commit_url = f"https://github.com/{owner}/{repo}/commit/{commit_sha}"
                self.commit_links_browser.append(
                    f"<a href='{commit_url}'>{commit_url}</a>"
                )

    def export_results(self):
        # Get the commit links from the text browser
        commit_links = self.commit_links_browser.toPlainText()

        # Prompt the user to select a file to save the commit links to
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save File", "", "Text Files (*.txt)", options=options
        )

        if file_name:
            # Save the commit links to the selected file
            with open(file_name, "w") as f:
                f.write(commit_links)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = CommitLinksApp()
    sys.exit(app.exec_())
