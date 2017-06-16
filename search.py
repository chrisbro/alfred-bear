#!/usr/bin/python
# encoding: utf-8

import os
import sys
import argparse
import datetime
import queries
from workflow import Workflow

#TODOs
# break SQL running out into separate file
# create class for the note and populate/return that to main script? seems heavy
# create note via create callback endpoint
# search notes by tag
# append/prepend text to note via append callback endpoint

SINGLE_QUOTE = "'"
ESC_SINGLE_QUOTE = "''"

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

def execute_search_query(args):
  query = None
  if args.query:
    query = args.query[0]

    if SINGLE_QUOTE in query:
        query = query.replace(SINGLE_QUOTE, ESC_SINGLE_QUOTE)
    
  results = queries.search_notes_by_title(wf, log, query)
  return results

if __name__ == '__main__':
  wf = Workflow()
  log = wf.logger
  sys.exit(wf.run(main))