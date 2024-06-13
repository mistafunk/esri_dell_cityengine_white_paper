# Esri/Dell Collaboration on CityEngine white paper

Repo with CityEngine sample projects

## General Usage

1. Clone repo
1. Optional: create new CityEngine workspace
1. Use menu item `File -> Import/Link Project Folder into workspace...`
   * Select the desired project directory in the repo
   * Disable `Copy project into workspace` (this keeps the link to the git repo)
1. The project is now linked into your workspace

## Project: Scripted Scene Creation

1. Open `scripts/create_wizard_scene.py`
1. Hit F9, this runs the script and creates `scenes/wizard_scene.cej`

Note: The script automatically generates the building models (see `ce.generateModels`).
