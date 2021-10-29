from os import error
from re import S
import re
from template_out import generate_importable_excel
from swagger import generate_ref_excel
import urllib


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


SWAGGER_HOSTED_IP = "<ADD_YOUR_IP_HERE>"


def generate_pair(url, module, repo_name):
    black_list_paths = ["/actuator", "/hystrix", "/error"]

    sw_url = urllib.request.urlopen(url)

    generate_ref_excel(
        module, sw_url.read().decode(), black_list_paths, out_file_name=repo_name
    )

    sw_url2 = urllib.request.urlopen(url)
    generate_importable_excel(
        module, sw_url2.read().decode(), black_list_paths, out_file_name=repo_name
    )


flow = input("BULK or SINGLE? (B/S):")

if flow == "S":

    module = input("Enter the module name/export file name:")
    url = input("Enter the swagger url:")
    generate_pair(url, module)
    print(f"{bcolors.OKGREEN}Finished !{bcolors.ENDC}")
else:
    try:
        with open("bulk.in", "r") as txt_file:
            for line in txt_file.readlines():
                line_arr = line.replace("\n", "").split(",")
                module_name = line_arr[1]
                url_module_name = line_arr[0]

                print(
                    "Genrateing... ",
                    module_name,
                    ">>",
                    "http://{}/{}/v2/api-docs".format(
                        SWAGGER_HOSTED_IP, url_module_name
                    ),
                )

                generate_pair(
                    url="http://{}/{}/v2/api-docs".format(
                        SWAGGER_HOSTED_IP, url_module_name
                    ),
                    module=module_name,
                    repo_name=url_module_name,
                )

        print(f"{bcolors.OKGREEN}Finished !{bcolors.ENDC}")
    except (error):
        print(f"{bcolors.WARNING}Error:{error} {bcolors.ENDC}")
