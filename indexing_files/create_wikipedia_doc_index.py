########################################################################################
# Create Wikipedia Document Index
#
# This script takes in a set of articles that have been extracted from an official
# Wikipedia dump and writes to them to the specified index in the ElasticSearch database
# that is pointed to by the user's c3creds.json file.
#
# Author(s): Marko Sterbentz / C3 Lab
########################################################################################

import logging
import json
import plac
from tqdm import tqdm
from datetime import datetime
import elasticsearch.exceptions

from jumbodb import Jumbo

@plac.annotations(
    #instead of json, search through elastic search index of full wikipedia documents
    parent_index=('Index in the ElasticSearch database to pull dictionary from', 'positional', None, str),
    #this is the passages index we need to write to
    passages_index=('Index in the ElasticSearch database to write the file contents to', 'positional', None, str)
)
def main(parent_index: str,
         passages_index: str):

    # Set up the connection to JumboDB
    jdb = Jumbo(True)

    # Double check that we're connected to Jumbo, ElasticSearch database, and have access to the specified index
    assert passages_index in jdb.wikipedia.document_client.indices.get(index="*")

    # Setup the output / logging file
    log_filename = "error_log_" + datetime.now().strftime("%m_%d_%Y_%H_%M_%S") + ".log"
    logging.basicConfig(filename=log_filename, level=logging.ERROR)

    #Using Python's scroll APi to iterate through all documents in wikipedia full documents index
    def es_iterate_all_documents(es, parent_index, pagesize=250, scroll_timeout="1m", **kwargs):
    
        #Helper to iterate ALL values from a single index
        #Yields all the documents.
        is_first = True
        while True:
            # Scroll next
            if is_first: # Initialize scroll
                result = es.search(index=parent_index, scroll="1m", **kwargs, body={
                    "size": pagesize
                })
                is_first = False
            else:
                result = es.scroll(body={
                    "scroll_id": scroll_id,
                    "scroll": scroll_timeout
                })
            scroll_id = result["_scroll_id"]
            hits = result["hits"]["hits"]
            # Stop after no more docs
            if not hits:
                break
            # Yield each entry
            yield from (hit['_source'] for hit in hits)

    #iterate through each dict (single article) in wiki docs full index 
    for dict in es_iterate_all_documents(es, parent_index):
        title = dict.get("title")
        url = dict.get("url")
        content = dict.get("content")

        #1. break it up into passages (/n):
        #paragraph_split is an array of strings separated by "\n"
            #eg: content = "Hi\nHow are you\n doing Where\n are you"
            #    paragraph_split = ['Hi', 'How are you', ' doing Where', ' are you']
        paragraph_split = content.split("\n")

        #initialising new_dict - each element (passage) in passages index will be a dictionary
        new_dict = dict(id=None, title=None, url=None, content=None)
        
        #2. iterate through each of those passages (preprocessing)
        for passage in paragraph_split:
            id = 0
            #new_dict[id] = id
            new_dict[title] = title
            new_dict[url] = url

            #edit passage based on certain criteria??? preprocessing
            #find methods to make sure that the passage contains answer
            #as of now the only constraint is that a "\n" character denotes a new passage
            new_dict[content] = passage
            
            #3. Write the current file to the specified index
            jdb.wikipedia.create_document(passages_index, id, new_dict)
            id = id + 1

    # Iterate through each line/entry in the current file
    #with open(json_file) as f:
        #for line in tqdm(f):
            #try:
                # Note: Each line is a JSON dict
                #data = json.loads(line)

                #if data['text']:
                    #id = data['id']

                    #file_contents = {
                        #'title': data['title'],
                        #'url': data['url'],
                        #'content': data['text']
                    #}

                    # Write the current file to the specified index
                    #jdb.wikipedia.create_document(passages_index, id, file_contents)

            except elasticsearch.exceptions.ConflictError as e:
                # Ignore conflict errors (i.e. when the document already exists in the index)
                # TODO: May want to change this behavior in the future
                pass

            except Exception as e:
                logging.error('Error when trying to insert article {} | ID: {}'.format(data['title'], data['id']))
                logging.error(e)
                logging.error('============================================================\n')


if __name__ == "__main__":
   plac.call(main)