#!/usr/bin/env python

import sys
import argparse
import sqlite3
#note --d 5 --email yes "read chapter 3"

conn = sqlite3.connect('termnote.db')
cur = conn.cursor()

#conn.execute("DROP TABLE IF EXISTS user_info")


def main():
    #print("TermNotes")
    #print(sys.argv)
    #note=sys.argv[-1]

    #Table for storing notes and their category
    cur.execute('''CREATE TABLE IF NOT EXISTS notes
         (  ID             INTEGER      PRIMARY KEY,
            DESC           TEXT                     NOT NULL,
            CAT            TEXT                     NOT NULL);''')

    #Table for storing user info. Assume only 1 user.
    cur.execute('''CREATE TABLE IF NOT EXISTS user_info
         (  ID             INTEGER      PRIMARY KEY,
            NAME           TEXT                     NOT NULL,
            EMAIL          TEXT);''')

    # Table for storing tasks and their due date
    cur.execute('''CREATE TABLE IF NOT EXISTS tasks
         (  ID             INTEGER      PRIMARY KEY,
            DESC           TEXT                     NOT NULL,
            DUE            INT                      NOT NULL);''')


    #print "Tables created successfully";



    parser = argparse.ArgumentParser(description='take notes on the terminal. Example: termnotes add "pay phone bill"')
    subparsers = parser.add_subparsers(help='sub command help', dest='command')

    parser_add = subparsers.add_parser('add',help='add help')
    parser_add.add_argument('note', type=str, help='Note to add')
    parser_add.add_argument('-c', '--category', type=str, default='unfiled', help="category for this note")

    parser_del = subparsers.add_parser('del',help='add help')
    parser_del.add_argument('id', type=str, help='Note id to del')

    parser_list = subparsers.add_parser('list', help='delete help')

    parser_remind = subparsers.add_parser('remind', help='remind help')
    parser_remind.add_argument('task', type=str, help='task to remind')
    parser_remind.add_argument('-d','--due', type=int, default=1, help='days until due (default: 1)')

    parser_settings = subparsers.add_parser('settings', help='settings help')
    parser_settings.add_argument('-n', '--name', type=str, help='Your display name')
    parser_settings.add_argument('-e', '--email', type=str, help='Your email address')

    cur.execute("SELECT * FROM user_info")
    userinfo = cur.fetchall()
    if(len(userinfo) == 0):         #if no user info exists, create a placeholder user
        cur.execute("INSERT INTO user_info (NAME,EMAIL) VALUES (?, ?)", ("Name","Name@example.com"));


    args = parser.parse_args()
    #print(args)
    #print(args.command)
    command = args.command
    if(command == "add"):
        addNote(args.note, args.category)
    elif(command == "del"):
        delNote(args.id)
    elif(command == "remind"):
        addTask(args.task, args.due)
    elif(command == "list"):
        listNotes()
    elif(command == "settings"):
        modifySettings(args.name, args.email)

    conn.commit()
    conn.close()


def addNote(note, category):
    cur.execute("INSERT INTO Notes (DESC,CAT) \
      VALUES (?, ?)", (note,category));
    print("Added note.")
    listNotes()



def modifySettings(name, email):
    cur.execute("UPDATE user_info SET NAME = ?, EMAIL = ? WHERE ID=1 ", (name, email))
    cur.execute("SELECT * FROM user_info")
    print(cur.fetchall())



def listNotes():
    cur.execute("SELECT * FROM Notes")
    print(cur.fetchall())


def delNote(id):
    cur.execute("DELETE FROM Notes WHERE ID=?", (id,))
    print("Deleted from Notes: note id {}".format(id))
    listNotes()

def addTask(task, due):
    cur.execute("INSERT INTO Notes (DESC,DUE) VALUES (?, ?)", (task,due));

def listTasks():
    pass



if __name__ == '__main__':
    main()
