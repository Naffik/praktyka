import json


class JSONTemplate:
    def __init__(self, template_file: str):
        with open(template_file, 'r') as file:
            self.template = json.load(file)

    def add_data(self, data_file: str):
        with open(data_file, 'r') as file:
            data = json.load(file)
        self.template.update(data)

    def delete_data(self, key: str):
        if key in self.template:
            del self.template[key]

    def edit_data(self, key: str, value: str):
        if key in self.template:
            self.template[key] = value

    def save_template(self, filename: str):
        with open(filename, 'w') as file:
            json.dump(self.template, file, indent=4)





