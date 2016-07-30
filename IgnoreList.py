#separate python script to add subreddit to our ignorelist.p

try:
    from .PickleList import PickleList
except Exception: #ImportError
    from PickleList import PickleList


ignoreList = PickleList('ignorelist.p')

while(True):
    user_input = input('Insert Subreddit to add to ignorelist.p (CTRL + C to break): ')
    print('Inserting ' + str(user_input) + ' into ignorelist.p')
    ignoreList.add_to_pickle_list(user_input)
    ignoreList.save_pickle_list()
    print(str(user_input) + ' has been added successfully.\n')


