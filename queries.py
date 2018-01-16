#!/usr/bin/python
# encoding: utf-8

"""
Defines queries and execution functions for calling the Bear sqlite DB.
"""

import sqlite3
import os

DB_LOCATION_OLD = (
    "/Library/Containers/net.shinyfrog.bear/Data/Library/Application Support/"
    "net.shinyfrog.bear/database.sqlite")
DB_LOCATION = (
    "/Library/Containers/net.shinyfrog.bear/Data/Documents/Application Data/"
    "database.sqlite")
DB_KEY = 'db_path'

RECENT_NOTES = (
    "SELECT DISTINCT"
    "   ZUNIQUEIDENTIFIER, ZTITLE "
    "FROM "
    "   ZSFNOTE "
    "WHERE "
    "   ZARCHIVED=0 "
    "   AND ZTRASHED=0 "
    "ORDER BY "
    "   ZMODIFICATIONDATE DESC "
    "LIMIT 25")

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
    "   ZMODIFICATIONDATE DESC "
    "LIMIT 25")

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
    "   ZMODIFICATIONDATE DESC "
    "LIMIT 25")

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
    "   t.ZMODIFICATIONDATE DESC "
    "LIMIT 25")

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
    "   n.ZMODIFICATIONDATE DESC "
    "LIMIT 25")

NOTES_BY_TAG_AND_TITLE = (
    "SELECT DISTINCT"
    "   note.ZUNIQUEIDENTIFIER, note.ZTITLE "
    "FROM "
    "   ZSFNOTE note "
    "   INNER JOIN Z_5TAGS nTag ON note.Z_PK = nTag.Z_5NOTES "
    "   INNER JOIN ZSFNOTETAG tag ON nTag.Z_10TAGS = tag.Z_PK "
    "WHERE "
    "   note.ZARCHIVED=0 "
    "   AND note.ZTRASHED=0 "
    "   AND lower(tag.ZTITLE) LIKE lower('%{0}%')"
    "   AND lower(note.ZTITLE) LIKE lower('%{1}%')"
    "ORDER BY "
    "   note.ZMODIFICATIONDATE DESC "
    "LIMIT 25")

NOTES_BY_TAG_AND_TEXT = (
    "SELECT DISTINCT"
    "   note.ZUNIQUEIDENTIFIER, note.ZTITLE "
    "FROM "
    "   ZSFNOTE note "
    "   INNER JOIN Z_5TAGS nTag ON note.Z_PK = nTag.Z_5NOTES "
    "   INNER JOIN ZSFNOTETAG tag ON nTag.Z_10TAGS = tag.Z_PK "
    "WHERE "
    "   note.ZARCHIVED=0 "
    "   AND note.ZTRASHED=0 "
    "   AND lower(tag.ZTITLE) LIKE lower('%{0}%')"
    "   AND lower(note.ZTEXT) LIKE lower('%{1}%')"
    "ORDER BY "
    "   note.ZMODIFICATIONDATE DESC "
    "LIMIT 25")

NOTES_BY_2TAG_AND_TEXT = (
    "SELECT DISTINCT"
    "   note.ZUNIQUEIDENTIFIER, note.ZTITLE "
    "FROM "
    "   ZSFNOTE note "
    "   INNER JOIN Z_5TAGS nTag ON note.Z_PK = nTag.Z_5NOTES "
    "   INNER JOIN ZSFNOTETAG tag ON nTag.Z_10TAGS = tag.Z_PK "
    "WHERE "
    "   note.ZARCHIVED=0 "
    "   AND note.ZTRASHED=0 "
    "   AND (lower(tag.ZTITLE) = lower('{0}')"
    "   OR lower(tag.ZTITLE) = lower('{1}'))"
    "   AND lower(note.ZTEXT) LIKE lower('%{2}%')"
    "GROUP BY note.ZUNIQUEIDENTIFIER "
    "HAVING COUNT(*) >= 2 "
    "ORDER BY "
    "   note.ZMODIFICATIONDATE DESC "
    "LIMIT 25")

NOTES_BY_MULTI_TAG_AND_X = (
    "SELECT DISTINCT"
    "   note.ZUNIQUEIDENTIFIER, note.ZTITLE "
    "FROM "
    "   ZSFNOTE note "
    "   INNER JOIN Z_5TAGS nTag ON note.Z_PK = nTag.Z_5NOTES "
    "   INNER JOIN ZSFNOTETAG tag ON nTag.Z_10TAGS = tag.Z_PK "
    "WHERE "
    "   note.ZARCHIVED=0 "
    "   AND note.ZTRASHED=0 "
    "   AND ({0})"
    "   AND  {1} "
    "GROUP BY note.ZUNIQUEIDENTIFIER "
    "HAVING COUNT(*) >= {2} "
    "ORDER BY "
    "   note.ZMODIFICATIONDATE DESC "
    "LIMIT 25")

def buildMultiTagAndTitle(tags, text):
    tagWhereList = []
    for t in tags:
        s = "lower(tag.ZTITLE) = lower('{}')".format(t)
        tagWhereList.append(s)
    tagWhere = ' OR '.join(tagWhereList)
    titleWhere = "lower(note.ZTITLE) LIKE lower('%{}%')".format(text)
    tagCount = len(tags)
    sql_query = NOTES_BY_MULTI_TAG_AND_X.format(tagWhere, titleWhere, tagCount)
    return sql_query

def search_notes_by_multitag_and_title(workflow, log, tags, text):
    """
    Searches for Bear notes by multi-tag name and title.
    """
    sql_query = buildMultiTagAndTitle(tags, text)
    return run_query(workflow, log, sql_query)    

def buildMultiTagAndText(tags, text):
    tagWhereList = []
    for t in tags:
        s = "lower(tag.ZTITLE) = lower('{}')".format(t)
        tagWhereList.append(s)
    tagWhere = ' OR '.join(tagWhereList)
    textWhere = "lower(note.ZTEXT) LIKE lower('%{}%')".format(text)
    tagCount = len(tags)
    sql_query = NOTES_BY_MULTI_TAG_AND_X.format(tagWhere, textWhere, tagCount)
    return sql_query

def search_notes_by_multitag_and_text(workflow, log, tags, text):
    """
    Searches for Bear notes by multi-tag name and title.
    """
    sql_query = buildMultiTagAndText(tags, text)
    return run_query(workflow, log, sql_query)    

def list_recent(workflow, log):
    """
    Searches for Bear notes by the title of the note.
    """

    sql_query = RECENT_NOTES
    return run_query(workflow, log, sql_query)

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

    sql_query = TAGS_BY_TITLE.format(query)
    return run_query(workflow, log, sql_query)


def search_notes_by_tag_title(workflow, log, query):
    """
    Searches for Bear notes by tag name.
    """

    sql_query = NOTES_BY_TAG_TITLE.format(query)
    return run_query(workflow, log, sql_query)

def search_notes_by_tag_and_title(workflow, log, tag, title):
    """
    Searches for Bear notes by tag name and title.
    """
    sql_query = NOTES_BY_TAG_AND_TITLE.format(tag, title)
    return run_query(workflow, log, sql_query)    

def search_notes_by_tag_and_text(workflow, log, tag, text):
    """
    Searches for Bear notes by tag name and text.
    """
    sql_query = NOTES_BY_TAG_AND_TEXT.format(tag, text)
    return run_query(workflow, log, sql_query)    

def search_notes_by_2tag_and_text(workflow, log, tag1, tag2, text):
    """
    Searches for Bear notes by tag name and text.
    """
    sql_query = NOTES_BY_2TAG_AND_TEXT.format(tag1, tag2, text)
    return run_query(workflow, log, sql_query)    


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

    log.debug(db_file)
    return db_file
