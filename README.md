# QLayoutDesigner

Automatic Map Layout Generator Plugin for QGIS

## Overview

QLayoutDesigner is a QGIS plugin designed to automate the creation of professional cartographic layouts. The plugin generates a ready-to-use map layout directly from the active QGIS project, reducing the time required for repetitive cartographic tasks.

The current version automatically creates:

* Main map frame
* Graphic scale bar
* Numeric scale display
* Map grid
* Dynamic legend
* Coordinate Reference System (CRS) information
* Date information
* Cartographic designer information

## Features

### Automatic Layout Creation

Generate a complete map layout with a single click.

### Dynamic Legend

The legend is automatically populated using the layers currently loaded in the QGIS project.

### Automatic Scale

The plugin automatically creates:

* Numeric scale (e.g. 1:250.000)
* Graphic scale bar

### North Arrow

A north arrow is automatically inserted into the layout.

### Grid Generation

Map grids and coordinate annotations can be generated automatically.

### Cartographic Metadata

The layout includes:

* CRS information
* Date of creation
* Cartographic designer details

## Requirements

* QGIS 3.34 or newer
* Python 3.x

## Installation

1. Download the repository.
2. Copy the plugin folder into:

```text
C:\Users\<USERNAME>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\
```

3. Open QGIS.
4. Enable the plugin from:

Plugins → Manage and Install Plugins

5. Activate QLayoutDesigner.

## Usage

1. Open a QGIS project.
2. Load the desired layers.
3. Click the QLayoutDesigner button.
4. A complete layout will be automatically generated.

## Current Version

Version: 0.2

## Roadmap

Future versions will include:

* Automatic PDF export
* Custom layout templates
* Company branding support
* Multiple layout formats (A4, A3, A2, A1)
* Advanced legend management
* Automatic map title generation
* Batch layout creation

## Author

Nikolaos Sorkos

MSc GIS Candidate

Department of Geography

## License

This project is released under the GNU General Public License (GPL v3).

## Acknowledgements

Developed using the QGIS Python API (PyQGIS).

QGIS® is a registered trademark of the QGIS Project.
