from tkinter import Frame, Label, Button
from PIL import ImageTk, Image

about = "This is a botanical encyclopedia made with Tkinter. This app allows you to search the plants by their botanical names, list out flora of a specific habitat and provide other relevant information about them."

class StartPage(Frame):

    def __init__(self, master=None, controller=None):

        super().__init__(master=master)

        self.leaf_image = Image.open("public/leaf.png").resize((200, 200))
        self.leaf = ImageTk.PhotoImage(self.leaf_image)

        self.search_icon = Image.open("public/search.png").resize((20, 20))
        self.search = ImageTk.PhotoImage(self.search_icon)

        self.save_icon = Image.open("public/save.png").resize((20, 20))
        self.save = ImageTk.PhotoImage(self.save_icon)

        self.heading = Label(master=self, text="Treco", anchor="c", fg="#0F8100", font=("Avenir Next", "50"))
        self.heading.pack(pady=(40, 0))

        self.image_holder = Label(master=self, image=self.leaf)
        self.image_holder.pack(pady=(20, 0))

        self.brief = Label(master=self, text=about, anchor="c", fg="#106A04", wraplength=450, font=(("Avenir Next", "15")))
        self.brief.pack(pady=(100,0))

        self.search_button = Button(master=self, text="Search  ", fg="#000000", width=40, font=(("Avenir Next", "15")), image=self.search, compound="right", command=lambda: controller.show_frame(1))
        self.search_button.bind("<Enter>", lambda e: e.widget.config(fg="#8100ff"))
        self.search_button.bind("<Leave>", lambda e: e.widget.config(fg="#000000"))
        self.search_button.pack(pady=(40, 0), ipadx=15, ipady=8)

        self.saved_button = Button(master=self, text="Saved  ", fg="#000000", width=40, font=(("Avenir Next", "15")), image=self.save, compound="right", command=lambda: controller.show_frame(3))
        self.saved_button.bind("<Enter>", lambda e: e.widget.config(fg="#8100ff"))
        self.saved_button.bind("<Leave>", lambda e: e.widget.config(fg="#000000"))
        self.saved_button.pack(pady=(10, 0), ipadx=15, ipady=8)