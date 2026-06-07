from qgis.PyQt.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QSpinBox,
    QLineEdit,
    QComboBox,
    QCheckBox,
    QDialogButtonBox,
)


class LayoutSettingsDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("QLayout Designer - Layout Settings")
        self.setMinimumWidth(350)

        self.title_input = QLineEdit()
        self.title_input.setText("Map")

        self.designer_input = QLineEdit()
        self.designer_input.setText("Nikolaos Sorkos")
        
        self.at_vh_input = QLineEdit()
        self.at_vh_input.setText("")

        self.nl_res_input = QLineEdit()
        self.nl_res_input.setText("")

        self.onb_input = QLineEdit()
        self.onb_input.setText("6258")

        self.asb_input = QLineEdit()
        self.asb_input.setText("6")

        self.sm_nr_input = QLineEdit()
        self.sm_nr_input.setText("")

        self.sheet_input = QLineEdit()
        self.sheet_input.setText("Startseite")

        self.scale_combo = QComboBox()
        self.pages_spinbox = QSpinBox()
        self.pages_spinbox.setMinimum(1)
        self.pages_spinbox.setMaximum(20)
        self.pages_spinbox.setValue(1)
        self.scale_combo.addItems([
            "1:1.000",
            "1:2.500",
            "1:5.000",
            "1:10.000",
            "1:25.000",
            "1:50.000",
            "1:100.000",
            "1:250.000"
        ])
        self.scale_combo.setCurrentText("1:250.000")

        self.size_combo = QComboBox()
        self.size_combo.addItems([
            "A4 Landscape",
            "A4 Portrait",
            "A3 Landscape",
            "A3 Portrait"
        ])
        self.size_combo.setCurrentText("A4 Landscape")

        self.legend_checkbox = QCheckBox("Legend")
        self.legend_checkbox.setChecked(True)

        self.north_checkbox = QCheckBox("North Arrow")
        self.north_checkbox.setChecked(True)



        self.scale_bar_checkbox = QCheckBox("Graphic Scale")
        self.scale_bar_checkbox.setChecked(True)

        self.numeric_scale_checkbox = QCheckBox("Scale")
        self.numeric_scale_checkbox.setChecked(True)

        form_layout = QFormLayout()
        form_layout.addRow("Map Title:", self.title_input)
        form_layout.addRow("Cartographic Editing:", self.designer_input)
        form_layout.addRow("AT/Vh-Bez:", self.at_vh_input)
        form_layout.addRow("NL/Res:", self.nl_res_input)
        form_layout.addRow("ONB:", self.onb_input)
        form_layout.addRow("ASB:", self.asb_input)
        form_layout.addRow("SM Nr:", self.sm_nr_input)
        form_layout.addRow("Blatt:", self.sheet_input)
        form_layout.addRow("Scale:", self.scale_combo)
        form_layout.addRow("Layout Size:", self.size_combo)
        form_layout.addRow("Number of Pages:", self.pages_spinbox)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)

        main_layout.addWidget(self.legend_checkbox)
        main_layout.addWidget(self.north_checkbox)
        main_layout.addWidget(self.scale_bar_checkbox)
        main_layout.addWidget(self.numeric_scale_checkbox)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        main_layout.addWidget(self.buttons)

        self.setLayout(main_layout)

    def get_values(self):
        scale_text = self.scale_combo.currentText()

        scale_value = int(
            scale_text.replace("1:", "").replace(".", "")
        )

        return {
            "title": self.title_input.text(),
            "designer": self.designer_input.text(),
            "scale": scale_value,
            "at_vh": self.at_vh_input.text(),
            "nl_res": self.nl_res_input.text(),
            "onb": self.onb_input.text(),
            "asb": self.asb_input.text(),
            "sm_nr": self.sm_nr_input.text(),
            "sheet": self.sheet_input.text(),
            "layout_size": self.size_combo.currentText(),
            "show_legend": self.legend_checkbox.isChecked(),
            "show_north": self.north_checkbox.isChecked(),
            "show_grid": False,
            "show_scale_bar": self.scale_bar_checkbox.isChecked(),
            "show_numeric_scale": self.numeric_scale_checkbox.isChecked(),
            "page_count": self.pages_spinbox.value()


        }