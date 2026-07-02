import os
from datetime import datetime

from .layout_dialog import LayoutSettingsDialog

from qgis.PyQt.QtWidgets import QAction, QMessageBox, QFileDialog
from qgis.PyQt.QtGui import QIcon, QFont, QColor
from qgis.PyQt.QtCore import Qt

from qgis.core import (
    QgsApplication,
    QgsProject,
    QgsPrintLayout,
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

    def create_map_item(self, layout, settings, page_index=0):
        page = layout.pageCollection().page(page_index)
        page_y = page.pos().y()

        map_item = QgsLayoutItemMap(layout)
        map_item.setRect(20, 20, 200, 120)
        map_item.setExtent(self.iface.mapCanvas().extent())
        map_item.setScale(settings["scale"])

        layout.addLayoutItem(map_item)

        map_item.attemptMove(
            QgsLayoutPoint(10, page_y + 25, QgsUnitTypes.LayoutMillimeters)
        )

        map_item.attemptResize(
            QgsLayoutSize(190, 135, QgsUnitTypes.LayoutMillimeters)
        )

        return map_item

    def style_frame(self, frame):
        if hasattr(frame, "setStrokeWidth"):
            frame.setStrokeWidth(0.30)
        if hasattr(frame, "setStrokeColor"):
            frame.setStrokeColor(QColor(0, 0, 0))
        elif hasattr(frame, "setBorderColor"):
            frame.setBorderColor(QColor(0, 0, 0))
        if hasattr(frame, "setLineJoinStyle"):
            frame.setLineJoinStyle(Qt.MiterJoin)
        if hasattr(frame, "setFillColor"):
            frame.setFillColor(QColor(255, 255, 255, 0))

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

        self.style_frame(frame)
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

    def add_horizontal_line(self, layout, x, y, width, thickness=0.30):
        line = QgsLayoutItemShape(layout)
        line.setShapeType(QgsLayoutItemShape.Rectangle)
        layout.addLayoutItem(line)

        line.attemptMove(
            QgsLayoutPoint(x, y, QgsUnitTypes.LayoutMillimeters)
        )
        line.attemptResize(
            QgsLayoutSize(width, thickness, QgsUnitTypes.LayoutMillimeters)
        )

        if hasattr(line, "setFillColor"):
            line.setFillColor(QColor(0, 0, 0))
        if hasattr(line, "setStrokeWidth"):
            line.setStrokeWidth(0)

        return line

    def add_vertical_line(self, layout, x, y, height, thickness=0.30):
        line = QgsLayoutItemShape(layout)
        line.setShapeType(QgsLayoutItemShape.Rectangle)
        layout.addLayoutItem(line)

        line.attemptMove(
            QgsLayoutPoint(x, y, QgsUnitTypes.LayoutMillimeters)
        )
        line.attemptResize(
            QgsLayoutSize(thickness, height, QgsUnitTypes.LayoutMillimeters)
        )

        if hasattr(line, "setFillColor"):
            line.setFillColor(QColor(0, 0, 0))
        if hasattr(line, "setStrokeWidth"):
            line.setStrokeWidth(0)

        return line

    def create_info_footer(self, layout, settings, page_index=0):
        page = layout.pageCollection().page(page_index)
        page_x = page.pos().x()
        page_y = page.pos().y()
        page_size = page.pageSize()

        footer_height = 90 if "A3" in settings["layout_size"] else 70
        footer_width = page_size.width() - 20
        footer_y = page_y + page_size.height() - footer_height - 10
        footer_x = page_x + 10

        self.add_frame(layout, footer_x, footer_y, footer_width, footer_height)

        fields = [
            ("Datum:", datetime.now().strftime("%d/%m/%Y")),
            ("Maßstab:", f"1:{settings['scale']:,}".replace(",", ".")),
            ("Planer:", settings["designer"]),
            ("SM Nr:", settings["sm_nr"]),
            ("Bezugssys:", QgsProject.instance().crs().authid()),
            ("ONB:", settings["onb"]),
            ("ASB:", settings["asb"]),
            ("AT/Vh-Bez:", settings["at_vh"]),
            ("NL/Res:", settings["nl_res"]),
        ]

        x = footer_x + 4
        y = footer_y + 4
        for label_text, value_text in fields:
            self.add_frame_label(layout, label_text, x, y, 7, True)
            self.add_frame_label(layout, value_text, x + 34, y, 7)
            y += 7

    def add_line(self, layout, x, y, width, height):
        line = QgsLayoutItemShape(layout)
        line.setShapeType(QgsLayoutItemShape.Rectangle)
        layout.addLayoutItem(line)

        line.attemptMove(
            QgsLayoutPoint(x, y, QgsUnitTypes.LayoutMillimeters)
        )
        line.attemptResize(
            QgsLayoutSize(width, height, QgsUnitTypes.LayoutMillimeters)
        )

        if hasattr(line, "setFillColor"):
            line.setFillColor(QColor(0, 0, 0))
        if hasattr(line, "setStrokeWidth"):
            line.setStrokeWidth(0)
        if hasattr(line, "setStrokeColor"):
            line.setStrokeColor(QColor(0, 0, 0))
        return line

    def create_title_block(self, layout, settings, page_index=0):
        if page_index > 0:
            return

        page = layout.pageCollection().page(page_index)
        page_x = page.pos().x()
        page_y = page.pos().y()
        page_size = page.pageSize()

        block_height = 62
        block_x = page_x + 10
        block_y = page_y + page_size.height() - block_height - 10
        block_width = page_size.width() - 20

        left_width = 55
        right_width = 105
        center_width = block_width - left_width - right_width

        left_x = block_x
        center_x = left_x + left_width
        right_x = center_x + center_width

        self.add_frame(layout, block_x, block_y, block_width, block_height)
        self.add_frame(layout, left_x, block_y, left_width, block_height)
        self.add_frame(layout, center_x, block_y, center_width, block_height)
        self.add_frame(layout, right_x, block_y, right_width, block_height)

        self.add_frame_label(layout, "N", left_x + left_width / 2, block_y + 3, 12, True)

        arrow_path = self.get_north_arrow_path()
        if arrow_path:
            arrow = QgsLayoutItemPicture(layout)
            arrow.setPicturePath(arrow_path)
            layout.addLayoutItem(arrow)
            arrow_width = 24
            arrow_height = 28
            arrow.attemptResize(QgsLayoutSize(arrow_width, arrow_height, QgsUnitTypes.LayoutMillimeters))
            arrow.attemptMove(
                QgsLayoutPoint(
                    left_x + (left_width - arrow_width) / 2,
                    block_y + 18,
                    QgsUnitTypes.LayoutMillimeters
                )
            )

        row_height = 10
        label_left = center_x + 2
        value_left = center_x + 46

        self.add_vertical_line(layout, center_x + 44, block_y, row_height * 3)
        self.add_horizontal_line(layout, center_x, block_y + row_height, center_width)
        self.add_horizontal_line(layout, center_x, block_y + row_height * 2, center_width)
        self.add_horizontal_line(layout, center_x, block_y + row_height * 3, center_width)

        self.add_frame_label(layout, "AT/Vh-Bez:", label_left, block_y + 3, 8, True)
        self.add_frame_label(layout, settings.get("at_vh", ""), value_left, block_y + 3, 8)
        self.add_frame_label(layout, "NL/Res:", label_left, block_y + 3 + row_height, 8, True)
        self.add_frame_label(layout, settings.get("nl_res", ""), value_left, block_y + 3 + row_height, 8)
        self.add_frame_label(layout, "ONB:", label_left, block_y + 3 + row_height * 2, 8, True)
        self.add_frame_label(layout, settings.get("onb", ""), value_left, block_y + 3 + row_height * 2, 8)

        logo_area_y = block_y + row_height * 3
        logo_area_height = block_height - row_height * 3
        self.add_frame(layout, center_x, logo_area_y, center_width, logo_area_height)

        logo_path = settings.get("logo_path", "")
        if logo_path and os.path.exists(logo_path):
            logo_item = QgsLayoutItemPicture(layout)
            logo_item.setPicturePath(logo_path)
            layout.addLayoutItem(logo_item)
            logo_width = center_width - 10
            logo_height = logo_area_height - 8
            if logo_width > 0 and logo_height > 0:
                logo_item.attemptResize(QgsLayoutSize(logo_width, logo_height, QgsUnitTypes.LayoutMillimeters))
                logo_item.attemptMove(
                    QgsLayoutPoint(center_x + 5, logo_area_y + 4, QgsUnitTypes.LayoutMillimeters)
                )

        right_label_width = 42
        right_value_left = right_x + right_label_width + 2
        right_row_height = 10

        self.add_vertical_line(layout, right_x + right_label_width, block_y, right_row_height * 6)
        self.add_horizontal_line(layout, right_x, block_y + right_row_height, right_width)
        self.add_horizontal_line(layout, right_x, block_y + right_row_height * 2, right_width)
        self.add_horizontal_line(layout, right_x, block_y + right_row_height * 3, right_width)
        self.add_horizontal_line(layout, right_x, block_y + right_row_height * 4, right_width)
        self.add_horizontal_line(layout, right_x, block_y + right_row_height * 5, right_width)
        self.add_horizontal_line(layout, right_x, block_y + right_row_height * 6, right_width)

        self.add_frame_label(layout, "AsB:", right_x + 2, block_y + 3, 8, True)
        self.add_frame_label(layout, settings.get("asb", ""), right_value_left, block_y + 3, 8)
        self.add_frame_label(layout, "Planer:", right_x + 2, block_y + 3 + right_row_height, 8, True)
        self.add_frame_label(layout, settings.get("planer", ""), right_value_left, block_y + 3 + right_row_height, 8)
        self.add_frame_label(layout, "Datum:", right_x + 2, block_y + 3 + right_row_height * 2, 8, True)
        self.add_frame_label(layout, settings.get("datum", "") or datetime.now().strftime("%d/%m/%Y"), right_value_left, block_y + 3 + right_row_height * 2, 8)
        self.add_frame_label(layout, "Bezugssys:", right_x + 2, block_y + 3 + right_row_height * 3, 8, True)
        self.add_frame_label(layout, settings.get("coordinate_system", "") or QgsProject.instance().crs().authid(), right_value_left, block_y + 3 + right_row_height * 3, 8)
        self.add_frame_label(layout, "Maßstab:", right_x + 2, block_y + 3 + right_row_height * 4, 8, True)
        self.add_frame_label(layout, f"1:{settings.get('scale', 0):,}".replace(",", "."), right_value_left, block_y + 3 + right_row_height * 4, 8)
        self.add_frame_label(layout, "Blatt:", right_x + 2, block_y + 3 + right_row_height * 5, 8, True)
        self.add_frame_label(layout, settings.get("sheet", str(page_index + 1)), right_value_left, block_y + 3 + right_row_height * 5, 8)

    def create_client_image(self, layout, settings, page_index=0):
        return None

    def get_north_arrow_path(self):
        plugin_dir = os.path.dirname(__file__)
        candidates = [
            os.path.join(plugin_dir, "north_arrow.png"),
            os.path.join(plugin_dir, "north_arrow.svg"),
            os.path.join(QgsApplication.svgPaths()[0], "arrows", "NorthArrow_01.svg"),
            os.path.join(QgsApplication.svgPaths()[0], "arrows", "NorthArrow_02.svg"),
            os.path.join(QgsApplication.svgPaths()[0], "arrows", "north_arrow.svg"),
            os.path.join(QgsApplication.svgPaths()[0], "north_arrows", "NorthArrow_01.svg"),
        ]

        for path in candidates:
            if os.path.exists(path):
                return path
        return None

    def create_north_arrow(self, layout, page_index=0):
        page = layout.pageCollection().page(page_index)
        page_y = page.pos().y()

        north_arrow = QgsLayoutItemPicture(layout)
        north_arrow_path = self.get_north_arrow_path()

        if north_arrow_path:
            north_arrow.setPicturePath(north_arrow_path)

        layout.addLayoutItem(north_arrow)

        north_arrow.attemptMove(
            QgsLayoutPoint(21, page_y + 183, QgsUnitTypes.LayoutMillimeters)
        )

        north_arrow.attemptResize(
            QgsLayoutSize(22, 28, QgsUnitTypes.LayoutMillimeters)
        )

        north_arrow.setZValue(100)
        return north_arrow

    def create_scale_bar(self, layout, map_item, page_index=0):
        page = layout.pageCollection().page(page_index)
        page_y = page.pos().y()

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
            QgsLayoutPoint(10, page_y + 172, QgsUnitTypes.LayoutMillimeters)
        )

        return scale_bar

    def create_legend(self, layout, map_item, settings, page_index=0):
        if page_index is None:
            page_index = 0

        page_count = layout.pageCollection().pageCount()
        if page_index >= page_count or page_index < 0:
            page_index = 0

        page = layout.pageCollection().page(page_index)
        page_y = page.pos().y()

        legend = QgsLayoutItemLegend(layout)
        legend.setTitle("Legend")
        legend.setLinkedMap(map_item)

        legend.setAutoUpdateModel(True)

        layout.addLayoutItem(legend)

        legend.attemptMove(
            QgsLayoutPoint(205, page_y + 25, QgsUnitTypes.LayoutMillimeters)
        )

        legend.attemptResize(
            QgsLayoutSize(80, 120, QgsUnitTypes.LayoutMillimeters)
        )

        return legend

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

            map_pages = []
            legend_page = 1 if settings["page_count"] > 1 and settings["show_legend"] else 0
            for page_index in range(settings["page_count"]):
                if settings["page_count"] > 1 and page_index == legend_page:
                    continue
                map_item = self.create_map_item(layout, settings, page_index)
                map_pages.append((page_index, map_item))

            if settings["show_scale_bar"]:
                for page_index, map_item in map_pages:
                    self.create_scale_bar(layout, map_item, page_index)

            if settings["show_legend"]:
                legend_map_item = map_pages[0][1] if map_pages else None
                if legend_map_item is not None:
                    self.create_legend(layout, legend_map_item, settings, legend_page)

            for page_index in range(settings["page_count"]):
                self.create_title_block(layout, settings, page_index)

            if settings["show_north"]:
                for page_index, _ in map_pages:
                    self.create_north_arrow(layout, page_index)

            if settings.get("open_designer", False):
                self.iface.openLayoutDesigner(layout)

            QMessageBox.information(
                None,
                "QLayout Designer",
                "The layout has been created successfully."
            )

        except Exception as e:
            QMessageBox.critical(
                None,
                "QLayout Designer Error",
                str(e)
            )