# -*- coding: utf-8 -*-

from flask import Flask, request, render_template
from jumbodb import Jumbo
import json
import random
import requests
from pprint import pprint

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/97.0.4692.99 Safari/537.36',
}

# initializes flask app:
app = Flask(__name__, template_folder='templates')

@app.route('/', methods=["GET", "POST"])
def load_page():

    def query_database(search_query):
        jdb = Jumbo()
        term = jdb.wikipedia.search("wikipedia_docs_full", query={"match": {"content": f"{search_query}"}})
        return term

    search_query = ""
    if request.method == 'POST':
        search_query = request.form.get("search_query", None)

    if search_query:  # This is run when the search query is changed
        value_from_database = query_database(search_query)

        if len(value_from_database["hits"]["hits"]) == 0:
            return render_template('website.html', search_query="No Results Found.".encode())

        results = []  # Contains all results displayed on the site in a list
        resultString = ""  # Contains `results` in string form for display on the website
        title = []  # Contains all titles of the Wiki pages
        pageViews = []  # Contains all page views of the Wiki pages, each index corresponds with each title.
        for index, value in enumerate(value_from_database["hits"]["hits"]):
            value = value["_source"]
            title.append(value["title"].replace(" ", "_"))

            # Query API for view counts
            wikipediaReturn = requests.get('https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/'
                         f'en.wikipedia/all-access/all-agents/{title[index]}/monthly/2021010100/2021123100', headers=headers)
            wikipediaReturn = json.loads(wikipediaReturn.text)

            pageViewCountForJanuary = wikipediaReturn["items"][0]["views"]
            pageViews.append(pageViewCountForJanuary)

            # Add view_count to the results
            value["view_count"] = pageViewCountForJanuary
            results.append(value)

            resultString += json.dumps(value) + "<br><br>"

        return render_template('website.html', search_query=resultString.encode())
    return render_template('website.html')

if __name__ == "__main__":
    app.debug = True
    app.run(port=5000)
