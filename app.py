# -*- coding: utf-8 -*-

from flask import Flask, request, render_template
from jumbodb import Jumbo
from preproccessing.preprocessing_content import preprocessing_content
from preproccessing.preprocessing_title import preprocessing_title
from postprocessing.bm25 import bm25_passage
import json
import requests
import urllib.parse
import html
import spacy

nlp = spacy.load("en_core_web_sm")

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
        title_array = preprocessing_title(search_query, nlp)
        if len(title_array) == 1:
            title_str = title_array[0]
        else:
            title_str = "(" + ") AND (".join(title_array) + ")"
            # print("Title String:", title_str)

        content_array = preprocessing_content(search_query)
        if len(content_array) == 1:
            content_str = content_array[0]
        else:
            content_str = "(" + ") AND (".join(content_array) + ")"
        if title_str == "()":
            term = jdb.wikipedia.search("wikipedia_docs_full",
                                        query={"match": {"content": content_str}}  # Content Search
                                        )
        else:
            term = jdb.wikipedia.search("wikipedia_docs_full",
                                    query={"bool": {
                                        "must": {"match": {"content": content_str}},  # Content Search
                                        "must": {"query_string": {"query": title_str,  # Title Search
                                                                    "default_field": "title"}}
                                    }})

        return term

    search_query = ""
    if request.method == 'POST':
        search_query = request.form.get("search_query", None)
    search_query_orig=search_query
    # print('search query: ', search_query_orig)
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
                                           f'en.wikipedia/all-access/all-agents/{urllib.parse.quote_plus(html.unescape(title[index]))}/monthly/2021010100/2021123100',
                                           headers=headers)
            wikipediaReturn = json.loads(wikipediaReturn.text)

            pageViewCountForJanuary = wikipediaReturn["items"][0]["views"]
            pageViews.append(pageViewCountForJanuary)

            # Add view_count to the results
            value["view_count"] = pageViewCountForJanuary
            results.append(value)

        results = sorted(results, key = lambda i: i['view_count'],reverse=True)

        for value in results: 
            curr_title = (json.dumps(list(value.values())[0])).strip('\"')
            curr_link = (json.dumps(list(value.values())[1])).strip('\"')
            article = (list(value.values())[2])
            curr_body = split_article(article, search_query).strip('\"')

    

            resultString += f"""
            <div class="searchResult"> 
                <div class="title">
                    <a class="titleLink" href="{curr_link}" target="_blank">{curr_title}</a>
                    
                </div>
                <div class="articleBody">
                    {curr_body}
                </div>
            </div> <br><br>"""  
            

        return render_template('website.html', search_query=resultString.encode(), original_search=search_query_orig)
    return render_template('website.html')

def split_article(article, search_query):
        passage_string = " "

        article = (json.dumps(article))
        splitArticle = article.split('\\n')
        # for i in range(len (splitArticle) -2):
        #    ## if(splitArticle[i])
        #    print(splitArticle[i])
        #    if(len(splitArticle[i]) < 100 and len(splitArticle) > (i-2)):
        #        print('in splitting')
        #        print(splitArticle[i])
        #        splitArticle[i:i+2] = [''.join(splitArticle[i:i+2])] 
        #        print(splitArticle[i])
        #     #print('printing, ', len(splitArticle[i]))
        passage_list = bm25_passage(splitArticle, search_query)

        for passage in passage_list:
            passage_string += passage + "<br><br>"
        return passage_string

if __name__ == "__main__":
    app.debug = True
    app.run(port=5000)
