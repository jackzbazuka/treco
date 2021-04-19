from tkinter import Frame, Tk
from sqlite3 import connect
from os import path
from pages.StartPage import StartPage
from pages.SearchPage import SearchPage
from pages.ResultPage import ResultPage
from pages.SavedPage import SavedPage

class Main(Tk):

    def __init__(self, screenName=None, baseName=None, useTk=1, sync=0, use=None, *args, **kwargs):

        super().__init__(screenName=screenName, baseName=baseName, useTk=useTk, sync=sync, use=use, *args, **kwargs)
        self.title("Treco")
        self.geometry("1200x720+120+50")
        self.resizable(False, False)

        container = Frame(master=self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.frames = {}

        pages = [StartPage, SearchPage, ResultPage, SavedPage]

        for i in range(len(pages)):
            frame = pages[i](master=container, controller=self)
            self.frames[i] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(0)

    def show_frame(self, controller, info=None, cameFrom=None):

        frame = self.frames[controller]
        if(controller == 2):
            frame.dataUpdate(info, cameFrom)
        elif(controller == 3):
            frame.renderResults()
        frame.tkraise()


open('savedspecies.db', 'a').close()

FILEPATH = path.join(path.dirname(__file__), 'savedspecies.db')

try:
     with connect(FILEPATH) as conn:
        query = '''CREATE TABLE IF NOT EXISTS species (uid INTEGER PRIMARY KEY AUTOINCREMENT, commonname TEXT NOT NULL, sciname TEXT NOT NULL, specieslink TEXT NOT NULL)'''
        cursor = conn.cursor()
        cursor.execute(query)
        print('Database created successfully')
except:
    print('Database creation failed')

if __name__ == "__main__":
    app = Main()
    app.mainloop()