from Tkinter import *
import tkMessageBox
import os

class DialogueBox(Toplevel):

    def validation(self):
        try:
            float(self.cost_var.get())
            return True
        except ValueError:
            tkMessageBox.showerror("Cost Error", "Please enter a Number")
            return False

    def apply(self):
        self.item = self.item_var.get()
        self.cost = self.cost_var.get()

    def ok_update_item(self, event=None):
        if not self.validation():
            self.initial_focus.focus_set()
            return

        self.apply()
        self.withdraw()
        self.update_idletasks()
        self.cancel_update_item()



    def cancel_update_item(self, event=None):
        self.parent.focus_set()
        self.destroy()

    def __init__(self, parent, item, cost, title=None):
        Toplevel.__init__(self, parent)
        self.transient(parent)

        if title:
            self.title(title)
        self.item = item
        self.cost = cost

        self.parent = parent
        self.geometry("200x110")
        body = Frame(self)
        self.initial_focus = body
        body.pack(padx=5, pady=5)
        self.item_label = Label(body, text="Item")
        self.cost_label = Label(body, text="Cost")

        self.item_var = StringVar()
        self.cost_var = StringVar()

        self.item_entry = Entry(body, textvariable=self.item_var, width=15)
        self.cost_entry = Entry(body, textvariable=self.cost_var, width=15)
        self.item_var.set(self.item)
        self.cost_var.set(self.cost)

        self.item_label.grid(row=0, column=0)
        self.cost_label.grid(row=1, column=0)

        self.item_entry.grid(row=0, column=1, pady=5)
        self.cost_entry.grid(row=1, column=1, pady=5)

        self.ok_button = Button(body, text="OK", command = self.ok_update_item)
        self.cancel_button = Button(body, text="Cancel",
                                    command=self.cancel_update_item)
        self.ok_button.grid(row=2, column=0, pady=5)
        self.cancel_button.grid(row=2, column=1, pady=5)

        self.bind("<Return>", self.ok_update_item)
        self.bind("<Escape>", self.cancel_update_item)

        self.wait_visibility()
        self.grab_set()
        self.initial_focus.focus_set()
        self.wait_window(self)
