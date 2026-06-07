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
    QgsLayoutItemPage,
    QgsLayoutItemShape,
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

    def create_extra_pages(self, layout, settings):
        page_collection = layout.pageCollection()

        while page_collection.pageCount() < settings["page_count"]:
            new_page = QgsLayoutItemPage(layout)

            if settings["layout_size"] == "A4 Landscape":
                new_page.setPageSize("A4", QgsLayoutItemPage.Landscape)
            elif settings["layout_size"] == "A4 Portrait":
                new_page.setPageSize("A4", QgsLayoutItemPage.Portrait)
            elif settings["layout_size"] == "A3 Landscape":
                new_page.setPageSize("A3", QgsLayoutItemPage.Landscape)
            elif settings["layout_size"] == "A3 Portrait":
                new_page.setPageSize("A3", QgsLayoutItemPage.Portrait)

            page_collection.addPage(new_page)

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

    def create_map_item(self, layout, settings):
        map_item = QgsLayoutItemMap(layout)
        map_item.setRect(20, 20, 200, 120)
        map_item.setExtent(self.iface.mapCanvas().extent())
        map_item.setScale(settings["scale"])

        layout.addLayoutItem(map_item)

        map_item.attemptMove(
            QgsLayoutPoint(10, 25, QgsUnitTypes.LayoutMillimeters)
        )

        map_item.attemptResize(
            QgsLayoutSize(190, 135, QgsUnitTypes.LayoutMillimeters)
        )

        return map_item

    def add_frame(self, layout, x, y, width, height):
        frame = QgsLayoutItemShape(layout)
        frame.setShapeType(QgsLayoutItemShape.Rectangle)

        layout.addLayoutItem(frame)

        frame.attemptMove(
            QgsLayoutPoint(x, y, QgsUnitTypes.LayoutMillimeters)
        )

        frame.attemptResize(
            QgsLayoutSize(width, height, QgsUnitTypes.LayoutMillimeters)
        )

        return frame

    def add_frame_label(self, layout, text, x, y, font_size=8, bold=False):
        label = QgsLayoutItemLabel(layout)
        label.setText(str(text))

        font = QFont("Times New Roman", font_size)
        font.setBold(bold)
        label.setFont(font)

        label.adjustSizeToText()
        layout.addLayoutItem(label)

        label.attemptMove(
            QgsLayoutPoint(x, y, QgsUnitTypes.LayoutMillimeters)
        )

        return label

    def create_title_block(self, layout, settings, page_index=0):
        page = layout.pageCollection().page(page_index)
        page_y = page.pos().y()

        date_text = datetime.now().strftime("%d/%m/%Y")
        scale_text = f"{settings['scale']:,}".replace(",", ".")
        sheet_text = f"{page_index + 1} / {settings['page_count']}"

        self.add_frame(layout, 10, page_y + 180, 277, 35)
        self.add_frame(layout, 10, page_y + 180, 45, 35)
        self.add_frame(layout, 55, page_y + 197, 90, 18)

        self.add_frame(layout, 55, page_y + 180, 110, 8)
        self.add_frame(layout, 55, page_y + 188, 110, 9)
        self.add_frame(layout, 55, page_y + 197, 110, 18)

        self.add_frame(layout, 165, page_y + 180, 65, 17)
        self.add_frame(layout, 165, page_y + 197, 65, 18)

        self.add_frame(layout, 230, page_y + 180, 57, 17)
        self.add_frame(layout, 230, page_y + 197, 57, 18)

        self.add_frame_label(layout, "AT/Vh-Bez:", 57, page_y + 182, 7, True)
        self.add_frame_label(layout, settings["at_vh"], 82, page_y + 182, 7)

        self.add_frame_label(layout, "NL/Res:", 57, page_y + 190, 7, True)
        self.add_frame_label(layout, settings["nl_res"], 82, page_y + 190, 7)

        self.add_frame_label(layout, "ONB:", 57, page_y + 201, 7, True)
        self.add_frame_label(layout, settings["onb"], 82, page_y + 201, 7)

        self.add_frame_label(layout, "ASB:", 167, page_y + 201, 7, True)
        self.add_frame_label(layout, settings["asb"], 190, page_y + 201, 7)

        self.add_frame_label(layout, "Planer:", 167, page_y + 206, 7, True)
        self.add_frame_label(layout, settings["designer"], 190, page_y + 206, 7)

        self.add_frame_label(layout, "Datum:", 167, page_y + 211, 7, True)
        self.add_frame_label(layout, date_text, 190, page_y + 211, 7)

        self.add_frame_label(layout, "SM Nr:", 232, page_y + 182, 7, True)
        self.add_frame_label(layout, settings["sm_nr"], 257, page_y + 182, 7)

        self.add_frame_label(layout, "Bezugssys:", 232, page_y + 201, 7, True)
        self.add_frame_label(
            layout,
            QgsProject.instance().crs().authid(),
            257,
            page_y + 201,
            7
        )

        self.add_frame_label(layout, "Maßstab:", 232, page_y + 206, 7, True)
        self.add_frame_label(layout, f"1:{scale_text}", 257, page_y + 206, 7)

        self.add_frame_label(layout, "Blatt:", 232, page_y + 211, 7, True)
        self.add_frame_label(layout, sheet_text, 257, page_y + 211, 7)

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

            self.apply_layout_size(layout, settings["layout_size"])
            self.create_extra_pages(layout, settings)

            manager.addLayout(layout)

            map_item = self.create_map_item(layout, settings)

            title = QgsLayoutItemLabel(layout)
            title.setText(settings["title"])
            title.setFont(QFont("Times New Roman", 20))
            title.adjustSizeToText()

            layout.addLayoutItem(title)

            title.attemptMove(
                QgsLayoutPoint(10, 8, QgsUnitTypes.LayoutMillimeters)
            )

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
                    QgsLayoutPoint(175, 30, QgsUnitTypes.LayoutMillimeters)
                )

                north_arrow.attemptResize(
                    QgsLayoutSize(20, 20, QgsUnitTypes.LayoutMillimeters)
                )

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
                    QgsLayoutPoint(10, 172, QgsUnitTypes.LayoutMillimeters)
                )

            if settings["show_legend"]:
                legend = QgsLayoutItemLegend(layout)
                legend.setTitle("Legend")
                legend.setLinkedMap(map_item)
                legend.setAutoUpdateModel(True)

                layout.addLayoutItem(legend)

                legend.attemptMove(
                    QgsLayoutPoint(205, 25, QgsUnitTypes.LayoutMillimeters)
                )

                legend.attemptResize(
                    QgsLayoutSize(80, 120, QgsUnitTypes.LayoutMillimeters)
                )

            for page_index in range(settings["page_count"]):
                self.create_title_block(layout, settings, page_index)

            self.iface.openLayoutDesigner(layout)

            QMessageBox.information(
                None,
                "QLayout Designer",
                "The layout has been created successfully and is now open for editing."
            )

        except Exception as e:
            QMessageBox.critical(
                None,
                "QLayout Designer Error",
                str(e)
            )