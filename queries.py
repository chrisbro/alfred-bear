#!/usr/bin/python
# encoding: utf-8

"""
Defines queries and execution functions for calling the Bear sqlite DB.
"""

import sqlite3
import os

DB_LOCATION_OLD_OLD = (
    "/Library/Containers/net.shinyfrog.bear/Data/Library/Application Support/"
    "net.shinyfrog.bear/database.sqlite")
DB_LOCATION_OLD = (
    "/Library/Containers/net.shinyfrog.bear/Data/Documents/Application Data/"
    "database.sqlite")
DB_LOCATION = (
    "/Library/Group Containers/9K33E3U3T4.net.shinyfrog.bear/Application Data/"
    "database.sqlite")
DB_KEY = 'db_path'

NOTES_BY_TITLE = (
    "SELECT DISTINCT"
    "   ZUNIQUEIDENTIFIER, ZTITLE "
    "FROM "
    "   ZSFNOTE "
    "WHERE "
    "   ZARCHIVED=0 "
    "   AND ZTRASHED=0 "
    "   AND lower(ZTITLE) LIKE lower('%{0}%')"
    "ORDER BY "
    "   ZMODIFICATIONDATE DESC")

NOTES_BY_TEXT = (
    "SELECT DISTINCT"
    "   ZUNIQUEIDENTIFIER, ZTITLE "
    "FROM "
    "   ZSFNOTE "
    "WHERE "
    "   ZARCHIVED=0 "
    "   AND ZTRASHED=0 "
    "   AND lower(ZTEXT) LIKE lower('%{0}%')"
    "ORDER BY "
    "   ZMODIFICATIONDATE DESC"
)

TAGS_BY_TITLE = (
    "SELECT DISTINCT"
    "   t.ZTITLE "
    "FROM "
    "   ZSFNOTE n "
    "   INNER JOIN Z_5TAGS nt ON n.Z_PK = nt.Z_5NOTES "
    "   INNER JOIN ZSFNOTETAG t ON nt.Z_10TAGS = t.Z_PK "
    "WHERE "
    "   n.ZARCHIVED=0 "
    "   AND n.ZTRASHED=0 "
    "   AND lower(t.ZTITLE) LIKE lower('%{0}%')"
    "ORDER BY "
    "   t.ZMODIFICATIONDATE DESC")

TAGS_BY_TITLE_V6 = (
    "SELECT DISTINCT"
    "   t.ZTITLE "
    "FROM "
    "   ZSFNOTE n "
    "   INNER JOIN Z_6TAGS nt ON n.Z_PK = nt.Z_6NOTES "
    "   INNER JOIN ZSFNOTETAG t ON nt.Z_13TAGS = t.Z_PK "
    "WHERE "
    "   n.ZARCHIVED=0 "
    "   AND n.ZTRASHED=0 "
    "   AND lower(t.ZTITLE) LIKE lower('%{0}%')"
    "ORDER BY "
    "   t.ZMODIFICATIONDATE DESC")

TAGS_BY_TITLE_V7 = (
    "SELECT DISTINCT"
    "   t.ZTITLE "
    "FROM "
    "   ZSFNOTE n "
    "   INNER JOIN Z_7TAGS nt ON n.Z_PK = nt.Z_7NOTES "
    "   INNER JOIN ZSFNOTETAG t ON nt.Z_14TAGS = t.Z_PK "
    "WHERE "
    "   n.ZARCHIVED=0 "
    "   AND n.ZTRASHED=0 "
    "   AND lower(t.ZTITLE) LIKE lower('%{0}%')"
    "ORDER BY "
    "   t.ZMODIFICATIONDATE DESC")

NOTES_BY_TAG_TITLE = (
    "SELECT DISTINCT"
    "   n.ZUNIQUEIDENTIFIER, n.ZTITLE "
    "FROM "
    "   ZSFNOTE n "
    "   INNER JOIN Z_5TAGS nt ON n.Z_PK = nt.Z_5NOTES "
    "   INNER JOIN ZSFNOTETAG t ON nt.Z_10TAGS = t.Z_PK "
    "WHERE "
    "   n.ZARCHIVED=0 "
    "   AND n.ZTRASHED=0 "
    "   AND lower(t.ZTITLE) LIKE lower('%{0}%')"
    "ORDER BY "
    "   n.ZMODIFICATIONDATE DESC")

NOTES_BY_TAG_TITLE_V6 = (
    "SELECT DISTINCT"
    "   n.ZUNIQUEIDENTIFIER, n.ZTITLE "
    "FROM "
    "   ZSFNOTE n "
    "   INNER JOIN Z_6TAGS nt ON n.Z_PK = nt.Z_6NOTES "
    "   INNER JOIN ZSFNOTETAG t ON nt.Z_13TAGS = t.Z_PK "
    "WHERE "
    "   n.ZARCHIVED=0 "
    "   AND n.ZTRASHED=0 "
    "   AND lower(t.ZTITLE) LIKE lower('%{0}%')"
    "ORDER BY "
    "   n.ZMODIFICATIONDATE DESC")

NOTES_BY_TAG_TITLE_V7 = (
    "SELECT DISTINCT"
    "   n.ZUNIQUEIDENTIFIER, n.ZTITLE "
    "FROM "
    "   ZSFNOTE n "
    "   INNER JOIN Z_7TAGS nt ON n.Z_PK = nt.Z_7NOTES "
    "   INNER JOIN ZSFNOTETAG t ON nt.Z_14TAGS = t.Z_PK "
    "WHERE "
    "   n.ZARCHIVED=0 "
    "   AND n.ZTRASHED=0 "
    "   AND lower(t.ZTITLE) LIKE lower('%{0}%')"
    "ORDER BY "
    "   n.ZMODIFICATIONDATE DESC")


def search_notes_by_title(workflow, log, query):
    """
    Searches for Bear notes by the title of the note.
    """

    sql_query = NOTES_BY_TITLE.format(query)
    return run_query(workflow, log, sql_query)


def search_notes_by_text(workflow, log, query):
    """
    Searches for Bear notes by the content of the note.
    """

    sql_query = NOTES_BY_TEXT.format(query)
    return run_query(workflow, log, sql_query)


def search_tags_by_title(workflow, log, query):
    """
    Searches for Bear tags by tag name.
    """

    sql_query = TAGS_BY_TITLE_V6.format(query)

    home = os.path.expanduser("~")
    if find_bear_db(log) == "{0}{1}".format(home, DB_LOCATION_OLD):
        sql_query = TAGS_BY_TITLE.format(query)

    try:
        results = run_query(workflow, log, sql_query)
    except:
        sql_query = TAGS_BY_TITLE_V7.format(query)
        results = run_query(workflow, log, sql_query)
    return results


def search_notes_by_tag_title(workflow, log, query):
    """
    Searches for Bear notes by tag name.
    """

    sql_query = NOTES_BY_TAG_TITLE_V6.format(query)

    home = os.path.expanduser("~")
    if find_bear_db(log) == "{0}{1}".format(home, DB_LOCATION_OLD):
        sql_query = NOTES_BY_TAG_TITLE.format(query)

    try:
        results = run_query(workflow, log, sql_query)
    except:
        sql_query = NOTES_BY_TAG_TITLE_V7.format(query)
        results = run_query(workflow, log, sql_query)
    return results


def run_query(workflow, log, sql):
    """
    Takes a SQL command, executes it, and returns the results.
    """

    db_path = workflow.stored_data(DB_KEY)
    home = os.path.expanduser("~")
    if db_path and db_path == "{0}{1}".format(home, DB_LOCATION_OLD):
        db_path = find_bear_db(log)
        workflow.store_data(DB_KEY, db_path)
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
    Finds the Bear sqlite3 DB.
    """

    home = os.path.expanduser("~")
    db_file = "{0}{1}".format(home, DB_LOCATION)

    if not os.path.isfile(db_file):
        log.debug(
            "Bear db not found at {0}".format(db_file))
        db_file = "{0}{1}".format(home, DB_LOCATION_OLD)
        if not os.path.isfile(db_file):
            log.debug(
                "Bear db not found at {0}".format(db_file))
            db_file = "{0}{1}".format(home, DB_LOCATION_OLD_OLD)
            if not os.path.isfile(db_file):
                log.debug(
                    "Bear db not found at {0}".format(db_file))

    log.debug(db_file)
    return db_file
