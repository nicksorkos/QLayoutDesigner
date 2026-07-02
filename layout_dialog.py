import os

from qgis.PyQt.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QFileDialog,
    QFormLayout,
    QSpinBox,
    QLineEdit,
    QComboBox,
    QCheckBox,
    QDialogButtonBox,
    QMessageBox,
    QGroupBox,
    QScrollArea,
    QWidget,
)


class LayoutSettingsDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("QLayout Designer — Layout Settings")
        self.setMinimumWidth(420)

        self.title_input = QLineEdit()
        self.title_input.setText("Map")

        self.designer_input = QLineEdit()
        self.designer_input.setText("Nikolaos Sorkos")

        self.company_input = QLineEdit()
        self.company_input.setText("")

        self.project_input = QLineEdit()
        self.project_input.setText("")

        self.client_input = QLineEdit()
        self.client_input.setText("")

        self.logo_input = QLineEdit()
        self.logo_input.setReadOnly(True)
        self.logo_button = QPushButton("Browse")
        self.logo_button.clicked.connect(self.browse_logo)

        self.coordinate_input = QLineEdit()
        self.coordinate_input.setText("")

        self.planer_input = QLineEdit()
        self.planer_input.setText("")

        self.datum_input = QLineEdit()
        self.datum_input.setText("")

        logo_layout = QHBoxLayout()
        logo_layout.addWidget(self.logo_input)
        logo_layout.addWidget(self.logo_button)

        self.at_vh_input = QLineEdit()
        self.nl_res_input = QLineEdit()

        self.onb_input = QLineEdit()
        self.onb_input.setText("6258")

        self.asb_input = QLineEdit()
        self.asb_input.setText("6")

        self.sm_nr_input = QLineEdit()

        self.sheet_input = QLineEdit()
        self.sheet_input.setText("Startseite")

        self.scale_combo = QComboBox()
        self.scale_combo.addItems([
            "1:500",
            "1:1,000",
            "1:2,000",
            "1:5,000",
            "1:10,000",
            "1:25,000"
        ])
        self.scale_combo.setCurrentText("1:1,000")

        self.size_combo = QComboBox()
        self.size_combo.addItems([
            "A4 Landscape",
            "A4 Portrait",
            "A3 Landscape",
            "A3 Portrait"
        ])
        self.size_combo.setCurrentText("A4 Landscape")

        self.pages_spinbox = QSpinBox()
        self.pages_spinbox.setMinimum(1)
        self.pages_spinbox.setMaximum(20)
        self.pages_spinbox.setValue(1)

        self.legend_checkbox = QCheckBox("Legend")
        self.legend_checkbox.setChecked(True)

        self.north_checkbox = QCheckBox("North Arrow")
        self.north_checkbox.setChecked(True)

        self.scale_bar_checkbox = QCheckBox("Graphic Scale")
        self.scale_bar_checkbox.setChecked(True)

        self.open_designer_checkbox = QCheckBox("Open Layout Designer")
        self.open_designer_checkbox.setChecked(True)

        self.title_input.setPlaceholderText("Enter layout title")
        self.designer_input.setPlaceholderText("Name of the cartographer")
        self.company_input.setPlaceholderText("Optional company name")
        self.project_input.setPlaceholderText("Optional project name")
        self.client_input.setPlaceholderText("Optional client name")
        self.logo_input.setPlaceholderText("Optional logo file")
        self.at_vh_input.setPlaceholderText("Drawing designation or reference")
        self.nl_res_input.setPlaceholderText("Project revision or reference")
        self.onb_input.setPlaceholderText("ONB reference")
        self.asb_input.setPlaceholderText("ASB reference")
        self.planer_input.setPlaceholderText("Optional planner name")
        self.datum_input.setPlaceholderText("Optional date")
        self.coordinate_input.setPlaceholderText("Optional coordinate system")
        self.sm_nr_input.setPlaceholderText("Document number")
        self.sheet_input.setPlaceholderText("Page identifier")

        self.legend_checkbox.setToolTip("Include the legend in the final layout")
        self.north_checkbox.setToolTip("Add a north arrow to every page")
        self.scale_bar_checkbox.setToolTip("Add a graphic scale bar linked to the map")
        self.open_designer_checkbox.setToolTip("Open the layout in the QGIS designer after creation")

        general_group = QGroupBox("General settings")
        general_form = QFormLayout()
        general_form.addRow("Map Title:", self.title_input)
        general_form.addRow("Designer:", self.designer_input)
        general_form.addRow("Company:", self.company_input)
        general_form.addRow("Project:", self.project_input)
        general_form.addRow("Client:", self.client_input)
        general_form.addRow("Logo Path:", logo_layout)
        general_group.setLayout(general_form)

        title_group = QGroupBox("Title block fields")
        title_form = QFormLayout()
        title_form.addRow("AT/Vh-Bez:", self.at_vh_input)
        title_form.addRow("NL/Res:", self.nl_res_input)
        title_form.addRow("ONB:", self.onb_input)
        title_form.addRow("ASB:", self.asb_input)
        title_form.addRow("Planer:", self.planer_input)
        title_form.addRow("Datum:", self.datum_input)
        title_form.addRow("Coordinate System:", self.coordinate_input)
        title_form.addRow("SM Nr:", self.sm_nr_input)
        title_form.addRow("Sheet:", self.sheet_input)
        title_group.setLayout(title_form)

        layout_group = QGroupBox("Layout options")
        layout_form = QFormLayout()
        layout_form.addRow("Scale:", self.scale_combo)
        layout_form.addRow("Layout Size:", self.size_combo)
        layout_form.addRow("Number of Pages:", self.pages_spinbox)
        layout_group.setLayout(layout_form)

        options_group = QGroupBox("Output options")
        options_layout = QVBoxLayout()
        options_layout.addWidget(self.legend_checkbox)
        options_layout.addWidget(self.north_checkbox)
        options_layout.addWidget(self.scale_bar_checkbox)
        options_layout.addWidget(self.open_designer_checkbox)
        options_group.setLayout(options_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(general_group)
        main_layout.addWidget(title_group)
        main_layout.addWidget(layout_group)
        main_layout.addWidget(options_group)

        scroll_widget = QWidget()
        scroll_widget.setLayout(main_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)

        outer_layout = QVBoxLayout()
        outer_layout.addWidget(scroll_area)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )

        self.buttons.accepted.connect(self.validate_and_accept)
        self.buttons.rejected.connect(self.reject)

        outer_layout.addWidget(self.buttons)
        self.setLayout(outer_layout)

    def validate_and_accept(self):
        if not self.title_input.text().strip():
            QMessageBox.warning(
                self,
                "Missing Title",
                "Please enter a map title before continuing."
            )
            return

        self.accept()

    def browse_logo(self):
        directory = os.path.dirname(self.logo_input.text()) if self.logo_input.text() else ""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Logo",
            directory,
            "Image Files (*.png *.jpg *.jpeg *.svg)"
        )

        if file_path:
            self.logo_input.setText(file_path)

    def get_values(self):
        scale_text = self.scale_combo.currentText()
        scale_value = int(
            scale_text.replace("1:", "").replace(".", "").replace(",", "").strip()
        )

        return {
            "title": self.title_input.text(),
            "designer": self.designer_input.text(),
            "company": self.company_input.text(),
            "project": self.project_input.text(),
            "client": self.client_input.text(),
            "logo_path": self.logo_input.text(),
            "at_vh": self.at_vh_input.text(),
            "nl_res": self.nl_res_input.text(),
            "onb": self.onb_input.text(),
            "asb": self.asb_input.text(),
            "planer": self.planer_input.text(),
            "datum": self.datum_input.text(),
            "coordinate_system": self.coordinate_input.text(),
            "sm_nr": self.sm_nr_input.text(),
            "sheet": self.sheet_input.text(),
            "layout_size": self.size_combo.currentText(),
            "scale": scale_value,
            "page_count": self.pages_spinbox.value(),
            "show_legend": self.legend_checkbox.isChecked(),
            "show_north": self.north_checkbox.isChecked(),
            "show_scale_bar": self.scale_bar_checkbox.isChecked(),
            "open_designer": self.open_designer_checkbox.isChecked(),
        }