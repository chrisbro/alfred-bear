#!/usr/bin/python
# encoding: utf-8

"""
Note creation script for alfred-bear workflow.
"""

import sys
from urllib import quote
from workflow import Workflow, ICON_SYNC

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

    LOGGER.debug('Started create workflow')
    query = workflow.args[0]
    LOGGER.debug(query)

    tags = extract_tags(query)
    tags_string = ', '.join(tags)
    title_string = strip_tags_from_string(tags, query)
    query_string = create_query_output(query, tags)
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
        query_string += 'title=' + quote(title.encode('utf-8'))
        query_string += '&text=' + quote(title.encode('utf-8'))

    if tags:
        tags_string = ''
        for tag in tags:
            tags_string += quote(tag.encode('utf-8')) + ','
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
        query = query.replace(quote('#' + tag.encode('utf-8')), '')
        query = query.replace('#' + tag, '')
    return query


def extract_tags(query):
    """
    Gets all the tags from the query.
    """
    return set(part[1:] for part in query.split() if part.startswith('#'))


if __name__ == '__main__':
    WORKFLOW = Workflow(update_settings=UPDATE_SETTINGS)
    LOGGER = WORKFLOW.logger
    sys.exit(WORKFLOW.run(main))
