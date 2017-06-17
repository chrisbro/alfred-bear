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
        query_string = create_query_output(title, tags)
        workflow.add_item(title='Create note with title ' +
                          title, arg=query_string, valid=True)

    workflow.send_feedback()


def create_query_output(title, tags):
    """
    Generates what query parameters to pass to the Alfred callback step.
    """

    query_string = ''
    if title:
        query_string += 'title=' + title
        query_string += '&text=' + title
    if tags:
        query_string += '&tags=' + tags
    LOGGER.debug(query_string)

    return query_string


if __name__ == '__main__':
    WORKFLOW = Workflow()
    LOGGER = WORKFLOW.logger
    sys.exit(WORKFLOW.run(main))
