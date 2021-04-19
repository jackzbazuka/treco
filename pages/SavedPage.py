from tkinter import Frame, Label, Button
from os import path, pardir
from sqlite3 import connect

class SavedPage(Frame):

    def __init__(self, master=None, controller=None):

        super().__init__(master=master)

        self.db_path = path.join(path.dirname(__file__), pardir, 'savedspecies.db')
        self.god = controller

        self.resultsHolder = Frame(master=self)

        self.back_button = Button(master=self, text="Back to Home", fg="#ffffff", highlightbackground="#40006F", width=15, font=("Avenir Next", "15"), command=lambda: controller.show_frame(0))
        self.back_button.pack(padx=10, pady=30, ipadx=5, ipady=2)

        self.Title = Label(master=self, text='Saved Species', fg="#40006F", font=("Avenir Next", "30"))
        self.Title.pack(padx=10, pady=30)

    def renderResults(self):

        for child in self.resultsHolder.winfo_children():
            child.destroy()

        try:
            with connect(self.db_path) as conn:
                cursor = conn.cursor()
                result = cursor.execute('SELECT commonname, specieslink FROM species').fetchall()
        except:
            print('Error connecting to database')

        self.label_holder = []

        a = 0
        b = 0

        for i in range(len(result)):
            name = result[i][0]
            data = result[i][1]
            self.label_holder.append(Label(master=self.resultsHolder, text=name, cursor="hand2"))
            self.label_holder[i].bind("<Enter>", lambda e: e.widget.config(fg="#fc0065"))
            self.label_holder[i].bind("<Leave>", lambda e: e.widget.config(fg="#000000"))
            self.label_holder[i].bind("<Button-1>", lambda e, arg=data: self.god.show_frame(2, arg, cameFrom='save'))
            if(b <= 6):
                self.label_holder[i].grid(row=a, column=b, padx=10, pady=15)
                b += 1
            elif(b == 7):
                a += 1
                b = 0
                self.label_holder[i].grid(row=a, column=b, padx=10, pady=15)
                b += 1

        print(f">>{len(self.label_holder)} results found!")
        
        self.resultsHolder.pack()