from rank_bm25 import BM25Okapi

passage_list = [
    "Hello there good man!",
    "It is quite windy in London",
    "How is the weather today?"
]

def bm25_passage(passage_list, search_query):
    tokenized_passage = [doc.split(" ") for doc in passage_list]

    bm25 = BM25Okapi(tokenized_passage)
    # <rank_bm25.BM25Okapi at 0x1047881d0>
