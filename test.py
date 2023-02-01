import json

import xmltodict

with open('data.xml', 'r') as my_file:
    obj = xmltodict.parse(my_file.read())

with open("data.json", "w") as outfile:
    json.dump(obj, outfile)

with open("data.json", "r") as json_file:
    json_data = json.load(json_file)

# json_data = json.dumps(data_dict, indent=4)
# # print(json_data)
# print(json_data)


def get_keys(obj, prev_key=None, keys=[]):
    if not isinstance(obj, dict):
        keys.append(prev_key)
        return keys
    new_keys = []
    for k, v in obj.items():
        if prev_key is not None:
            new_key = "{}.{}".format(prev_key, k)
        else:
            new_key = k
        new_keys.extend(get_keys(v, new_key, []))
    return new_keys


def json_extract(obj, key):
    """Recursively fetch values from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    if k == key:
                        arr.append((k, v))
                    extract(v, arr, key)
                elif k == key:
                    arr.append((k, v))
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    return values


print(type(json_data))
data = json_extract(json_data, "clusters")
print(data)
with open("data_search.json", "w") as outfile:
    json.dump(data, outfile)






    # # data = json.dumps(json_data)
    # for key in json_data.items():
    #     print(key, end='\n')

# keyVal = "structure"
# if keyVal in json_data:
#     print("%s is found in JSON data" % keyVal)
#     print("The value of", keyVal, "is", json_data[keyVal])
