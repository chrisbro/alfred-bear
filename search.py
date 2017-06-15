#!/usr/bin/python
# encoding: utf-8

import os
import sys
import argparse
import datetime
import sqlite3
from workflow import Workflow

#TODOs
# break queries out into separate file
# break SQL running out into separate file
# create class for the note and populate/return that to main script? seems heavy
# create note via create callback endpoint
# search notes via tag callback endpoint
# append/prepend text to note via append callback endpoint

DB_LOCATION = ("/Library/Containers/net.shinyfrog.bear/Data/Library/Application Support/net.shinyfrog.bear/database.sqlite")
MAS_DB_LOCATION = DB_LOCATION.replace('.dunno', '.dunno.MacAppStore')
# todo: need to figure out what the actual app store install location is

SINGLE_QUOTE = "'"
ESC_SINGLE_QUOTE = "''"
DB_KEY = 'db_path'

log = None

def main(wf):
  log.debug('Started workflow')
  args = parse_args()

  if args.query:
    query = args.query[0]
    log.debug("Searching notes for '{0}'".format(query))
    results = execute_search_query(args)

  if not results:
      wf.add_item('No search results found.')
  else:
    for result in results:
      log.debug(result)
      wf.add_item(title=result[1], arg=result[0], valid=True)

  wf.send_feedback()

def parse_args():
  parser = argparse.ArgumentParser(description="Search Bear Notes")
  parser.add_argument('query', type=unicode, nargs=argparse.REMAINDER, help='query string')

  log.debug(wf.args)
  args = parser.parse_args(wf.args)
  return args

def find_bear_db():
  home = os.path.expanduser("~")
  db = "{0}{1}".format(home, DB_LOCATION)
  mas = "{0}{1}".format(home, MAS_DB_LOCATION)

  if not os.path.isfile(db):
      log.debug("Bear db not found at {0}; using {1} instead".format(db, mas))
      db = mas
  elif os.path.isfile(mas):
      db_mod = mod_date(db)
      mas_mod = mod_date(mas)
      if db_mod < mas_mod:
          db = mas
      log.debug("Bear direct and MAS db's found; using {0} as it's newer "
                "(Direct {1} vs. MAS {2})".format(db, db_mod, mas_mod))

  log.debug(db)
  return db

def mod_date(filename):
  mtime = os.path.getmtime(filename)
  return datetime.datetime.fromtimestamp(mtime)

def execute_search_query(args):
  query = None
  if args.query:
    query = args.query[0]

    if SINGLE_QUOTE in query:
        query = query.replace(SINGLE_QUOTE, ESC_SINGLE_QUOTE)
    
  results = search_notes(query)
  return results

def search_notes(query):
    sqlQuery = "SELECT ZUNIQUEIDENTIFIER, ZTITLE FROM ZSFNOTE WHERE ZARCHIVED=0 AND ZTRASHED=0 AND lower(ZTITLE) LIKE lower('%{0}%')".format(query)
    #todo: search text as well as title, figure out best way to sort results
    return run_query(sqlQuery)

def run_query(sql):
  db_path = wf.stored_data(DB_KEY)
  if not db_path:
    db_path = find_bear_db()
    wf.store_data(DB_KEY, db_path)
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

if __name__ == '__main__':
  wf = Workflow()
  log = wf.logger
  sys.exit(wf.run(main))