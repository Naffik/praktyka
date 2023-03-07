import json
import pprint
import tkinter
import tkinter.messagebox
import customtkinter
import xml.etree.ElementTree as ET
import xmltodict


def json_extract(obj: object, key: str) -> str:
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
    return values


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


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
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

        self.sidebar_textbox_label = customtkinter.CTkLabel(self.sidebar_frame, text="Search",
                                                            font=customtkinter.CTkFont(size=16, weight="bold"))
        self.sidebar_textbox_label.grid(row=4, column=0, padx=20, pady=10, sticky="sew")
        self.sidebar_textbox = customtkinter.CTkTextbox(self.sidebar_frame, width=160, height=60)
        self.sidebar_textbox.grid(row=5, column=0, padx=20, pady=10, sticky="n")
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Search",
                                                        command=self.search)
        self.sidebar_button_3.grid(row=6, column=0, padx=20, pady=10)

        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Save JSON file",
                                                        command=self.save)
        self.sidebar_button_3.grid(row=7, column=0, padx=20, pady=10)

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=8, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                                       values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 10))

        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=10, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                               values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=11, column=0, padx=20, pady=(10, 20))

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
        print(self.json_data)

    def search(self):
        self.textbox.delete("0.0", "end")
        with open("data.json", "r") as json_file:
            json_data = json.load(json_file)
        key = self.sidebar_textbox.get("0.0", "end")
        print(key.strip())
        self.data = json_extract(json_data, key.strip())
        self.textbox.insert("0.0", json.dumps(self.data, indent=4))
        # with open("data_search_1.json", "w") as outfile:
        #     json.dump(data, outfile)

    def save(self):
        filetypes = (('JSON files', '*.json'),)

        filename = customtkinter.filedialog.asksaveasfilename(
            title='Save a file',
            initialdir='/',
            filetypes=filetypes,
            defaultextension="*.json")
        if filename:
            with open(filename, "w") as file:
                json.dump(self.json_data, file)


if __name__ == "__main__":
    app = App()
    app.mainloop()
