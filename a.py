import json


command_json = "command backap.json"
command_json_result = "command.json"
data = {}
data_result = []
with open(command_json, 'r') as f:
    data: dict = json.load(f)


def rec(data):
    ready_arr = []
    for i in data:
        if data[i] != "N":
            if "_c_addon" in i or "c_all" in i:
                continue
            next = []
            next_always = False
            compile_function = ""
            addon_with_compile_function = []
            if isinstance(data[i], str):
                next_always = True
                compile_function = data[i]
                if f"{i}_c_addon" in data:
                    addon_with_compile_function = rec(data[f"{i}_c_addon"])

                    if "c_all" in data[f"{i}_c_addon"]:
                        if isinstance(data[f"{i}_c_addon"]["c_all"], str):
                            next = data[f"{i}_c_addon"]["c_all"]
                        else:
                            next = rec(data[f"{i}_c_addon"]["c_all"])

            else:
                next = rec(data[i])

            ready_arr.append({
                "c": i.split(" ")[0],
                "h": " ".join(i.split(" ")[1:]).replace("[", "").replace("]", ""),
                "cf": compile_function,
                "awcf": addon_with_compile_function,
                "na": next_always,
                "n": next
            })
        else:
            next = []

            addon_with_compile_function = []

            next_always = False

            ready_arr.append({
                "c": i.split(" ")[0],
                "h": " ".join(i.split(" ")[1:]).replace("[", "").replace("]", ""),
                "cf": "",
                "awcf": addon_with_compile_function,
                "na": next_always,
                "n": next
            })
    return ready_arr


with open(command_json_result, 'w') as f:
    f.write(json.dumps(rec(data)))
