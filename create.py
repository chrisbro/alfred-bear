#!/usr/bin/python
# encoding: utf-8

"""
Note creation script for alfred-bear workflow.
"""

import sys
from workflow import Workflow

LOGGER = None


def main(workflow):
    """
    I'm just here so I don't get fined by pylint
    """

    LOGGER.debug('Started create workflow')
    query = workflow.args[0]
    LOGGER.debug(query)

    title = None
    tags = None

    if not '#' in query:
        title = query
        workflow.add_item(title='Create note with title ' + title, arg=title, valid=True)

    workflow.send_feedback()


if __name__ == '__main__':
    WORKFLOW = Workflow()
    LOGGER = WORKFLOW.logger
    sys.exit(WORKFLOW.run(main))
