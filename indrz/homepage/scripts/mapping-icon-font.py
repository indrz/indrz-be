font_map = [{'name':"icon-h", "description":"exit"}]
import json
with open('wu-picto-index.html') as htmlfile:
    icon_name_list = []
    for line in htmlfile:
        if "<span class=\"icon-" in line:
            print(line)
            nline = line.split('"')[1]
            newby = {"name": nline, "description": ""}
            icon_name_list.append(newby)

    print(icon_name_list)
    with open("font-map.json", "w") as j:
        for x in icon_name_list:
            j.write(json.dumps(x) + "," + "\n")
            print(x)
