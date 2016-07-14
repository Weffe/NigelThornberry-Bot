__author__ = 'Rogelio Negrete - Weffe'

import pickle
import random
import time
from datetime import datetime

class PickleList:
    def __init__(self, nameoffile):
        self.nameoffile = nameoffile
        self.pickle_list = self.load_pickle_list()

    def load_pickle_list(self):
        with open(self.nameoffile, "rb") as file:
            try:
                pickle_list = pickle.load(file)
                return pickle_list
            except:
                return []

    def add_to_pickle_list(self, user_input):
        #its a list of tuples
        #user input = [{permalink : timeposted}, {permalink : timeposted}, ...]
        self.pickle_list.append(user_input)

    def save_pickle_list(self):
        # save to existing list
        with open(self.nameoffile, "wb") as file:
            pickle.dump(self.pickle_list, file)

    def manual_add_to_pickle_list(self):
        endLoop = False

        while (endLoop != True):
            user_input = input("Enter in (Nigel) Link [Enter DONE to stop]: ")
            if user_input != 'done':
                self.pickle_list.append(user_input)
                print(self.pickle_list)
            else:
                endLoop = True
        # save to existing list
        with open(self.nameoffile, "wb") as file:
            pickle.dump(self.pickle_list, file)

    def empty_pickle_file(self):
        #cheeky way of deleting the file content
        #just open the file and save an empty list to it - which overwrites everything
        with open(self.nameoffile, "wb") as file:
            pickle.dump([], file)

    def print_pickle(self):
        print(self.pickle_list)

    #-----------------------
    #NIGEL Related method(s)
    def choose_random_nigel_pic(self):
        #choose a random nigel picture from the pickle list
        return random.choice(self.pickle_list)

    #----------------------
    #permalinks Related method(s)
    def is_link_in_list(self, permalink):
        linkInList = False

        #permalink list looks like: (permalink, date_posted)
        for key in [y[0] for y in self.pickle_list]:
            if permalink == key:
                #print('Found old match. Ignoring comment. Link: ' + permalink)
                linkInList = True

        return linkInList

    def clean_up_permalink_list(self):
        day_ago = datetime.fromtimestamp(time.time() - (24 * 60 * 60))  # find date for 24 hours ago

        for tupleItem in self.pickle_list:
            permalink_date = tupleItem[1]
            time_delta = int((day_ago - permalink_date).days) + 1

            if time_delta >= 2:
                #print("Found Old Link.")
                self.pickle_list.remove(tupleItem)



