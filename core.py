#!/usr/bin/python
# encoding: utf-8

"""
Core shared functions
"""

import queries

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
    return text.strip(), tags

def autocompleteTags(workflow, LOGGER, query):
    """
    populates workflow with autocompletes for tags
    """
    LOGGER.debug('autocompleteTags >> query: {!r}'.format(query))
    
    qItems = query.split()
    if len(qItems) > 0 and not query.endswith(' '):
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
                    valid=False)

def addToWorkflow(workflow, LOGGER, results):
    for r in results:
        LOGGER.debug(r)
        workflow.add_item(
            title=r[1], 
            subtitle="Open note", 
            arg=r[0], 
            valid=True)

def addRecent(workflow, LOGGER):
    recent_results = queries.list_recent(workflow, LOGGER)
    addToWorkflow(workflow, LOGGER, recent_results)