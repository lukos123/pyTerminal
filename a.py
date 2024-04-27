import json


command_json = "command_linuks.json"
command_json_result = "command_linuks.json"
data = {}
data_result = []
with open(command_json, 'r') as f:
    data: dict = json.load(f)


def rec(data):
    ready_arr = []
    for i in data:
        if data[i] != "N":
            if "_c_addon" in i:
                continue
            next = []
            next_always = False
            compile_function = ""
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
            addon_with_compile_function = []

            ready_arr.append({
                "command": i.split(" ")[0],
                "help": " ".join(i.split(" ")[1:]).replace("[", "").replace("]", ""),
                "compile_function": compile_function,
                "addon_with_compile_function": addon_with_compile_function,
                "next_always": next_always,
                "next": next
            })
        else:
            next = []

            addon_with_compile_function = []

            next_always = False

            ready_arr.append({
                "command": i.split(" ")[0],
                "help": " ".join(i.split(" ")[1:]).replace("[", "").replace("]", ""),
                "compile_function": "",
                "addon_with_compile_function": addon_with_compile_function,
                "next_always": next_always,
                "next": next
            })
    return ready_arr


with open(command_json_result, 'w') as f:
    f.write(json.dumps(rec(data)))
