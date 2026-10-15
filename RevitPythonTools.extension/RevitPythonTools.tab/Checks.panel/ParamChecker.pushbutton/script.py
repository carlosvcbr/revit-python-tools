# -*- coding: utf-8 -*-
"""Param Checker

Reads a CSV file of required parameters per category and lists every
element whose required parameter is missing or empty.

CSV format (semicolon separated, first line is the header):

    category;parameter
    OST_Walls;Comments
    OST_Doors;Mark

Categories use the BuiltInCategory name (OST_...), so the same CSV works
in any Revit language. The tool is read-only: it never changes the model.

Note: pyRevit runs this with IronPython 2.7 by default, so avoid f-strings
and use "{}".format(...) instead.
"""
import codecs

from pyrevit import DB, forms, revit, script

doc = revit.doc
output = script.get_output()


def read_rules(csv_path):
    """Read the CSV and return {category_name: [parameter names]}.

    Example result:
        {"OST_Walls": ["Comments", "Mark"], "OST_Doors": ["Mark"]}
    """
    rules = {}
    with codecs.open(csv_path, "r", encoding="utf-8-sig") as f:
        lines = f.read().splitlines()

    
    for line in lines[1:]:              # every line except the 1st (header)
        if not line.strip():            # empty line?
            continue                    #   then skip to the next one
        parts = line.split(";")         # "OST_Walls;Mark" -> ["OST_Walls", "Mark"]
        category = parts[0].strip()     # 1st piece, without spaces
        parameter = parts[1].strip()    # 
        rules.setdefault(category, []).append(parameter)
    return rules


def get_elements(category_name):
    """Return all elements (not types) of a category, e.g. "OST_Walls"."""
    bic = getattr(DB.BuiltInCategory, category_name, None)
    if bic is None:
        return None  # unknown category name in the CSV
    return (DB.FilteredElementCollector(doc)
            .OfCategory(bic)
            .WhereElementIsNotElementType()
            .ToElements())


def find_parameter(element, param_name):
    """Look for the parameter on the instance first, then on its type."""
    param = element.LookupParameter(param_name)
    if param is None:
        element_type = doc.GetElement(element.GetTypeId())
        if element_type is not None:
            param = element_type.LookupParameter(param_name)
    return param


def check_value(param):
    """Return "missing", "empty" or None (None means the value is fine)."""
    # TODO 2 (your part):
    #   - if param is None, the element does not have it  -> return "missing"
    #   - if param.StorageType == DB.StorageType.String:
    #         text = param.AsString()
    #         None or only spaces                           -> return "empty"
    #   - for other types (numbers, ids):
    #         if not param.HasValue                         -> return "empty"
    #   - otherwise                                         -> return None
    return None


def main():
    csv_path = forms.pick_file(file_ext="csv", title="Pick the required parameters CSV")
    if not csv_path:
        script.exit()

    rules = read_rules(csv_path)
    if not rules:
        forms.alert("No rules found in the CSV. Check the format.", exitscript=True)

    rows = []
    for category_name, param_names in sorted(rules.items()):
        elements = get_elements(category_name)
        if elements is None:
            output.print_md("**Unknown category in CSV:** {}".format(category_name))
            continue
        for element in elements:
            for param_name in param_names:
                problem = check_value(find_parameter(element, param_name))
                if problem:
                    rows.append([output.linkify(element.Id), category_name,
                                 param_name, problem])

    output.print_md("## Param Checker")
    if rows:
        output.print_table(rows, columns=["Element", "Category", "Parameter", "Problem"])
        output.print_md("**{} problems found.**".format(len(rows)))
    else:
        output.print_md("All required parameters are filled in.")


main()
