#!/usr/bin/python
# encoding: utf-8

"""
Note creation script for alfred-bear workflow.
"""

import sys
from urllib import quote
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

    title = query
    tags = extract_tags(query)
    tags_string = ', '.join(tags)
    title_string = strip_tags_from_string(tags, title)
    query_string = create_query_output(title, tags)
    LOGGER.debug(title_string)
    LOGGER.debug(query_string)
    if tags:
        workflow.add_item(title='Create note with title ' + title_string,
                          subtitle='Tags: ' + tags_string, arg=query_string, valid=True)
    else:
        workflow.add_item(title='Create note with title ' + title_string,
                          arg=query_string, valid=True)

    workflow.send_feedback()


def create_query_output(title, tags):
    """
    Generates what query parameters to pass to the Alfred callback step.
    """

    query_string = ''
    if title:
        query_string += 'title=' + quote(title)
        query_string += '&text=' + quote(title)

    if tags:
        tags_string = ''
        for tag in tags:
            tags_string += quote(tag) + ','
        query_string = strip_tags_from_string(tags, query_string)
        tags_string = tags_string[:-1]
        query_string += '&tags=' + tags_string

    LOGGER.debug(query_string)

    return query_string


def strip_tags_from_string(tags, query):
    """
    Yanks out all the hashtags from a string.
    """
    for tag in tags:
        query = query.replace(quote('#' + tag), '')
        query = query.replace('#' + tag, '')
    return query


def extract_tags(query):
    """
    Gets all the tags from the query.
    """
    return set(part[1:] for part in query.split() if part.startswith('#'))


if __name__ == '__main__':
    WORKFLOW = Workflow()
    LOGGER = WORKFLOW.logger
    sys.exit(WORKFLOW.run(main))
