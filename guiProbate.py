from probate import Person
from Tkinter import *
from PIL import Image, ImageTk
import ttk
import tkMessageBox
import tkFileDialog
import sys
from stdoutredirect import StdoutRedirector
from dialoguepopup import DialogueBox

class ProbateGUI(object):


    def quit_app(self, event=None):
        self.root.quit()

    def save_file(self, event=None):
        self.backend.commit_save()

    def save_as_file(self, event=None):
        self.root.filename = tkFileDialog.asksaveasfilename(initialdir= "/",
                                                          title="Select file",
                                                          filetypes=(("json file", "*.json"),
                                                                     ("all files", "*.*")))
        self.backend.save_as(self.root.filename)

    def open_file(self, event=None):
        self.root.filename = tkFileDialog.askopenfilename(initialdir= "/",
                                                          title="Select file",
                                                          filetypes=(("json file", "*.json"),
                                                                     ("all files", "*.*")))
        self.backend = Person(self.root.filename)
        if self.backend.data["assets"]:
            pass
        else:
            popup = tkMessageBox.askyesno("Create New File",
                                          "Do you wish to create New File?")
            if popup:
                self.backend.create_new()
                self.backend.commit_save()

    def new_file(self, filename, event=None):
        popup = tkMessageBox.askyesno("Create New File",
                                      "Delete the current file and create a new one?")
        if popup:
            self.backend = Person(filename)
            self.backend.create_new()
            self.update_app()


    def update_app(self, event=None):
        self.list_probate_worth()
        self.probate_worth_summary_update()
        self.expense_probate_summary_update()
        self.expense_probate_list()
        self.combobox_names()


    def summary_update(self):
        sys.stdout = StdoutRedirector(self.summary_box)
        self.summary_box.config(state='normal')
        self.summary_box.delete('1.0', END)
        self.backend.print_asset()
        print "\nExpenses:\n"
        self.backend.print_expenses()
        print "\nAsset Split:\n"
        self.backend.print_asset_split()
        self.summary_box.config(state='disabled')
        sys.stdout = sys.__stdout__

    def summary_page_person_update(self):
        sys.stdout = StdoutRedirector(self.summary_page_person)
        self.summary_page_person.config(state='normal')
        self.summary_page_person.delete('1.0', END)
        print "Total Expense:"
        print self.backend.expenses_person(self.person)
        print "Asset Split:"
        print self.backend.asset_person(self.person)
        self.summary_page_person.config(state='disabled')
        sys.stdout = sys.__stdout__

    def probate_worth_summary_update(self):
        sys.stdout = StdoutRedirector(self.probate_worth_summary)
        self.probate_worth_summary.config(state='normal')
        self.probate_worth_summary.delete('1.0', END)
        print "Asset worth:"
        print self.backend.asset_worth()
        sys.stdout = sys.__stdout__

    def expense_probate_summary_update(self):
        sys.stdout = StdoutRedirector(self.expense_probate_summary)
        self.expense_probate_summary.config(state='normal')
        self.expense_probate_summary.delete('1.0', END)
        print "Expenses:"
        print self.backend.asset_expenses()
        sys.stdout = sys.__stdout__

    def scrollable(self, *args):
        self.probate_listbox.yview(*args)
        self.probate_worth_listbox.yview(*args)

    def scrollable_asset_expenses(self, *args):
        self.expense_item_listbox.yview(*args)
        self.expense_item_cost_listbox.yview(*args)

    def scrollable_person_item(self, *args):
        self.person_item_listbox.yview(*args)
        self.person_item_cost_listbox.yview(*args)

    def check_float(self, number):
        try:
            float(number)
            return True
        except ValueError:
            tkMessageBox.showerror("Price Error", "Please input a number")
            return False

    def check_name(self, name):
        name = name.strip()
        if name == "":
            tkMessageBox.showerror("Error", "Please input non-empty string")
            return False
        else:
             return True

    def list_probate_worth(self):
        self.probate_listbox.delete(0, END)
        self.probate_worth_listbox.delete(0, END)
        for item, worth in self.backend.data["assets"]["boon"].iteritems():
            self.probate_listbox.insert(END, item)
            self.probate_worth_listbox.insert(END, worth)

    def expense_probate_list(self):
        self.expense_item_listbox.delete(0, END)
        self.expense_item_cost_listbox.delete(0, END)
        for item, cost in self.backend.data["assets"]["expenses"].iteritems():
            self.expense_item_listbox.insert(END, item)
            self.expense_item_cost_listbox.insert(END, cost)

    def delete_asset(self, event):
        widget = event.widget
        if widget == self.probate_listbox or widget == self.probate_worth_listbox:
            if widget == self.probate_listbox:
                selection = self.probate_listbox.curselection()
            elif widget == self.probate_worth_listbox:
                selection = self.probate_worth_listbox.curselection()
            item = self.probate_listbox.get(selection)
            self.backend.delete_asset_boon(item)
            self.list_probate_worth()
            self.probate_worth_summary_update()
        elif widget == self.expense_item_listbox or widget == self.expense_item_cost_listbox:
            if widget == self.expense_item_listbox:
                selection = self.expense_item_listbox.curselection()
            elif widget == self.expense_item_cost_listbox:
                selection = self.expense_item_cost_listbox.curselection()
            item = self.expense_item_listbox.get(selection)
            self.backend.delete_asset_expense(item)
            self.expense_probate_summary_update()
            self.expense_probate_list()

    def add_item_probate(self):
        item = self.item_asset.get()
        worth = self.item_asset_worth.get()
        if self.check_name(item) and self.check_float(worth):
            self.backend.add_asset_boon(item, worth)
            self.list_probate_worth()
            self.probate_worth_summary_update()

    def add_item_expense(self):
        item = self.item_expense.get()
        cost = self.item_expense_cost.get()
        if self.check_name(item) and self.check_float(cost):
            self.backend.add_asset_expense(item, cost)
            self.expense_probate_summary_update()
            self.expense_probate_list()

    def update_asset(self, event):
        widget = event.widget
        item_location = widget.curselection()
        if widget == self.probate_listbox or widget == self.probate_worth_listbox:
            item = self.probate_listbox.get(item_location)
            cost = self.probate_worth_listbox.get(item_location)
        elif widget == self.expense_item_listbox or widget == self.expense_item_cost_listbox:
            item = self.expense_item_listbox.get(item_location)
            cost = self.expense_item_cost_listbox.get(item_location)
        popup = DialogueBox(self.root, item, cost)
        if popup.item != item or popup.cost != cost:
            if widget == self.probate_listbox or widget == self.probate_worth_listbox:
                self.backend.delete_asset_boon(item)
                self.backend.add_asset_boon(popup.item, popup.cost)
                self.list_probate_worth()
                self.probate_worth_summary_update()
            elif widget == self.expense_item_listbox or widget == self.expense_item_cost_listbox:
                self.backend.delete_asset_expense(item)
                self.backend.add_asset_expense(popup.item, popup.cost)
                self.expense_probate_summary_update()
                self.expense_probate_list()

    def add_person(self):
        person = self.add_name_var.get()
        self.backend.add_name(person)
        self.combobox_names()
        self.person_select_combobox.set(person)
        self.person_select()

    def delete_person(self, person):
        self.backend.remove_name(person)
        self.combobox_names()
        self.person_select_combobox.current(0)
        self.person_select()


    def add_person_item(self):
        item = self.person_item_var.get()
        cost = self.person_item_cost_var.get()
        if self.check_name(item) and self.check_float(cost):
            self.backend.add_expense(item, cost, self.person)
            self.person_item_listbox.insert(END, item)
            self.person_item_cost_listbox.insert(END, cost)
            self.summary_page_person_update()
        else:
            pass

    def remove_person_item(self, event):
        widget = event.widget
        if widget == self.person_item_listbox:
            selection = self.person_item_listbox.curselection()
        elif widget == self.person_item_cost_listbox:
            selection = self.person_item_cost_listbox.curselection()
        item = self.person_item_listbox.get(selection)
        self.backend.remove_expense(item, self.person)
        self.insert_person_listbox()
        self.summary_page_person_update()

    def update_person_item(self, event):
        """ Brings up a new window to change the current selected item.
        Have to double click left mouse button to bring it up. """
        widget = event.widget
        if widget == self.person_item_listbox:
            select = self.person_item_listbox.curselection()
        elif widget == self.person_item_cost_listbox:
            select = self.person_item_cost_listbox.curselection()
        item = self.person_item_listbox.get(select)
        price = self.person_item_cost_listbox.get(select)
        popup = DialogueBox(self.person_page, item, price,
                            title="Update Person Item")
        popup_item = popup.item.strip()
        popup_cost = popup.cost.strip()
        if popup_item != item or popup_cost != price:
            self.backend.remove_expense(item, self.person)
            self.backend.add_expense(popup_item, popup_cost, self.person)
            self.insert_person_listbox()
            self.summary_page_person_update()

    def combobox_names(self):
        """ Puts the names in the Combobox"""
        names = list()
        for name, expenses in self.backend.data["name"].iteritems():
            names.append(name)
        self.person_select_combobox['values'] = names

    def insert_person_listbox(self):
        """ Inserts the item and the cost in the Listboxes for selected person """
        self.person_item_listbox.delete(0 ,END)
        self.person_item_cost_listbox.delete(0, END)
        for item, cost in self.backend.data["name"][self.person]["expenses"].iteritems():
            self.person_item_listbox.insert(END, item)
            self.person_item_cost_listbox.insert(END, cost)


    def person_select(self, event=None):
        """ Creates the page for the person selected in the Combobox"""
        self.person = self.person_select_combobox.get()
        self.delete_button = Button(self.person_page, text="DELETE",
                                    command=lambda: self.delete_person(self.person))
        self.delete_button.grid(row=1, column=2)

        self.person_item_scrollbar = ttk.Scrollbar(self.person_page,
                                                   orient=VERTICAL,
                                                   command=self.scrollable_person_item)
        item_label_person = Label(self.person_page, text="Item")
        cost_label_person = Label(self.person_page, text="Cost")

        item_label_person.grid(row=2, column=0)
        cost_label_person.grid(row=2, column=1)

        self.person_item_listbox = Listbox(self.person_page, width=10,
                                           yscrollcommand=self.person_item_scrollbar)
        self.person_item_cost_listbox = Listbox(self.person_page, width=10,
                                                yscrollcommand=self.person_item_scrollbar)
        self.person_item_listbox.grid(row=3, column=0)
        self.person_item_cost_listbox.grid(row=3, column=1)
        self.insert_person_listbox()
        self.person_item_listbox.bind('<Double-Button-1>',
                                      self.update_person_item)
        self.person_item_cost_listbox.bind('<Double-Button-1>',
                                      self.update_person_item)
        self.person_item_listbox.bind('<Delete>',
                                      self.remove_person_item)
        self.person_item_cost_listbox.bind('<Delete>',
                                           self.remove_person_item)
        self.summary_page_person = Text(self.person_page, width=14, height=10)
        self.summary_page_person.grid(row=3, column=2)
        self.summary_page_person.config(state='disabled')
        self.summary_page_person["bg"] = '#D3D3D3'
        self.summary_page_person_update()

        self.person_item_var = StringVar()
        self.person_item_cost_var = StringVar()

        self.person_item_entry = Entry(self.person_page,
                                       textvariable=self.person_item_var,
                                       width=10)
        self.person_item_cost_entry = Entry(self.person_page,
                                            textvariable=self.person_item_cost_var,
                                            width=10)
        self.person_item_add = Button(self.person_page, text="Add Item",
                                      command=self.add_person_item)
        self.person_item_entry.grid(row=4, column=0, pady=10)
        self.person_item_cost_entry.grid(row=4, column=1, pady=10)
        self.person_item_add.grid(row=4, column=2)




    def __init__(self, root, filename):
        self.root = root
        self.root.title("Probate Calculator")
        self.root.geometry("300x550")
        self.root.resizable(False, False)
        self.root.option_add('*tearoff', FALSE)
        self.backend = Person(filename)

        # -------- Creating pulldown menu

        menubar = Menu(self.root)
        menu_file = Menu(menubar, tearoff=0)
        #menu_edit = Menu(menubar, tearoff=0)
        menu_help = Menu(menubar, tearoff=0)
        menubar.add_cascade(menu=menu_file, label='File')
        #menubar.add_cascade(menu=menu_edit, label='Edit')
        menubar.add_cascade(menu=menu_help, label='Help')

        # --------- Cascade menu for file

        menu_file.add_command(label='New',
                              command=lambda: self.new_file(filename))
        menu_file.add_separator()
        menu_file.add_command(label='Save', command=self.save_file)
        menu_file.add_command(label='Save As...', command=self.save_as_file)
        menu_file.add_separator()
        menu_file.add_command(label='Open', command=self.open_file)
        menu_file.add_separator()
        menu_file.add_command(label='Exit', command=self.quit_app)

        # --------- Some bindings for the commands
        self.root.bind_all("<Control-x>", self.quit_app)
        self.root.bind_all("<Control-s>", self.save_file)

        # ---------- Cascade menu for Edit

        #menu_edit.add_command(label='Add Person')
        #menu_edit.add_command(label='Remove Person')

        # ---------- Cascade menu for Help

        menu_help.add_command(label="Help...")
        self.root.config(menu=menubar)

        # ---------- Tabs for probate
        tabs = ttk.Notebook(self.root)
        tabs.pack(fill="both")

        summary_page = ttk.Frame(tabs)
        probate_page = ttk.Frame(tabs)
        self.person_page = ttk.Frame(tabs)
        tabs.add(summary_page, text="Summary")
        tabs.add(probate_page, text="Probate")
        tabs.add(self.person_page, text="Reimbursements")

        # --------- Summary page
        summary_scrollbar = Scrollbar(summary_page)
        summary_scrollbar.pack(side=RIGHT, fill=Y)
        self.summary_box = Text(summary_page, height= 35, width=15, wrap='word',
                                yscrollcommand=summary_scrollbar.set)
        self.summary_box.config(state='disabled')
        self.summary_box["bg"] = '#D3D3D3'
        self.summary_box.pack(padx=5, pady=5, fill="both")
        calculate_summary = Button(summary_page, text="Calculate",
                                   command=self.summary_update)
        calculate_summary.pack()

        #---------- Probate page
        probate_item_label = ttk.Label(probate_page, text="Asset")
        probate_item_worth_label = ttk.Label(probate_page, text="Worth")
        probate_item_label.grid(row=0, column=0, pady=10)
        probate_item_worth_label.grid(row=0, column=1, pady=10)
        # --------- Assets of Probate
        self.asset_scrollbar = ttk.Scrollbar(probate_page, orient=VERTICAL,
                                             command=self.scrollable)

        probate_item = StringVar()
        probate_cost = StringVar()

        self.probate_listbox = Listbox(probate_page, width=10,
                                       yscrollcommand=self.asset_scrollbar,
                                       listvariable=probate_item)
        self.probate_worth_listbox = Listbox(probate_page, width=10,
                                             yscrollcommand=self.asset_scrollbar,
                                             listvariable=probate_cost)
        self.probate_worth_summary = Text(probate_page, width=14, height=10)
        self.list_probate_worth()
        self.probate_listbox.grid(row=1, column=0)
        self.probate_worth_listbox.grid(row=1, column=1)
        self.probate_worth_summary.grid(row=1, column=2)
        self.probate_worth_summary.config(state='disabled')
        self.probate_worth_summary["bg"] = '#D3D3D3'
        self.probate_worth_summary_update()

        self.item_asset = StringVar()
        self.item_asset_worth = StringVar()

        self.entry_item_asset = Entry(probate_page, textvariable=self.item_asset,
                                      width=10)
        self.entry_item_cost = Entry(probate_page, textvariable=self.item_asset_worth,
                                     width=10)
        self.entry_item_asset.grid(row=2, column=0)


        self.entry_item_cost.grid(row=2, column=1)
        self.add_probate_asset = Button(probate_page, text="Add",
                                        command=self.add_item_probate)
        self.add_probate_asset.grid(row=2, column=2)
        self.probate_listbox.bind('<Delete>',
                                  self.delete_asset)
        self.probate_worth_listbox.bind('<Delete>',
                                        self.delete_asset)
        self.probate_worth_listbox.bind('<Double-Button-1>',
                                        self.update_asset)


        # -------- Expenses of Probate
        self.item_expense_item_label = Label(probate_page, text="Expense")
        self.item_expense_cost_label = Label(probate_page, text="Worth")
        self.item_expense_item_label.grid(row=3, column=0, pady=10)
        self.item_expense_cost_label.grid(row=3, column=1, pady=10)

        self.probate_item_expenses = StringVar()
        self.probate_cost_expenses = StringVar()
        self.asset_expenses_scrollbar = ttk.Scrollbar(probate_page,
                                                      orient=VERTICAL,
                                                      command=self.scrollable_asset_expenses)
        self.expense_item_listbox = Listbox(probate_page, width=10,
                                            yscrollcommand=self.asset_expenses_scrollbar,
                                            listvariable=self.probate_item_expenses)
        self.expense_item_cost_listbox = Listbox(probate_page, width=10,
                                            yscrollcommand=self.asset_expenses_scrollbar,
                                            listvariable=self.probate_cost_expenses)
        self.expense_probate_summary = Text(probate_page, width=14, height=10)
        self.expense_probate_list()
        self.expense_item_listbox.grid(row=4, column=0)
        self.expense_item_cost_listbox.grid(row=4, column=1)
        self.expense_probate_summary.grid(row=4, column=2)
        self.expense_probate_summary.config(state='disabled')
        self.expense_probate_summary["bg"] = '#D3D3D3'
        self.expense_probate_summary_update()

        self.item_expense = StringVar()
        self.item_expense_cost = StringVar()

        self.item_expense_entry = Entry(probate_page, textvariable=self.item_expense,
                                        width=10)
        self.item_expense_cost_entry = Entry(probate_page,
                                             textvariable=self.item_expense_cost,
                                             width=10)
        self.item_expense_entry.grid(row=5, column=0)
        self.item_expense_cost_entry.grid(row=5, column=1)
        self.item_add_expense = Button(probate_page, text="Add",
                                       command=self.add_item_expense)
        self.item_add_expense.grid(row=5, column=2)
        self.expense_item_listbox.bind('<Delete>',
                                       self.delete_asset)
        self.expense_item_cost_listbox.bind('<Delete>',
                                            self.delete_asset)
        self.expense_item_listbox.bind('<Double-Button-1>',
                                       self.update_asset)
        self.expense_item_cost_listbox.bind('<Double-Button-1>',
                                            self.update_asset)

        # ------------ Person Page
        self.add_name_var = StringVar()
        self.add_name_entry = Entry(self.person_page, textvariable=self.add_name_var,
                                    width=10)
        button_add_person = Button(self.person_page, text="Add Person",
                                   command=self.add_person)

        self.add_name_entry.grid(row=0, column=1)
        button_add_person.grid(row=0, column=0)

        person_select_label = Label(self.person_page, text="Select Person")
        self.person_select_combobox = ttk.Combobox(self.person_page, width=10)
        person_select_label.grid(row=1,column=0)
        self.person_select_combobox.grid(row=1, column=1, pady=15)
        self.combobox_names()
        self.person_select_combobox.bind('<<ComboboxSelected>>',
                                         self.person_select)






root = Tk()
probategui = ProbateGUI(root, "reim.json")
root.mainloop()
