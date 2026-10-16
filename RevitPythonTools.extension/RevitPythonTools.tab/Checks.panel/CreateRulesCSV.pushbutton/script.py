# -*- coding: utf-8 -*-
"""Create Rules CSV

Lists every model category that has elements in the open model and saves
a CSV template for Param Checker. Fill in the "parameter" column, then
run Param Checker with the file.

CSV columns (semicolon separated):

    category;parameter;name;elements
    OST_Walls;;Walls;124

- category: BuiltInCategory name, the same in any Revit language
- parameter: left empty for you to fill in (one parameter per line;
  copy the line to require more than one parameter)
- name, elements: only for information, Param Checker ignores them

The tool is read-only: it never changes the model.
"""
import codecs

from System import Enum

from pyrevit import DB, forms, revit, script

doc = revit.doc
output = script.get_output()


def category_code(category):
    """Return the BuiltInCategory name of a category, e.g. "OST_Walls"."""
    id_value = getattr(category.Id, "Value", None)  # Revit 2024+
    if id_value is None:
        id_value = category.Id.IntegerValue         # Revit 2023 and older
    return str(Enum.ToObject(DB.BuiltInCategory, id_value))


def count_categories():
    """Return {category code: [display name, number of elements]}."""
    counts = {}
    elements = (DB.FilteredElementCollector(doc)
                .WhereElementIsNotElementType()
                .ToElements())
    for element in elements:
        category = element.Category
        if category is None or category.CategoryType != DB.CategoryType.Model:
            continue  # skip elements without a category and annotations
        code = category_code(category)
        if not code.startswith("OST_"):
            continue  # skip categories that have no built-in name
        entry = counts.setdefault(code, [category.Name, 0])
        entry[1] += 1
    return counts


def main():
    counts = count_categories()
    if not counts:
        forms.alert("No model elements found.", exitscript=True)

    csv_path = forms.save_file(file_ext="csv", default_name="required_params")
    if not csv_path:
        script.exit()

    with codecs.open(csv_path, "w", encoding="utf-8-sig") as f:
        f.write("category;parameter;name;elements\n")
        for code, (name, number) in sorted(counts.items()):
            # TODO (your part): build one line of the CSV.
            #   It must look like:  OST_Walls;;Walls;124
            #   The format below already has the 4 columns; fill in the blank
            #   with the variable that holds the category code.
            row = "{};;{};{}\n".format(code, name, number)  # <- YOUR TURN
            f.write(row)

    output.print_md("## Create Rules CSV")
    output.print_md("Saved **{}** categories to `{}`.".format(len(counts), csv_path))
    output.print_md("Next: open the file, fill in the **parameter** column "
                    "and run **Param Checker**.")


main()
