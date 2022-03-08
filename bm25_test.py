from rank_bm25 import BM25Okapi

passage_list = [
    "Hello there good man!",
    "It is quite windy in London",
    "How is the weather today?"
]

search_query = "windy London"
def bm25_passage(passage_list, search_query):
    tokenized_passage = [doc.split(" ") for doc in passage_list]

    bm25 = BM25Okapi(tokenized_passage)
    # <rank_bm25.BM25Okapi at 0x1047881d0>

    tokenized_query = search_query.split(" ")

    doc_scores = bm25.get_scores(tokenized_query)
    # array([0.        , 0.93729472, 0.        ])

    return bm25.get_top_n(tokenized_query, passage_list, n=1)
    # ['It is quite windy in London']

print(bm25_passage(passage_list, search_query))