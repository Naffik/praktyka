import json
import objectpath
import customtkinter
import xmltodict


def json_extract(obj: object, key: str) -> dict:
    """Recursively fetch values from nested JSON."""
    arr = []

    def extract(obj: object, arr: list, key: str) -> str:
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
    return dict(values)


class JSONTemplate:

    def __init__(self, template_file: str):
        with open(template_file, 'r') as file:
            self.template = json.load(file)

    def add_data(self, data_file: str, search_key: str):
        with open(data_file, 'r') as file:
            new_data = json.load(file)
        # print(search_key)
        # print(self.template)

        if add_data_to_json(self.template, search_key, new_data):
            print(f"Dodano nowe dane do klucza '{search_key}' w pliku '{self.template}'.")
        else:
            # jeśli wartość nie została znaleziona, wypisz stosowny komunikat
            print(f"Nie znaleziono klucza '{search_key}' w pliku '{self.template}'.")

    def delete_data(self, key: str):
        if key in self.template:
            del self.template[key]

    def edit_data(self, key: str, value: str):
        if key in self.template:
            self.template[key] = value

    def save_template(self, filename: str):
        with open(filename, 'w') as file:
            json.dump(self.template, file, indent=4)


def add_data_to_json(json_data, key_to_find, new_data):
    # print(json_data)
    # json_data = json.dumps(json_data)
    # print(json_data)
    if isinstance(json_data, dict):
        for k, v in json_data.items():
            if k == key_to_find:
                for key, value in new_data.items():
                    # print(json_data[key_to_find][key])
                    # json_data.pop(key_to_find)
                    print(value)
                    # json_data.update(value)
                    json_data[key_to_find] = value
                # json_data[k] = new_data
                # print(json_data[k], end="\n")
                return True
            else:
                if add_data_to_json(v, key_to_find, new_data):
                    return True
    elif isinstance(json_data, list):
        for i, v in enumerate(json_data):
            if add_data_to_json(v, key_to_find, new_data):
                return True
    return False


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.key = None
        self.template = None
        self.data = None
        self.data_dict = None
        self.json_data = None
        self.title("XML to JSON converter")
        self.geometry(f"{1280}x{720}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="XML to Json",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Open XML file",
                                                        command=self.read_xml_file)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_1_label = customtkinter.CTkLabel(self.sidebar_frame, text="", anchor="w", width=180)
        self.sidebar_button_1_label.grid(row=2, column=0, padx=20, pady=(10, 0))

        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Convert to JSON",
                                                        command=self.convert_to_json)
        self.sidebar_button_2.grid(row=3, column=0, padx=20, pady=10)

        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Open JSON template file",
                                                        command=self.load_template)
        self.sidebar_button_3.grid(row=4, column=0, padx=20, pady=10)
        self.sidebar_button_3_label = customtkinter.CTkLabel(self.sidebar_frame, text="", anchor="w", width=180)
        self.sidebar_button_3_label.grid(row=5, column=0, padx=20, pady=(10, 0))

        self.sidebar_textbox_label = customtkinter.CTkLabel(self.sidebar_frame, text="Search",
                                                            font=customtkinter.CTkFont(size=16, weight="bold"))
        self.sidebar_textbox_label.grid(row=6, column=0, padx=20, pady=10, sticky="sew")
        self.sidebar_textbox = customtkinter.CTkTextbox(self.sidebar_frame, width=160, height=60)
        self.sidebar_textbox.grid(row=7, column=0, padx=20, pady=10, sticky="n")
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Search",
                                                        command=self.search)
        self.sidebar_button_3.grid(row=8, column=0, padx=20, pady=10)

        self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_frame, text="Add to template",
                                                        command=self.add_to_template)

        self.sidebar_button_4.grid(row=9, column=0, padx=20, pady=10)
        self.sidebar_button_5 = customtkinter.CTkButton(self.sidebar_frame, text="Save JSON file",
                                                        command=self.save)
        self.sidebar_button_5.grid(row=10, column=0, padx=20, pady=10)

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=11, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                                       values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=12, column=0, padx=20, pady=(10, 10))

        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=13, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                               values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=14, column=0, padx=20, pady=(10, 20))

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=250, height=680, activate_scrollbars=True)
        self.textbox.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.sidebar_frame_2 = customtkinter.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame_2.grid(row=0, column=3, rowspan=4, sticky="nsew")
        self.sidebar_frame_2.grid_rowconfigure(4, weight=1)
        self.logo_label_2 = customtkinter.CTkLabel(self.sidebar_frame_2, text="XML to Json",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def read_xml_file(self):
        filetypes = (('XML files', '*.XML'), )

        filename = customtkinter.filedialog.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)
        f = filename.split("/")
        self.sidebar_button_1_label.configure(text=f[-1])

        with open(filename, "r") as xml_file:
            self.data_dict = xmltodict.parse(xml_file.read())

    def convert_to_json(self):
        self.json_data = self.data_dict
        self.textbox.insert("0.0", json.dumps(self.data_dict, indent=4))
        # print(self.json_data)

    def search(self):
        self.textbox.delete("0.0", "end")
        with open("data.json", "r") as json_file:
            json_data = json.load(json_file)
        self.key = self.sidebar_textbox.get("0.0", "end").strip()
        # print(self.key.strip())
        print(json_extract(json_data, self.key.strip()))
        self.data = json_extract(json_data, self.key.strip())
        self.textbox.insert("0.0", json.dumps(self.data, indent=4))
        with open("search.json", "w") as outfile:
            json.dump(self.data, outfile, indent=4)

    def save(self):
        filetypes = (('JSON files', '*.json'),)

        filename = customtkinter.filedialog.asksaveasfilename(
            title='Save a file',
            initialdir='/',
            filetypes=filetypes,
            defaultextension="*.json")
        if filename:
            self.template.save_template(filename)

    def load_template(self):
        filetypes = (('JSON files', '*.json'),)

        filename = customtkinter.filedialog.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)
        f = filename.split("/")
        self.sidebar_button_3_label.configure(text=f[-1])

        self.template = JSONTemplate(filename)

    def add_to_template(self):
        self.template.add_data("search.json", self.key)


if __name__ == "__main__":
    app = App()
    app.mainloop()
