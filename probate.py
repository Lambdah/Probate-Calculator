import json


class Person(object):

    def __init__(self, filename):
        self.filename = filename
        try:
            self.data = self.openjson(filename)
        except IOError:
            self.create_new()
            self.data = self.openjson(filename)

    def asset_worth(self):
        assets = self.data["assets"]["boon"]
        tot_asset = 0
        for item, worth in assets.iteritems():
            tot_asset += float(worth)
        return tot_asset

    def asset_expenses(self):
        expenses = self.data["assets"]["expenses"]
        tot_expense = 0
        for item, worth in expenses.iteritems():
            tot_expense += float(worth)
        return tot_expense

    def print_names(self):
        names = self.data["name"]
        for k, v in names.iteritems():
            print k

    def print_expenses(self):
        person_expenses = self.data["name"]
        asset_expenses = self.data["assets"]["expenses"]
        tot_person_exp = 0
        tot_asset_exp = 0
        for name, expense in person_expenses.iteritems():
            personal_exp = self.print_expenses_person(name)
            tot_person_exp += personal_exp
        print "Total expenses for people: {:0.2f}".format(tot_person_exp)
        print "Asset Expense"
        for item, expense in asset_expenses.iteritems():
            print "\t", item, "\n\t\t", expense
            tot_asset_exp += float(expense)
        print "Total Asset expenses: {:0.2f}".format(tot_asset_exp)
        print "Total Expenses: {:0.2f}".format(tot_asset_exp + tot_person_exp)

    def print_expenses_person(self, name):
        person_expenses = self.data["name"][name]["expenses"]
        tot_exp_person = 0
        print name
        for item, expense in person_expenses.iteritems():
            tot_exp_person += float(expense)
            print "\t", item, "\n\t\t", expense
        print "Total: {:0.2f}".format(tot_exp_person)
        return tot_exp_person

    def print_asset(self):
        asset_boon = self.data["assets"]["boon"]
        print "Asset Items"
        for item, income in asset_boon.iteritems():
            print "\t", item, "\n\t\t", income
        print "Total Asset Worth: ", self.asset_worth()

    def expenses_person(self, name):
        tot_exp = 0
        person_exp = self.data["name"][name]["expenses"]
        for item, exp in person_exp.iteritems():
            tot_exp += float(exp)
        return tot_exp

    def total_expenses(self):
        tot_exp = 0
        per_expenses = self.data["name"]
        for name, exp in per_expenses.iteritems():
            per_expenses = self.data["name"][name]["expenses"]
            for item, cost in per_expenses.iteritems():
                tot_exp += float(cost)
        asset_expenses = self.data["assets"]["expenses"]
        for item, val in asset_expenses.iteritems():
            tot_exp += float(val)
        return tot_exp

    def split_asset(self):
        counter = 0
        for k, v in self.data["name"].iteritems():
            counter += 1
        exp_worth = self.total_expenses()
        split = round((self.asset_worth() - exp_worth) / counter, 2)
        return split

    def print_asset_split(self):
        split_asset_worth = self.split_asset()
        for name, exp in self.data["name"].iteritems():
            print name
            income_worth = self.expenses_person(name)
            print "\t{:0.2f}".format(income_worth + split_asset_worth)

    def print_asset_person(self, name):
        exp_person = self.expenses_person(name)
        split_asset_worth = self.split_asset()
        print name
        print "\t", (split_asset_worth + exp_person)

    def asset_person(self, name):
        exp_person = self.expenses_person(name)
        split_asset_worth = self.split_asset()
        return (split_asset_worth + exp_person)

# Dealing with the json file
    def openjson(self, jsonfile):
        with open(jsonfile, 'r+') as k:
            reim = json.load(k)
        return reim

    def add_expense(self, expense, value, name):
        item = {expense: value }
        try:
            self.data["name"][name]["expenses"].update(item)
        except KeyError:
            self.add_name(name)
            self.data["name"][name]["expenses"].update(item)
        #with open(self.filename, 'w') as f:
            #f.write("{}".format(json.dumps(self.data, sort_keys=True, indent=4, separators=(',', ': '))))

    def remove_expense(self, expense, name):
        try:
            del self.data["name"][name]["expenses"][expense]
            #with open(self.filename, 'w') as f:
                #f.write("{}".format(json.dumps(self.data, sort_keys=True, indent=4, separators=(',', ': '))))
        except KeyError:
            print "Expense does not exist with", name

    def add_name(self, name):
        fname = {name: {"expenses" : {} } }
        self.data["name"].update(fname)
        #with open(self.filename, 'w') as f:
            #f.write("{}".format(json.dumps(self.data, sort_keys=True, indent=4, separators=(',', ': '))))

    def remove_name(self, name):
        try:
            del self.data["name"][name]
            #with open(self.filename, 'w') as f:
                #f.write("{}".format(json.dumps(self.data, sort_keys=True, indent=4, separators=(',', ': '))))
        except KeyError:
            print "Person does not with the name ", name

    def add_asset_expense(self, expense, value):
        item = {expense: value}
        try:
            self.data["assets"]["expenses"].update(item)
        except KeyError:
            print "Error"
        #with open(self.filename, 'w') as f:
            #f.write("{}".format(json.dumps(self.data, sort_keys=True, indent=4, separators=(',', ': '))))

    def delete_asset_expense(self, expense):
        try:
            del self.data["assets"]["expenses"][expense]
            #with open(self.filename, 'w') as f:
                #f.write("{}".format(json.dumps(self.data, sort_keys=True, indent=4, separators=(',', ': '))))
        except KeyError:
            print "No ", expense, " exists"

    def add_asset_boon(self, item, value):
        boon = {item: value}
        try:
            self.data["assets"]["boon"].update(boon)
        except KeyError:
            print "Error"
        #with open(self.filename, 'w') as f:
            #f.write("{}".format(json.dumps(self.data, sort_keys=True, indent=4, separators=(',', ': '))))

    def delete_asset_boon(self, item):
        try:
            del self.data["assets"]["boon"][item]
        except KeyError:
            print "Asset does not exist"

    def create_new(self):
        self.data = {"assets" : {"boon": {},"expenses": {} }, "name": {} }
        with open(self.filename, 'w') as f:
            f.write("{}".format(json.dumps(self.data, sort_keys=True, indent=4, separators=(',', ': '))))

    def commit_save(self):
        with open(self.filename, 'w') as f:
            f.write("{}".format(json.dumps(self.data, sort_keys=True, indent=4, separators=(',', ': '))))

    def save_as(self, namefile):
        with open(namefile, 'w') as f:
            f.write("{}".format(json.dumps(self.data, sort_keys=True, indent=4, separators=(',', ': '))))
