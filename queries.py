#!/usr/bin/python
# encoding: utf-8

"""
Defines queries and execution functions for calling the Bear sqlite DB.
"""

import sqlite3
import os
import datetime

DB_LOCATION = (
    "/Library/Containers/net.shinyfrog.bear/Data/Library/Application Support/"
    "net.shinyfrog.bear/database.sqlite")
MAS_DB_LOCATION = DB_LOCATION.replace('.dunno', '.dunno.MacAppStore')
DB_KEY = 'db_path'
# todo: need to figure out what the actual app store install location is

NOTE_TITLE_SEARCH = (
    "SELECT "
    "   ZUNIQUEIDENTIFIER, ZTITLE "
    "FROM "
    "   ZSFNOTE "
    "WHERE "
    "ZARCHIVED=0 "
    "AND ZTRASHED=0 "
    "AND lower(ZTITLE) LIKE lower('%{0}%')")

NOTE_TAG_SEARCH = (
    "SELECT "
    "t.ZTITLE "
    "FROM "
    "ZSFNOTE n "
    "INNER JOIN Z_5TAGS nt ON n.Z_PK = nt.Z_5NOTES "
    "INNER JOIN ZSFNOTETAG t ON nt.Z_10TAGS = t.Z_PK "
    "WHERE "
    "n.ZARCHIVED=0 "
    "AND n.ZTRASHED=0 "
    "AND lower(t.ZTITLE) LIKE lower('%{0}%')")


def search_notes_by_title(workflow, log, query):
    """
    Searches for bear notes by the title of the note.
    """

    sql_query = NOTE_TITLE_SEARCH.format(query)
    return run_query(workflow, log, sql_query)


def search_notes_by_tag(workflow, log, query):
    """
    Searches for Bear notes by tag name.
    """

    sql_query = NOTE_TAG_SEARCH.format(query)
    return run_query(workflow, log, sql_query)


def run_query(workflow, log, sql):
    """
    Takes a SQL command, executes it, and returns the results.
    """

    db_path = workflow.stored_data(DB_KEY)
    if not db_path:
        db_path = find_bear_db(log)
        workflow.store_data(DB_KEY, db_path)
    else:
        log.debug(db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    log.debug(sql)
    cursor.execute(sql)
    results = cursor.fetchall()
    log.debug("Found {0} results".format(len(results)))
    cursor.close()
    return results

def find_bear_db(log):
    """
    Finds the correct Bear sqlite3 DB - either a Mac app store installation,
    or a normal installation. If both are present, it uses the one that was
    last modified.
    """

    home = os.path.expanduser("~")
    db_file = "{0}{1}".format(home, DB_LOCATION)
    mas_db_file = "{0}{1}".format(home, MAS_DB_LOCATION)

    if not os.path.isfile(db_file):
        log.debug(
            "Bear db not found at {0}; using {1} instead".format(db_file, mas_db_file))
        db_file = mas_db_file
    elif os.path.isfile(mas_db_file):
        db_mod = mod_date(db_file)
        mas_mod = mod_date(mas_db_file)
        if db_mod < mas_mod:
            db_file = mas_db_file
        log.debug("Bear direct and MAS db's found; using {0} as it's newer "
                  "(Direct {1} vs. MAS {2})".format(db_file, db_mod, mas_mod))

    log.debug(db_file)
    return db_file

def mod_date(filename):
    """
    Returns the last modified date of a file.
    """

    mtime = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(mtime)
