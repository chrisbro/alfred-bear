#!/usr/bin/python
# encoding: utf-8

"""
Core shared functions
"""

import queries

def autocompleteTags(workflow, LOGGER, query):
    """
    populates workflow with autocompletes for tags
    """
    qItems = query.split()
    last = qItems[-1]
    if last.startswith('#'):
        tag_results = queries.search_tags_by_title(workflow, LOGGER, last[1:])
        for t in tag_results:
            tag = '#'+t[0]
            # add final to the end of the query
            new_qItems = qItems[:-1]
            new_qItems.append(tag)
            complete = ' '.join(new_qItems) + ' '
            workflow.add_item(
                title=tag, 
                autocomplete=complete, 
                valid=True)
