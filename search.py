#!/usr/bin/python
# encoding: utf-8

"""
Main search script for alfred-bear workflow.
"""

import sys
import argparse
import queries
import core
from workflow import Workflow, ICON_SYNC

TITLE = "i"
TAGS = "a"

SINGLE_QUOTE = "'"
ESC_SINGLE_QUOTE = "''"

LOGGER = None

# Update workflow from GitHub repo
UPDATE_SETTINGS = {'github_slug': 'chrisbro/alfred-bear'}
SHOW_UPDATES = True

def separateTags(query):
    textList = []
    tags = set([])
    items = query.split()
    for i in items:
        if i.startswith('#'):
            tags.add(i[1:])
        else:
            textList.append(i)
    text = ' '.join(textList)
    return text, tags

def addToWorkflow(workflow, results):
    for r in results:
        LOGGER.debug(r)
        workflow.add_item(
            title=r[1], 
            subtitle="Open note", 
            arg=r[0], 
            valid=True)

def addUnique(results, newResults):
    for r in newResults:
        if r not in results:
            results.append(r)
    return results

def searchQuery(workflow, LOGGER, text, tags):
    if len(tags) != 0:
        LOGGER.debug("Multi Tag Search")
        results = []
        tags = list(tags)
        titleResults = queries.search_notes_by_multitag_and_title(
                workflow, LOGGER, tags, text)
        textResults = queries.search_notes_by_multitag_and_text(
                workflow, LOGGER, tags, text)
        addUnique(results, titleResults)
        addUnique(results, textResults)
        addToWorkflow(workflow, results)
    else:
        titleResults = queries.search_notes_by_title(
            workflow, LOGGER, text)
        textResults =  queries.search_notes_by_text(
            workflow, LOGGER, text)
        results = []
        addUnique(results, titleResults)
        addUnique(results, textResults)
        addToWorkflow(workflow, results)

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
        core.autocompleteTags(workflow, LOGGER, query)
        text, tags = separateTags(query)
        LOGGER.debug('tags: {!r}'.format(tags))
        LOGGER.debug('text: {!r}'.format(text))
        searchQuery(workflow, LOGGER, text, tags)

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

if __name__ == '__main__':
    WORKFLOW = Workflow(update_settings=UPDATE_SETTINGS)
    LOGGER = WORKFLOW.logger
    sys.exit(WORKFLOW.run(main))
