# -*- coding: utf-8 -*-

from flask import Flask, request, render_template
from jumbodb import Jumbo
import json
import random
import requests
from pprint import pprint

# initializes flask app:
app = Flask(__name__, template_folder='templates')

@app.route('/', methods=["GET", "POST"])
def load_page():
    search_query = ""
    if request.method == 'POST':
        search_query = request.form.get("search_query", None)

    def query_database(search_query):
        jdb = Jumbo()
        term = jdb.wikipedia.search("wikipedia_docs_full", query={"match": {"content": f"{search_query}"}})
        return term

    if search_query:
        value_from_database = query_database(search_query)

        if len(value_from_database["hits"]["hits"]) == 0:
            return render_template('website.html', search_query="No Results Found.")

        results = []
        resultString = ""

        for value in value_from_database["hits"]["hits"]:
            results.append(value["_source"])
            resultString += json.dumps(value["_source"]) + "<br><br>"
        return render_template('website.html', search_query=resultString.encode('utf-8'))

    return render_template('website.html')

if __name__ == "__main__":
    app.debug = True
    app.run(port=5060)
