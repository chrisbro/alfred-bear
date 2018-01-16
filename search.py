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
        core.addToWorkflow(workflow, LOGGER, results)
    elif text == '':
        core.addRecent(workflow, LOGGER)
    else:
        titleResults = queries.search_notes_by_title(
            workflow, LOGGER, text)
        textResults =  queries.search_notes_by_text(
            workflow, LOGGER, text)
        results = []
        addUnique(results, titleResults)
        addUnique(results, textResults)
        core.addToWorkflow(workflow, LOGGER, results)

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

    LOGGER.debug('sys.argv: {!r}'.format(sys.argv))
    if len(sys.argv) > 1:
        query = sys.argv[1].strip()
        core.autocompleteTags(workflow, LOGGER, query)
        text, tags = core.separateTags(query)
        LOGGER.debug('tags: {!r}'.format(tags))
        LOGGER.debug('text: {!r}'.format(text))
        searchQuery(workflow, LOGGER, text, tags)

    workflow.send_feedback()

if __name__ == '__main__':
    WORKFLOW = Workflow(update_settings=UPDATE_SETTINGS)
    LOGGER = WORKFLOW.logger
    sys.exit(WORKFLOW.run(main))
