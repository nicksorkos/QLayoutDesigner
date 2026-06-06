import os
from datetime import datetime

from .layout_dialog import LayoutSettingsDialog

from qgis.PyQt.QtWidgets import QAction, QMessageBox, QFileDialog
from qgis.PyQt.QtGui import QIcon, QFont

from qgis.core import (
    QgsApplication,
    QgsProject,
    QgsPrintLayout,
    QgsLayoutExporter,
    QgsLayoutItemMap,
    QgsLayoutItemLabel,
    QgsLayoutItemLegend,
    QgsLayoutItemScaleBar,
    QgsLayoutItemPicture,
    QgsLayoutItemMapGrid,
    QgsLayoutItemPage,
    QgsLayoutPoint,
    QgsLayoutSize,
    QgsUnitTypes
)


class QLayoutDesigner:

    def __init__(self, iface):
        self.iface = iface
        self.action = None

    def initGui(self):
        icon_path = os.path.join(os.path.dirname(__file__), "icon.png")

        self.action = QAction(
            QIcon(icon_path),
            "Create Automatic Layout",
            self.iface.mainWindow()
        )

        self.action.triggered.connect(self.run)
        self.iface.addPluginToMenu("&QLayout Designer", self.action)
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        self.iface.removePluginMenu("&QLayout Designer", self.action)
        self.iface.removeToolBarIcon(self.action)

    def get_unique_layout_name(self, manager, base_name):
        counter = 1
        final_name = base_name

        while manager.layoutByName(final_name):
            counter += 1
            final_name = f"{base_name} {counter}"

        return final_name

    def add_map_grid(self, map_item):
        grid = QgsLayoutItemMapGrid("Auto Grid", map_item)

        grid.setEnabled(True)
        grid.setIntervalX(500)
        grid.setIntervalY(500)
        grid.setAnnotationEnabled(True)
        grid.setAnnotationPrecision(0)
        grid.setAnnotationFrameDistance(2)

        map_item.grids().addGrid(grid)
        map_item.refresh()

    def apply_layout_size(self, layout, layout_size):
        page = layout.pageCollection().page(0)

        if layout_size == "A4 Landscape":
            page.setPageSize("A4", QgsLayoutItemPage.Landscape)

        elif layout_size == "A4 Portrait":
            page.setPageSize("A4", QgsLayoutItemPage.Portrait)

        elif layout_size == "A3 Landscape":
            page.setPageSize("A3", QgsLayoutItemPage.Landscape)

        elif layout_size == "A3 Portrait":
            page.setPageSize("A3", QgsLayoutItemPage.Portrait)

    def export_to_pdf(self, layout):
        pdf_path, _ = QFileDialog.getSaveFileName(
            None,
            "Export Layout as PDF",
            "",
            "PDF Files (*.pdf)"
        )

        if not pdf_path:
            return

        if not pdf_path.lower().endswith(".pdf"):
            pdf_path += ".pdf"

        exporter = QgsLayoutExporter(layout)

        result = exporter.exportToPdf(
            pdf_path,
            QgsLayoutExporter.PdfExportSettings()
        )

        if result == QgsLayoutExporter.Success:
            QMessageBox.information(
                None,
                "Export Successful",
                f"PDF exported:\n{pdf_path}"
            )
        else:
            QMessageBox.warning(
                None,
                "Export Failed",
                "Could not export PDF."
            )

    def run(self):
        dialog = LayoutSettingsDialog()

        if dialog.exec_() != dialog.Accepted:
            return

        settings = dialog.get_values()

        project = QgsProject.instance()
        manager = project.layoutManager()

        layout_name = self.get_unique_layout_name(
            manager,
            "Map Layout"
        )

        try:
            layout = QgsPrintLayout(project)
            layout.initializeDefaults()
            layout.setName(layout_name)

            self.apply_layout_size(
                layout,
                settings["layout_size"]
            )

            manager.addLayout(layout)

            # =========================
            # MAIN MAP
            # =========================
            map_item = QgsLayoutItemMap(layout)
            map_item.setRect(20, 20, 200, 120)
            map_item.setExtent(self.iface.mapCanvas().extent())
            map_item.setScale(settings["scale"])

            layout.addLayoutItem(map_item)

            map_item.attemptMove(
                QgsLayoutPoint(
                    10,
                    25,
                    QgsUnitTypes.LayoutMillimeters
                )
            )

            map_item.attemptResize(
                QgsLayoutSize(
                    190,
                    135,
                    QgsUnitTypes.LayoutMillimeters
                )
            )

            if settings["show_grid"]:
                self.add_map_grid(map_item)

            # =========================
            # TITLE
            # =========================
            title = QgsLayoutItemLabel(layout)
            title.setText(settings["title"])
            title.setFont(QFont("Times New Roman", 20))
            title.adjustSizeToText()

            layout.addLayoutItem(title)

            title.attemptMove(
                QgsLayoutPoint(
                    10,
                    8,
                    QgsUnitTypes.LayoutMillimeters
                )
            )

            # =========================
            # NORTH ARROW
            # =========================
            if settings["show_north"]:
                north_arrow = QgsLayoutItemPicture(layout)

                north_arrow_path = os.path.join(
                    QgsApplication.svgPaths()[0],
                    "arrows",
                    "NorthArrow_01.svg"
                )

                if os.path.exists(north_arrow_path):
                    north_arrow.setPicturePath(north_arrow_path)

                layout.addLayoutItem(north_arrow)

                north_arrow.attemptMove(
                    QgsLayoutPoint(
                        175,
                        30,
                        QgsUnitTypes.LayoutMillimeters
                    )
                )

                north_arrow.attemptResize(
                    QgsLayoutSize(
                        20,
                        20,
                        QgsUnitTypes.LayoutMillimeters
                    )
                )

            # =========================
            # NUMERIC SCALE
            # =========================
            if settings["show_numeric_scale"]:
                scale_value = settings["scale"]
                formatted_scale = f"{scale_value:,}".replace(",", ".")

                numeric_scale = QgsLayoutItemLabel(layout)
                numeric_scale.setText(
                    f"Scale : 1:{formatted_scale}"
                )

                numeric_scale.setFont(QFont("Times New Roman", 12))
                numeric_scale.adjustSizeToText()

                layout.addLayoutItem(numeric_scale)

                numeric_scale.attemptMove(
                    QgsLayoutPoint(
                        10,
                        164,
                        QgsUnitTypes.LayoutMillimeters
                    )
                )

            # =========================
            # GRAPHIC SCALE BAR
            # =========================
            if settings["show_scale_bar"]:
                scale_bar = QgsLayoutItemScaleBar(layout)
                scale_bar.setStyle("Double Box")
                scale_bar.setLinkedMap(map_item)
                scale_bar.setUnits(QgsUnitTypes.DistanceMeters)
                scale_bar.setNumberOfSegments(4)
                scale_bar.setNumberOfSegmentsLeft(0)
                scale_bar.setUnitsPerSegment(50)
                scale_bar.setUnitLabel("m")
                scale_bar.applyDefaultSize()

                layout.addLayoutItem(scale_bar)

                scale_bar.attemptMove(
                    QgsLayoutPoint(
                        10,
                        172,
                        QgsUnitTypes.LayoutMillimeters
                    )
                )

            # =========================
            # LEGEND
            # =========================
            if settings["show_legend"]:
                legend = QgsLayoutItemLegend(layout)
                legend.setTitle("Legend")
                legend.setLinkedMap(map_item)
                legend.setAutoUpdateModel(True)

                layout.addLayoutItem(legend)

                legend.attemptMove(
                    QgsLayoutPoint(
                        205,
                        25,
                        QgsUnitTypes.LayoutMillimeters
                    )
                )

                legend.attemptResize(
                    QgsLayoutSize(
                        80,
                        120,
                        QgsUnitTypes.LayoutMillimeters
                    )
                )

            # =========================
            # CRS LABEL
            # =========================
            crs_label = QgsLayoutItemLabel(layout)
            crs_text = project.crs().authid()

            crs_label.setText(
                f"Map view: {crs_text}"
            )

            crs_label.setFont(QFont("Times New Roman", 10))
            crs_label.adjustSizeToText()

            layout.addLayoutItem(crs_label)

            crs_label.attemptMove(
                QgsLayoutPoint(
                    10,
                    188,
                    QgsUnitTypes.LayoutMillimeters
                )
            )

            # =========================
            # DESIGNER LABEL
            # =========================
            designer_label = QgsLayoutItemLabel(layout)
            designer_label.setText(
                f"Cartographic Editing: {settings['designer']}"
            )

            designer_label.setFont(QFont("Times New Roman", 10))
            designer_label.adjustSizeToText()

            layout.addLayoutItem(designer_label)

            designer_label.attemptMove(
                QgsLayoutPoint(
                    10,
                    198,
                    QgsUnitTypes.LayoutMillimeters
                )
            )

            # =========================
            # DATE LABEL
            # =========================
            date_label = QgsLayoutItemLabel(layout)
            date_text = datetime.now().strftime("%d/%m/%Y")

            date_label.setText(
                f"Date: {date_text}"
            )

            date_label.setFont(QFont("Times New Roman", 10))
            date_label.adjustSizeToText()

            layout.addLayoutItem(date_label)

            date_label.attemptMove(
                QgsLayoutPoint(
                    10,
                    208,
                    QgsUnitTypes.LayoutMillimeters
                )
            )

            # =========================
            # PREVIEW FIRST
            # =========================
            self.iface.openLayoutDesigner(layout)

            reply = QMessageBox.question(
                None,
                "QLayout Designer",
                "The layout has been created successfully.\n\nDo you want to export it to PDF now?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                self.export_to_pdf(layout)

        except Exception as e:
            QMessageBox.critical(
                None,
                "QLayout Designer Error",
                str(e)
            )