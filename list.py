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

    LOGGER.debug('Started listing workflow')

    recent_results = queries.list_recent(WORKFLOW, LOGGER)

    for r in recent_results:
        LOGGER.debug(recent_results)
        WORKFLOW.add_item(title=r[1], subtitle="Open note",
                          arg=r[0], valid=True)

    workflow.send_feedback()

if __name__ == '__main__':
    WORKFLOW = Workflow(update_settings=UPDATE_SETTINGS)
    LOGGER = WORKFLOW.logger
    sys.exit(WORKFLOW.run(main))
