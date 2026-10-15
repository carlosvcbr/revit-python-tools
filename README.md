# revit-python-tools

Python tools that automate Revit and BIM quality checks, built as a
[pyRevit](https://github.com/pyrevitlabs/pyRevit) extension.

## Tools

| Tool | What it does | Changes the model? |
|---|---|---|
| **Param Checker** | Reads a CSV of required parameters per category and lists every element where a required parameter is missing or empty. Click an element id in the report to select it in Revit. | No |

More tools will be added over time.

## Installation

1. Install [pyRevit](https://github.com/pyrevitlabs/pyRevit/releases).
2. Clone or download this repository.
3. In Revit: **pyRevit tab > Settings > Custom Extension Directories**, add the
   folder of this repository, then click **Reload**.
4. A new **Python Tools** tab appears in the Revit ribbon.

## Param Checker

1. Write a CSV with the parameters each category must have
   (see [`examples/required_params.csv`](examples/required_params.csv)):

   ```
   category;parameter
   OST_Walls;Comments
   OST_Doors;Mark
   ```

   Categories use Revit's `BuiltInCategory` names (`OST_...`), so the same
   file works in any Revit language. Parameter names must match the names
   shown in your Revit.

2. Click **Param Checker** and pick the CSV.
3. The report lists each element, the parameter and the problem
   (`missing` = the element does not have the parameter, `empty` = it has no value).

## Requirements

- Revit 2022 or newer
- pyRevit 4.8 or newer

## License

[MIT](LICENSE)
