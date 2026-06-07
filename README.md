# QLayout Designer

QLayout Designer is a QGIS plugin designed to automate the creation of professional map layouts.

The plugin helps GIS professionals, cartographers, engineers and students generate map layouts quickly without manually placing every layout element.

---

## Features

### Automatic Layout Creation

* Create new QGIS print layouts automatically
* Unique layout naming
* A4 Landscape
* A4 Portrait
* A3 Landscape
* A3 Portrait

### Map Elements

* Automatic map frame creation
* Automatic north arrow insertion
* Automatic legend generation
* Automatic graphic scale bar
* Automatic map title

### Multi-Page Layouts

* User-defined number of pages
* Automatic page generation
* Automatic sheet numbering (Blatt)

### Dynamic Title Block

The plugin automatically creates a professional title block including:

* AT/Vh-Bez
* NL/Res
* ONB
* ASB
* Planer
* Datum
* Maßstab
* Bezugssystem
* Blatt

All fields are configurable through the Layout Settings Dialog.

### Layout Settings Dialog

Users can define:

* Map Title
* Cartographic Designer
* Scale
* Layout Size
* Number of Pages
* ONB
* ASB
* SM Number
* Sheet Information
* Legend visibility
* North Arrow visibility
* Scale Bar visibility

### Export

* Layout preview in QGIS Layout Designer
* PDF export support

---

## Installation

1. Download or clone the repository

```bash
git clone https://github.com/nicksorkos/QLayoutDesigner.git
```

2. Copy the plugin folder into:

```text
QGIS3/profiles/default/python/plugins/
```

3. Restart QGIS

4. Enable the plugin from:

```text
Plugins → Manage and Install Plugins
```

---

## Current Version

### v0.5

Implemented:

* Layout Dialog
* Multi-page layouts
* Dynamic title block
* Automatic page numbering
* Dynamic metadata fields
* GitHub integration

---

## Planned Features

### v0.5.1

* Map frame on every page
* North arrow on every page
* Legend on every page
* Scale bar on every page

### v0.6

* Company logo support
* Project name support
* Client information
* Improved title block templates

### v0.7

* Smart Legend
* Automatic basemap filtering
* Dynamic scale bar sizing

### v1.0

* QGIS Plugin Repository release
* Professional engineering templates
* Atlas generation support

---

## Author

Nikolaos Sorkos

GIS | Cartography | QGIS Development

---

## License

MIT License
