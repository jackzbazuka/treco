from tkinter import Frame, Label, Button, Entry, Scrollbar
import requests
from dotenv import load_dotenv
from os import getenv
from progress.bar import Bar

load_dotenv()

class SearchPage(Frame):

    def __init__(self, master=None, controller=None):

        super().__init__(master=master)
        self.god = controller

        self.searchHolder = Frame(master=self)
        self.resultsHolder = Frame(master=self)

        self.Title = Label(master=self, text='Search', fg="#40006F", font=("Avenir Next", "30"))
        self.Title.pack(padx=10, pady=30)

        self.search_box = Entry(master=self.searchHolder, width=30, borderwidth=3, font=("Avenir Next", "18"))
        self.search_box.bind("<Return>", lambda e: self.fetchData())
        self.search_box.grid(row=0, column=0, padx=15, pady=30, ipadx=5, ipady=2)

        self.search_button = Button(master=self.searchHolder, text="Search", fg="#ffffff", highlightbackground="#40006F", width=15, font=("Avenir Next", "15"), command=lambda: self.fetchData())
        self.search_button.grid(row=0, column=1, padx=10, pady=30, ipadx=5, ipady=2)

        self.back_button = Button(master=self.searchHolder, text="Back to Home", fg="#ffffff", highlightbackground="#40006F", width=15, font=("Avenir Next", "15"), command=lambda: controller.show_frame(0))
        self.back_button.grid(row=0, column=2, padx=10, pady=30, ipadx=5, ipady=2)

        self.searchHolder.pack()

    def fetchData(self):

        i = 1
        flow = True
        pageLimit = 2
        self.common_name_list = []

        for child in self.resultsHolder.winfo_children():
            child.destroy()

        query_string = str(self.search_box.get())
        query_string = query_string.lower()
        query_string = query_string.replace(' ', '%20')

        while(flow and i <= pageLimit):
            response = requests.get(f"https://trefle.io/api/v1/species/search?q={self.search_box.get()}&token={getenv('APP_TOKEN')}&filter_not[common_name]=null&page={i}")
            json_response = response.json()
            response_data = json_response["data"]

            bar = Bar(f">>Searching page {i}", max=len(response_data))

            for species in response_data:
                if ((species["image_url"] == None) or (species["scientific_name"] == None)):
                    pass
                    #print(f"\n>>Insufficient data available on {species['scientific_name']}, species discarded")
                else:
                    self.common_name_list.append((species["common_name"], species["links"]["self"]))
                bar.next()
            bar.finish()

            try:
                if("page=" in json_response["links"]["next"]):
                    flow = True
                    i += 1
                else:
                    flow = False
            except:
                flow = False
        bar.finish()
        print(f">>{len(self.common_name_list)} results found!\n")

        self.renderLabels()

    def renderLabels(self):

        self.label_holder = []

        a = 0
        b = 0

        for i in range(len(self.common_name_list)):
            name = self.common_name_list[i][0]
            data = self.common_name_list[i][1]
            self.label_holder.append(Label(master=self.resultsHolder, text=name, cursor="hand2"))
            self.label_holder[i].bind("<Enter>", lambda e: e.widget.config(fg="#fc0065"))
            self.label_holder[i].bind("<Leave>", lambda e: e.widget.config(fg="#000000"))
            self.label_holder[i].bind("<Button-1>", lambda e, arg=data: self.god.show_frame(2, arg, cameFrom='search'))
            if(b <= 6):
                self.label_holder[i].grid(row=a, column=b, padx=10, pady=15)
                b += 1
            elif(b == 7):
                a += 1
                b = 0
                self.label_holder[i].grid(row=a, column=b, padx=10, pady=15)
                b += 1

        self.resultsHolder.pack()