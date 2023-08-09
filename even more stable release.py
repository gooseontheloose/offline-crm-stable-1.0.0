import sys
import json
import os
import csv
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QComboBox, QTabWidget, QFileDialog
from PyQt5.QtGui import QFont, QPalette, QColor, QPixmap
from PyQt5.QtCore import Qt
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtWidgets import QMessageBox


def install_dependencies():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    except subprocess.CalledProcessError:
        print("Failed to install required dependencies.")
        sys.exit(1)

def check_dependencies():
    try:
        import PyQt5
        import reportlab
    except ImportError:
        return False
    return True

class ContractorLeadsApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Contractor Leads Database by REA")
        self.setGeometry(100, 100, 1600, 800)

        if not check_dependencies():
            install_dependencies()

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.leads = []
        self.load_leads_data()

        self.setup_ui()

    def setup_ui(self):
        self.tabs = TabWidget(self, self.leads)
        self.logo_label = QLabel()
        self.logo_pixmap = QPixmap("logo.png")
        self.logo_pixmap = self.logo_pixmap.scaledToWidth(150, Qt.SmoothTransformation)
        self.logo_label.setPixmap(self.logo_pixmap)
        self.logo_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.logo_label)
        layout.addWidget(self.tabs)
        self.central_widget.setLayout(layout)

        self.set_dark_theme()

    def set_dark_theme(self):
        app = QApplication.instance()
        app.setStyle("Fusion")

        # Dark palette
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, Qt.black)
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.AlternateBase, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)

        app.setPalette(dark_palette)

        # Set the font for all widgets to improve readability
        app_font = QFont("Arial", 10)
        app.setFont(app_font)

    def closeEvent(self, event):
        self.save_leads_data()
        event.accept()

    def save_leads_data(self):
        with open("leads_data.json", "w") as file:
            json.dump(self.leads, file)

    def load_leads_data(self):
        if os.path.exists("leads_data.json"):
            try:
                with open("leads_data.json", "r") as file:
                    self.leads = json.load(file)
            except json.JSONDecodeError:
                self.leads = []
        else:
            folder_path = os.path.dirname(os.path.abspath(__file__))
            os.makedirs(folder_path, exist_ok=True)
            self.leads = []


class TabWidget(QWidget):
    def __init__(self, parent, leads_list):
        super().__init__()

        self.leads_list = leads_list

        self.tabs = QTabWidget(self)

        self.contractor_input_tab = ContractorInputTab(self.leads_list, self)
        self.leads_table_tab = LeadsTableTab(self.leads_list)  # Remove the second argument
        self.calendar_tab = ComingSoonTab()
        self.calls_tab = ComingSoonTab()
        self.email_tab = QTabWidget()
        self.email_gmail_tab = ComingSoonTab()
        self.email_smtp_tab = ComingSoonTab()
        self.messaging_tab = QTabWidget()
        self.messaging_twilio_tab = ComingSoonTab()
        self.forms_tab = QTabWidget()
        self.forms_my_forms_tab = ComingSoonTab()
        self.forms_create_tab = ComingSoonTab()
        self.forms_embed_tab = ComingSoonTab()
        self.forms_settings_tab = ComingSoonTab()
        self.integrations_tab = ComingSoonTab()
        self.settings_tab = ComingSoonTab()

        self.email_tab.addTab(self.email_gmail_tab, "Gmail")
        self.email_tab.addTab(self.email_smtp_tab, "SMTP")

        self.messaging_tab.addTab(self.messaging_twilio_tab, "Twilio")

        self.forms_tab.addTab(self.forms_my_forms_tab, "My Forms")
        self.forms_tab.addTab(self.forms_create_tab, "Create")
        self.forms_tab.addTab(self.forms_embed_tab, "Embed")
        self.forms_tab.addTab(self.forms_settings_tab, "Settings")

        self.tabs.addTab(self.contractor_input_tab, "Contractor Leads Input")
        self.tabs.addTab(self.leads_table_tab, "Leads Table View")
        self.tabs.addTab(self.calendar_tab, "Calendar")
        self.tabs.addTab(self.calls_tab, "Calls")
        self.tabs.addTab(self.email_tab, "Email")
        self.tabs.addTab(self.messaging_tab, "Messaging")
        self.tabs.addTab(self.forms_tab, "Forms")
        self.tabs.addTab(self.integrations_tab, "Integrations")
        self.tabs.addTab(self.settings_tab, "Settings")

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)

class ContractorInputTab(QWidget):
    def __init__(self, leads_list, parent):
        super().__init__()

        self.leads_list = leads_list
        self.parent = parent

        self.name_label = QLabel("Name:")
        self.name_input = QLineEdit()

        self.address_label = QLabel("Address:")
        self.address_input = QLineEdit()

        self.phone_label = QLabel("Phone Number:")
        self.phone_input = QLineEdit()

        self.email_label = QLabel("Email:")
        self.email_input = QLineEdit()

        self.notes_label = QLabel("Notes:")
        self.notes_input = QTextEdit()

        self.referred_by_label = QLabel("Referred By:")
        self.referred_by_input = QLineEdit()
        
        self.job_type_label = QLabel("Job Type:")
        self.job_type_dropdown = QComboBox()
        self.job_type_dropdown.addItems(["Residential", "Commercial", "Unknown"])
        
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.add_lead)  # Connect to the add_lead method

        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.address_label)
        layout.addWidget(self.address_input)
        layout.addWidget(self.phone_label)
        layout.addWidget(self.phone_input)
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.notes_label)
        layout.addWidget(self.notes_input)
        layout.addWidget(self.referred_by_label)
        layout.addWidget(self.referred_by_input)
        layout.addWidget(self.job_type_label)
        layout.addWidget(self.job_type_dropdown)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def add_lead(self):
        name = self.name_input.text()
        address = self.address_input.text()
        phone = self.phone_input.text()
        email = self.email_input.text()
        notes = self.notes_input.toPlainText()
        referred_by = self.referred_by_input.text()
        job_type = self.job_type_dropdown.currentText()

        lead_data = {
            "Name": name,
            "Address": address,
            "Phone": phone,
            "Email": email,
            "Notes": notes,
            "Referred By": referred_by,
            "Job Type": job_type,
            "Lead Status": "In System"  # Set the initial status here
        }

        # Append the lead data to the leads_list
        self.leads_list.append(lead_data)
        self.parent.leads_table_tab.populate_table()
        
        # Clear input fields after adding the lead
        self.name_input.clear()
        self.address_input.clear()
        self.phone_input.clear()
        self.email_input.clear()
        self.notes_input.clear()
        self.job_type_dropdown.setCurrentIndex(0)

class CustomDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = super().createEditor(parent, option, index)
        if isinstance(editor, QLineEdit):
            editor.editingFinished.connect(lambda: self.commitData.emit(editor))
        elif isinstance(editor, QComboBox):
            editor.currentIndexChanged.connect(lambda: self.commitData.emit(editor))
        return editor
        
class LeadsTableTab(QWidget):
    def __init__(self, leads_list):
        super().__init__()
        self.edit_mode = False  # Initialize edit_mode to False

        self.leads_list = leads_list

        self.table = QTableWidget(self)
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels(
            ["Lead Status", "Name", "Address", "Phone", "Email", "Notes", "Job Type", "Referred By", "Referred To", "Actions"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Apply custom delegate to handle editing of cell widgets
        delegate = CustomDelegate()
        self.table.setItemDelegate(delegate)
        
        # Create the refresh button
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.populate_table)

        # Create the export buttons
        self.export_csv_button = QPushButton("Export to CSV")
        self.export_csv_button.clicked.connect(self.export_to_csv)
        self.export_pdf_button = QPushButton("Export to PDF")
        self.export_pdf_button.clicked.connect(self.export_to_pdf)
        self.export_txt_button = QPushButton("Export to TXT")
        self.export_txt_button.clicked.connect(self.export_to_txt)

        # Create the toggle edit mode button
        self.toggle_edit_button = QPushButton("Toggle Edit Mode")
        self.toggle_edit_button.clicked.connect(self.toggle_edit_mode)

        # Modify the button sizes here
        button_width = 120
        button_height = 30

        # Set fixed sizes for the buttons
        self.refresh_button.setFixedSize(button_width, button_height)
        self.export_csv_button.setFixedSize(button_width, button_height)
        self.export_pdf_button.setFixedSize(button_width, button_height)
        self.export_txt_button.setFixedSize(button_width, button_height)
        self.toggle_edit_button.setFixedSize(button_width, button_height)

        # Create a layout for the export buttons
        export_button_layout = QVBoxLayout()
        export_button_layout.addWidget(self.export_csv_button)
        export_button_layout.addWidget(self.export_pdf_button)
        export_button_layout.addWidget(self.export_txt_button)

        # Create a layout for the buttons and set alignment
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.refresh_button)
        button_layout.addLayout(export_button_layout)
        button_layout.addWidget(self.toggle_edit_button)
        button_layout.setAlignment(Qt.AlignCenter)  # Center-align the buttons vertically

        # Create the main layout for the tab
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addLayout(button_layout)  # Add the button layout to the main layout

        self.setLayout(layout)

        self.populate_table()


    def toggle_edit_mode(self):
        self.edit_mode = not getattr(self, "edit_mode", False)
        
        for row in range(self.table.rowCount()):
            for col in range(1, self.table.columnCount() - 1):
                item = self.table.cellWidget(row, col)
                if isinstance(item, QLineEdit):
                    item.setReadOnly(not self.edit_mode)
        
        self.toggle_edit_button.setText("Editing Enabled" if self.edit_mode else "Editing Disabled")

    def createEditor(self, parent, option, index):
        if not self.edit_mode:
            QMessageBox.warning(self, "Editing Mode Off", "Editing must be enabled to edit cell data.")
            return None

        editor = super().createEditor(parent, option, index)
        if isinstance(editor, QLineEdit):
            editor.editingFinished.connect(lambda: self.commitData.emit(editor))
        elif isinstance(editor, QComboBox):
            editor.currentIndexChanged.connect(lambda: self.commitData.emit(editor))
        return editor

    def populate_table(self):
        self.table.setRowCount(len(self.leads_list))  # Clear existing rows
        for row, lead in enumerate(self.leads_list):

            # Status Combo Box
            status_combo = QComboBox()
            status_combo.addItems(["In System", "Good Lead", "Contact Later", "Bad Lead", "Passed Along", "Closed"])
            current_status = lead.get("Lead Status", "In System")
            status_combo.setCurrentText(current_status)
            status_combo.currentTextChanged.connect(lambda text, r=row: self.status_changed(r, text))
            self.table.setCellWidget(row, 0, status_combo)

            # Name, Address, Phone, Email
            name_input = QLineEdit(lead["Name"])
            name_input.editingFinished.connect(lambda r=row, input_field=name_input: self.input_field_changed(r, "Name", input_field.text()))
            self.table.setCellWidget(row, 1, name_input)

            address_input = QLineEdit(lead["Address"])
            address_input.editingFinished.connect(lambda r=row, input_field=address_input: self.input_field_changed(r, "Address", input_field.text()))
            self.table.setCellWidget(row, 2, address_input)

            phone_input = QLineEdit(lead["Phone"])
            phone_input.editingFinished.connect(lambda r=row, input_field=phone_input: self.input_field_changed(r, "Phone", input_field.text()))
            self.table.setCellWidget(row, 3, phone_input)

            email_input = QLineEdit(lead["Email"])
            email_input.editingFinished.connect(lambda r=row, input_field=email_input: self.input_field_changed(r, "Email", input_field.text()))
            self.table.setCellWidget(row, 4, email_input)
            
            # Notes
            notes_input = QLineEdit(lead["Notes"])
            self.table.setCellWidget(row, 5, notes_input)

            #Type, Referred to/by
            self.table.setItem(row, 6, QTableWidgetItem(lead["Job Type"]))
            self.table.setItem(row, 7, QTableWidgetItem(lead["Referred By"]))
            self.table.setItem(row, 8, QTableWidgetItem(lead.get("Referred To", "")))

            # Job Type Combo Box
            job_type_combo = QComboBox()
            job_type_combo.addItems(["Residential", "Commercial", "Other"])
            current_job_type = lead.get("Job Type", "Unknown")
            job_type_combo.setCurrentText(current_job_type)
            job_type_combo.currentTextChanged.connect(lambda text, r=row: self.job_type_changed(r, text))
            self.table.setCellWidget(row, 6, job_type_combo)

            # Referred By, Referred To
            referred_by_input = QLineEdit(lead.get("Referred By", ""))
            referred_by_input.textChanged.connect(lambda text, r=row: self.referred_by_changed(r, text))
            self.table.setCellWidget(row, 7, referred_by_input)
            referred_to_input = QLineEdit(lead.get("Referred To", ""))
            referred_to_input.textChanged.connect(lambda text, r=row: self.referred_to_changed(r, text))
            self.table.setCellWidget(row, 8, referred_to_input)

            # Delete Button
            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(lambda _, r=row: self.delete_lead(r))
            self.table.setCellWidget(row, 9, delete_button)

            # Connect input field changes to corresponding functions
            referred_by_input.textChanged.connect(lambda text, r=row: self.input_field_changed(r, "Referred By", text))
            referred_to_input.textChanged.connect(lambda text, r=row: self.input_field_changed(r, "Referred To", text))
            
    def input_field_changed(self, row, field_name, new_value):
        self.leads_list[row][field_name] = new_value

    def status_changed(self, row, text):
        self.leads_list[row]["Lead Status"] = text

    def name_changed(self, row, text):
        self.leads_list[row]["Name"] = text
        
    def address_changed(self, row, text):
        self.leads_list[row]["Address"] = text
        
    def phone_changed(self, row, text):
        self.leads_list[row]["Phone"] = text
        
    def email_changed(self, row, text):
        self.leads_list[row]["Email"] = text
        
    def notes_changed(self, row, text):
        self.leads_list[row]["Notes"] = text
        
    def referred_by_changed(self, row, text):
        self.leads_list[row]["Referred By"] = text

    def referred_to_changed(self, row, text):
        self.leads_list[row]["Referred To"] = text
        
    def export_to_csv(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Export to CSV", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_name:
            with open(file_name, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                # Write the header
                writer.writerow(["Name", "Address", "Phone", "Email", "Notes", "Job Type"])
                # Write the data
                for lead in self.leads_list:
                    writer.writerow([lead["Name"], lead["Address"], lead["Phone"], lead["Email"], lead["Notes"], lead["Job Type"]])

    def export_to_pdf(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Export to PDF", "", "PDF Files (*.pdf);;All Files (*)", options=options)
        if file_name:
            doc = SimpleDocTemplate(file_name, pagesize=letter)
            elements = []
            data = [["Name", "Address", "Phone", "Email", "Notes", "Job Type"]]
            for lead in self.leads_list:
                data.append([lead["Name"], lead["Address"], lead["Phone"], lead["Email"], lead["Notes"], lead["Job Type"]])
            t = Table(data)
            t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                   ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                   ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                   ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                   ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                   ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
            elements.append(t)
            doc.build(elements)

    def export_to_txt(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Export to TXT", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            with open(file_name, "w") as file:
                for lead in self.leads_list:
                    file.write(f"Name: {lead['Name']}\n")
                    file.write(f"Address: {lead['Address']}\n")
                    file.write(f"Phone: {lead['Phone']}\n")
                    file.write(f"Email: {lead['Email']}\n")
                    file.write(f"Notes: {lead['Notes']}\n")
                    file.write(f"Job Type: {lead['Job Type']}\n")
                    file.write("\n")

    def delete_lead(self, row):
        confirmation = QMessageBox.question(
            self, "Confirm Deletion",
            "Are you sure you want to delete this lead?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if confirmation == QMessageBox.Yes:
            del self.leads_list[row]
            self.populate_table()  # Refresh the table

    def job_type_changed(self, row, text):
        self.leads_list[row]["Job Type"] = text

class ComingSoonTab(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel("Coming Soon")
        self.label.setAlignment(Qt.AlignCenter)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ContractorLeadsApp()
    window.show()
    sys.exit(app.exec_())
