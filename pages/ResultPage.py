from tkinter import Button, Frame, Label
from dotenv import load_dotenv
from os import getenv, path, pardir
from PIL import ImageTk, Image
from io import BytesIO
from math import floor
from json import dump
from sqlite3 import connect
import requests

load_dotenv()

class ResultPage(Frame):

    def __init__(self, master=None, controller=None):

        super().__init__(master=master)
        self.master = master
        self.god = controller

        self.db_path = path.join(path.dirname(__file__), pardir, 'savedspecies.db')

        self.backTo = ''
        self.data_cache = ''

        self.button_holder = Frame(master=self)
        self.button_holder.pack()

        self.back_button = Button(master=self.button_holder, text="Back", fg="#ffffff", highlightbackground="#DB8D22", width=15, font=("Avenir Next", "14"), command=lambda: self.goBack())
        self.back_button.grid(row=0, column=0, padx=10, pady=30, ipadx=5, ipady=2)

        self.save_button = Button(master=self.button_holder, text="Save", fg="#ffffff", highlightbackground="#DB8D22", width=15, font=("Avenir Next", "14"), command=lambda: self.savePlant())
        self.save_button.grid(row=0, column=1, padx=10, pady=30, ipadx=5, ipady=2)

        self.result_holder = Frame(master=self)

        self.image_holder_frame = Frame(master=self.result_holder, width=40)
        self.image_holder_frame.grid(row=0, column=0, padx=20, pady=40)

        self.image_holder = Label(master=self.image_holder_frame)
        self.image_holder.pack()

        self.info_holder = Frame(master=self.result_holder)
        self.info_holder.grid(row=0, column=1, padx=20, pady=40)

        self.sci_name_label = Label(master=self.info_holder, font=('Avenir Next', 14), text="Scientific name: ")
        self.sci_name_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.sci_name = Label(master=self.info_holder, font=('Avenir Next', 14), text="")
        self.sci_name.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.genus_label = Label(master=self.info_holder, font=('Avenir Next', 14), text="Genus: ")
        self.genus_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.genus = Label(master=self.info_holder, font=('Avenir Next', 14), text="")
        self.genus.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        self.family_label = Label(master=self.info_holder, font=('Avenir Next', 14), text="Family: ")
        self.family_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.family = Label(master=self.info_holder, font=('Avenir Next', 14), text="")
        self.family.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        self.avg_height_label = Label(master=self.info_holder, font=('Avenir Next', 14), text="Average height: ")
        self.avg_height_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        self.avg_height = Label(master=self.info_holder, font=('Avenir Next', 14), text="")
        self.avg_height.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        self.native_place_label = Label(master=self.info_holder, font=('Avenir Next', 14), text="Native place: ")
        self.native_place_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        self.native_place = Label(master=self.info_holder, font=('Avenir Next', 14), text="")
        self.native_place.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        self.tox_label = Label(master=self.info_holder, font=('Avenir Next', 14), text="Toxicity: ")
        self.tox_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")

        self.tox = Label(master=self.info_holder, font=('Avenir Next', 14), text="")
        self.tox.grid(row=5, column=1, padx=10, pady=10, sticky="w")

        self.edible_label = Label(master=self.info_holder, font=('Avenir Next', 14), text="Edible: ")
        self.edible_label.grid(row=6, column=0, padx=10, pady=10, sticky="w")

        self.edible = Label(master=self.info_holder, font=('Avenir Next', 14), text="")
        self.edible.grid(row=6, column=1, padx=10, pady=10, sticky="w")

        self.duration_label = Label(master=self.info_holder, font=('Avenir Next', 14), text="Duration: ")
        self.duration_label.grid(row=7, column=0, padx=10, pady=10, sticky="w")

        self.duration = Label(master=self.info_holder, font=('Avenir Next', 14), text="")
        self.duration.grid(row=7, column=1, padx=10, pady=10, sticky="w")

        self.download_button = Button(master=self.result_holder, text="Download JSON", command=self.downloadData)
        self.download_button.grid(row=1, columnspan=2, ipadx=3, ipady=5)

        self.result_holder.pack()

    def buttonToggle(self):

        if self.notInDB():
            self.save_button.config(text='Save')
        else:
            self.save_button.config(text='Unsave')

    def goBack(self):

        if self.backTo == 'search':
            self.god.show_frame(1)
        elif self.backTo == 'save':
            self.god.show_frame(3)

    def notInDB(self):

        try:
            with connect(self.db_path) as conn:
                query = '''SELECT sciname FROM species WHERE sciname = ?'''
                cursor = conn.cursor()
                result = cursor.execute(query, (self.data_cache['scientific_name'],)).fetchall()
                if len(result) == 0:
                    return True
                else:
                    return False
        except:
            print('Database connection failed')

    def savePlant(self):

        if self.notInDB():
            try:
                with connect(self.db_path) as conn:
                    query = '''INSERT INTO species (commonname, sciname, specieslink) VALUES (?, ?, ?)'''
                    cursor = conn.cursor()
                    cursor.execute(query, (self.data_cache['common_name'],self.data_cache['scientific_name'], self.data_cache['links']['self']))
                    conn.commit()
                    print(f">>{self.data_cache['scientific_name']} saved\n")
            except:
                print('Database connection failed')
        else:
            try:
                with connect(self.db_path) as conn:
                    query = '''DELETE FROM species WHERE sciname = ?'''
                    cursor = conn.cursor()
                    cursor.execute(query, (self.data_cache['scientific_name'],))
                    conn.commit()
                    print(f">>{self.data_cache['scientific_name']} removed\n")
            except:
                print('Database connection failed')
        self.buttonToggle()

    def dataUpdate(self, val, cameFrom):

        self.backTo = cameFrom

        response = requests.get(f"https://trefle.io{val}?token={getenv('APP_TOKEN')}")
        response_json = response.json()["data"]
        self.data_cache = response_json
        self.data_cache.pop("id")

        imgUrl = response_json["image_url"]
        r = requests.get(imgUrl, stream=True)
        raw_image = Image.open(BytesIO(r.content))
        raw_image.thumbnail((500, 500))
        resolved_image = ImageTk.PhotoImage(raw_image)

        self.image_holder.config(image=resolved_image)
        self.image_holder.image = resolved_image

        self.sci_name.config(text=f"{response_json['scientific_name']}")
        self.genus.config(text=f"{response_json['genus']}")
        self.family.config(text=f"{response_json['family']}")

        if response_json['specifications']['average_height']['cm'] == None:
            cm_final = 'n/a'
        elif response_json['specifications']['average_height']['cm'] >= 100:
            cm_val = response_json['specifications']['average_height']['cm'] / 100
            cm_final = str(cm_val) + 'm'
        else:
            cm_val = response_json['specifications']['average_height']['cm']
            cm_final = str(cm_val) + 'cm'
        self.avg_height.config(text=f"{cm_final}")

        try:
            temp = response_json['distribution']['native']

            native_list = []

            for item in temp:
                if(len(native_list) == 4):
                    break
                native_list.append(item)

            final = ", ".join(native_list)
        except:
            final = 'n/a'

        self.native_place.config(text=f"{final}")

        if(str(response_json['specifications']['toxicity']) == 'None'):
            setToxic = 'n/a'
        else:
            setToxic = str(response_json['specifications']['toxicity'])
        self.tox.config(text=f"{setToxic}")

        setEdible = ''
        if(str(response_json['edible']) == 'True'):
            setEdible = 'Yes'
        elif(str(response_json['edible']) == 'False'):
            setEdible = 'No'
        else:
            setEdible = 'n/a'
        self.edible.config(text=f"{setEdible}")

        duration_combo = []

        try:
            duration_data = response_json['duration']
            duration_vals = []
            for item in duration_data:
                duration_vals.append(item)
            final_dura = ', '.join(duration_vals)
        except:
            final_dura = 'n/a'
        self.duration.config(text=final_dura)

        self.buttonToggle()

    def downloadData(self):

        file_name = self.data_cache["scientific_name"]
        file_name = file_name.replace(" ", "_")
        file_name = file_name.lower()
        download_path = path.join(path.dirname(__file__), pardir)
        full_path = f"{download_path}/{file_name}.json"

        with open(full_path, "a") as f:
            dump(self.data_cache, f, indent=4)
            print(f">>Data downloaded in {full_path}")