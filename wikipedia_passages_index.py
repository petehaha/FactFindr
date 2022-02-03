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
    json_file=('Path to the JSON file containing the extracted Wikipedia articles.', 'positional', None, str),
    index_name=('Index in the ElasticSearch database to write the file contents to', 'positional', None, str)
)
def main(json_file: str,
         index_name: str):

    # Set up the connection to JumboDB
    jdb = Jumbo(True)

    # Double check that we're connected to Jumbo, ElasticSearch database, and have access to the specified index
    assert index_name in jdb.wikipedia.document_client.indices.get(index="*")

    # Setup the output / logging file
    log_filename = "error_log_" + datetime.now().strftime("%m_%d_%Y_%H_%M_%S") + ".log"
    logging.basicConfig(filename=log_filename, level=logging.ERROR)

    # Iterate through each line/entry in the current file
    # pull articles from jumbo, for each article --> preprocess
    # iterate through IDs
    with open(json_file) as f:
        for line in tqdm(f):
            try:
                # Note: Each line is a JSON dict
                data = json.loads(line)

                if data['text']:
                    id = data['id']

                    file_contents = {
                        'title': data['title'],
                        'url': data['url'],
                        'content': data['text']
                    }

                    # Write the current file to the specified index
                    # same function for creating a new passage, create log to double check
                    jdb.wikipedia.create_document(index_name, id, file_contents)

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