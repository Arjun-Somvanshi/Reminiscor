from response import api
import time
def test(n):
    if n == 1:
        database  = [
                        {"title": "Apple 1"},
                        {"title": "Apple 11"},
                        {"title": "BlackBerry 1"},
                        {"title": "BlackBerry 2"},
                        {"title": "BlackBerry 4"},
                        {"title": "Dropbox 4"},
                        {"title": "Google"},
                        {"title": "Google"},
                        {"title": "Google"},
                        {"title": "Google 1"},
                        {"title": "Google 10"},
                    ]
    if n == 2:
        database = []
    if n == 3: 
        database = [
                        {"title": "Google 0"}
                   ]
    return database
title = input("Enter a title: ")
database = test(1)
i = api.entry_insertion_index(title, database)
database.insert(i, {"title": title})
for i in database:
    print(i)
