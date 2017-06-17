#!/usr/bin/python
# encoding: utf-8

"""
Main search script for alfred-bear workflow.
"""

import sys
import argparse
import queries
from workflow import Workflow, ICON_SYNC

TITLE = "i"
TAGS = "a"

SINGLE_QUOTE = "'"
ESC_SINGLE_QUOTE = "''"

LOGGER = None

# Update workflow from GitHub repo
UPDATE_SETTINGS = {'github_slug': 'chrisbro/alfred-bear'}
SHOW_UPDATES = True


def main(workflow):
    """
    I'm just here so I don't get fined by pylint
    """

    if SHOW_UPDATES and workflow.update_available:
        workflow.add_item('A new version is available',
                          'Action this item to install the update',
                          autocomplete='workflow:update',
                          icon=ICON_SYNC)

    LOGGER.debug('Started search workflow')
    args = parse_args()

    if args.query:
        query = args.query[0]
        LOGGER.debug("Searching notes for %s", format(query))
        results = execute_search_query(args)

    if not results:
        workflow.add_item('No search results found.')
    else:
        for result in results:
            LOGGER.debug(result)
            if args.type == TAGS:
                workflow.add_item(title=result[0], arg=result[0], valid=True)
            else:
                workflow.add_item(title=result[1], arg=result[0], valid=True)

    workflow.send_feedback()


def parse_args():
    """
    Parses out the arguments sent to the script in the Alfred workflow.
    """

    parser = argparse.ArgumentParser(description="Search Bear Notes")
    parser.add_argument('-t', '--type', default=TITLE,
                        choices=[TITLE, TAGS],
                        type=str, help='What to search for: t(i)tle, or t(a)gs?')
    parser.add_argument('query', type=unicode,
                        nargs=argparse.REMAINDER, help='query string')

    LOGGER.debug(WORKFLOW.args)
    args = parser.parse_args(WORKFLOW.args)
    return args


def execute_search_query(args):
    """
    Decides what search to run based on args that were passed in and executes the search.
    """
    query = None
    if args.query:
        query = args.query[0]

        if SINGLE_QUOTE in query:
            query = query.replace(SINGLE_QUOTE, ESC_SINGLE_QUOTE)

    if args.type == TAGS:
        LOGGER.debug('Searching tags')
        results = queries.search_notes_by_tag(WORKFLOW, LOGGER, query)
    else:
        LOGGER.debug('Searching tasks')
        results = queries.search_notes_by_title(WORKFLOW, LOGGER, query)
    return results


if __name__ == '__main__':
    WORKFLOW = Workflow(update_settings=UPDATE_SETTINGS)
    LOGGER = WORKFLOW.logger
    sys.exit(WORKFLOW.run(main))
