import json
import urllib.request, json
from reader import get_endpoints_with_permissions
import os
import xlsxwriter


def generate_importable_excel(moduleName, swaggerUrl, black_list_paths, out_file_name):
    out_file_name = "./import/" + out_file_name + ".xlsx"
    if os.path.exists(out_file_name):
        os.remove(out_file_name)

    workbook = xlsxwriter.Workbook(out_file_name)
    worksheet = workbook.add_worksheet()

    data = json.loads(swaggerUrl)

    base_path = str(data["basePath"]).replace("/", "")  # base_path / repo name
    paths = get_endpoints_with_permissions(
        data, black_list_paths=black_list_paths, base_path=base_path, prefix=moduleName
    )
    col = 0
    row = 1
    worksheet.write(row, col, "Permission")
    worksheet.write(row, col + 1, "Api Url")

    prev_key = "//"
    is_colored = True
    for key in paths:

        permissions = paths[key]
        for v in permissions:
            if str(key).startswith("/" + str(prev_key).split("/")[1]):
                if is_colored:
                    cf = workbook.add_format({"bg_color": "#CCFFFF"})
                else:
                    cf = workbook.add_format({"bg_color": "white"})

            else:
                # a controller change
                is_colored = not is_colored
                if is_colored:
                    cf = workbook.add_format({"bg_color": "#CCFFFF"})
                else:
                    cf = workbook.add_format({"bg_color": "white"})
            worksheet.write(row, col, v, cf)
            worksheet.write(row, col + 1, key, cf)
            prev_key = key

            row += 1

    workbook.close()
