# QLayout Designer

**QLayout Designer** is a QGIS plugin that automatically creates professional map layouts with a structured title block, map frame, legend, scale bar, north arrow, logo support, and multi-page layout generation.

The plugin is designed for GIS professionals, engineers, cartographers, and mapping workflows where repeated production of standardized layouts is required.

---

## Features

* Automatic QGIS layout creation
* Multi-page layout support
* Map frame generated from the current QGIS map canvas
* Custom layout size selection:

  * A4 Landscape
  * A4 Portrait
  * A3 Landscape
  * A3 Portrait
* Custom map scale selection:

  * 1:1.000
  * 1:2.500
  * 1:5.000
  * 1:10.000
  * 1:25.000
  * 1:50.000
  * 1:100.000
  * 1:250.000
* Dynamic title block
* Logo support
* North arrow support
* Graphic scale bar
* Legend support
* Smart Legend option for hiding common basemap layers
* Automatic page numbering
* Optional PDF export
* Option to open the layout directly in QGIS Layout Designer

---

## Title Block Information

The plugin generates a structured title block with dynamic fields such as:

* AT/Vh-Bez
* NL/Res
* ONB
* ASB
* Planer
* Datum
* SM Nr
* Bezugssys
* Maßstab
* Blatt
* Company
* Project
* Client

These fields are entered through the plugin dialog and automatically placed inside the generated layout.



## Installation

### Manual Installation

1. Download or clone this repository.

2. Copy the plugin folder:

```text
QLayoutDesigner
```

to your QGIS plugins directory.

On Windows, this is usually:

```text
C:\Users\<YourUsername>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\
```

3. Restart QGIS.

4. Go to:

```text
Plugins → Manage and Install Plugins
```

5. Enable:

```text
QLayout Designer
```

6. The plugin will appear in the QGIS toolbar and under:

```text
Plugins → QLayout Designer → Create Automatic Layout
```

---

## Required Plugin Files

The plugin folder should contain:

```text
QLayoutDesigner/
├── __init__.py
├── metadata.txt
├── Q_Layout_Designer.py
├── layout_dialog.py
├── icon.png
├── north_arrow.png
├── README.md
├── CHANGELOG.md
├── LICENSE
└── .gitignore
```

---

## Files That Should Not Be Included

The following files should not be committed or included in the release package:

```text
__pycache__/
*.pyc
*.pyo
*.pyd
.vscode/
```

Recommended `.gitignore`:

```gitignore
__pycache__/
*.pyc
*.pyo
*.pyd
.vscode/
```

---

## Usage

1. Open a QGIS project.
2. Load the layers you want to map.
3. Zoom the QGIS map canvas to the desired area.
4. Click:

```text
Create Automatic Layout
```

5. Fill in the layout settings:

   * Map title
   * Designer
   * Company
   * Project
   * Client
   * Logo
   * AT/Vh-Bez
   * NL/Res
   * ONB
   * ASB
   * SM Nr
   * Scale
   * Layout size
   * Number of pages

6. Choose which layout elements to include:

   * Legend
   * Smart Legend
   * North Arrow
   * Graphic Scale
   * Open Layout Designer
   * Export PDF Automatically

7. Press **OK**.

The plugin will generate the layout automatically.

---

## Logo Support

The user can select a logo image from the plugin dialog.

Supported formats:

```text
.png
.jpg
.jpeg
.svg
```

The logo is placed inside the title block and repeated on every generated page.

---

## North Arrow

The plugin uses a local north arrow image named:

```text
north_arrow.png
```

This file should be placed inside the plugin folder.

If the file is missing, the plugin attempts to use available QGIS default north arrow SVG files.

---

## PDF Export

The plugin includes optional PDF export.

If the user enables:

```text
Export PDF Automatically
```

the plugin asks for a PDF save location and exports the generated layout.

If the user enables:

```text
Open Layout Designer
```

the generated layout opens directly inside QGIS for further manual editing.

Both options can be enabled at the same time.

---

## Current Version

```text
Version: 1.0.0
```

---

## Version 1.0.0 Highlights

* Stable automatic layout generation
* Multi-page support
* Dynamic title block
* Company, Project, and Client fields
* Logo support
* North arrow support
* Graphic scale bar
* Legend support
* Smart Legend option
* Optional PDF export
* Editable layout preview in QGIS Layout Designer

---

## Development Status

This plugin is currently in active development.

Planned future improvements may include:

* Template system
* Custom title block templates
* Better legend customization
* Custom logo positioning
* Custom map frame sizes
* Export presets
* Support for different engineering/cartographic layout standards

---

## Suggested Future Templates

Possible future layout templates:

* Generic GIS Map
* FTTH Network Design
* Road Network Mapping
* Utility Mapping
* Cadastre Mapping
* Environmental Mapping

---

## Requirements

* QGIS 3.x
* Python 3
* PyQGIS

The plugin is developed for QGIS 3 and uses the QGIS Layout API.

---

## Repository

GitHub repository:

```text
https://github.com/nicksorkos/QLayoutDesigner
```

---

## Author

**Nikolaos Sorkos**

GIS / Geoinformatics
QGIS, Cartography, GIS Automation

---

## License

This project is released under the MIT License.

See the `LICENSE` file for more information.

---

## Disclaimer

This plugin is provided as-is.

Users should always check generated layouts before final publication or professional submission.

The plugin is intended to assist layout creation, but final cartographic validation remains the responsibility of the user.

---

## Screenshots

Screenshots can be added here in future versions.

Suggested examples:

```text
docs/screenshots/plugin_dialog.png
docs/screenshots/generated_layout.png
docs/screenshots/title_block.png
```

Example Markdown format:

```markdown
![Plugin Dialog](docs/screenshots/plugin_dialog.png)

![Generated Layout](docs/screenshots/generated_layout.png)

![Title Block](docs/screenshots/title_block.png)
```
