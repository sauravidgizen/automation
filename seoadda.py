import sys
import threading
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QTextEdit
)
from PyQt5.QtCore import Qt

class KeywordTool(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Keyword Research Tool")
        self.setGeometry(100, 100, 500, 400)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Enter Keyword:")
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("e.g., chandni chowk")

        self.start_button = QPushButton("Start Research")
        self.start_button.clicked.connect(self.start_process)

        self.status_box = QTextEdit()
        self.status_box.setReadOnly(True)

        layout.addWidget(self.label)
        layout.addWidget(self.input_field)
        layout.addWidget(self.start_button)
        layout.addWidget(self.status_box)

        self.setLayout(layout)

    def start_process(self):
        keyword = self.input_field.text().strip()
        if keyword:
            self.status_box.append(f"🔍 Starting automation for: {keyword}")
            thread = threading.Thread(target=self.run_selenium, args=(keyword,))
            thread.start()
        else:
            self.status_box.append("❌ Please enter a keyword.")

    def run_selenium(self, keyword):
        self.update_status("✅ Successfully opened Keyword Magic Tool!")
        self.update_status("✅ Opened the location dropdown")
        self.update_status("✅ Selected 'India'")
        self.update_status(f"🔍 Searching for keyword: {keyword}")
        self.update_status("✅ Clicked on 'All Keywords' tab.")
        self.update_status("✅ Clicked on Export tab.")
        self.update_status("✅ CSV export clicked!")
        self.update_status("⏳ Waiting for download to begin...")
        
        # Simulate processing time
        import time
        time.sleep(3)

        self.update_status("✅ Process completed. Closing browser...")

    def update_status(self, message):
        self.status_box.append(message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KeywordTool()
    window.show()
    sys.exit(app.exec_())
