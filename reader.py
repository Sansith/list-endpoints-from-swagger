def get_endpoints_with_permissions(json_data, black_list_paths, prefix, base_path):
    result_dic = {}
    paths = json_data["paths"]
    # col = 0
    # row = 0
    print("Base Path/Repo:", base_path)

    print("Working...")

    for key in paths:
        # remove the black listed endpoints
        if checkInBlackList(key, black_list_paths):
            continue
        # write endpoint

        # worksheet.write(row, col, key)

        # print(key, end=" ")
        verbs = []
        pathObj = paths[key]

        # this will get the endpoint methods [eg:POST,GET,PUT...]
        for v in pathObj:

            summary = str(
                "{}:{}:{}:{}".format(prefix, base_path, str(pathObj[v]["summary"]), v)
            )

            # worksheet.write(row, col + 1, summary)
            verbs.append(summary)
            # row += len(verbs)

        result_dic[key] = verbs

    return result_dic


def checkInBlackList(checkKey, black_list_paths):
    for item in black_list_paths:
        if str(checkKey).startswith(item):
            return True
    return False
