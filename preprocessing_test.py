import spacy
from spacy.tokenizer import Tokenizer

# initializes nlp
nlp = spacy.load("en_core_web_sm")

# sample search query
search_query = "How many times did Russia invade Ukraine?"

#-------------------------------------------------------------------------
# preprocesses query for title search
# returns an array of entities
# title must contain 1 or more elements in this array?
def query_preprocessing_title(search_query, nlp):
     doc = nlp(search_query)
     
     # pulling out entities will help with title search
     entity_array = []
     for ent in doc.ents:
        entity_array.append(ent.text) 
     print(entity_array)
     return entity_array

query_preprocessing_title(search_query, nlp)

#-------------------------------------------------------------------------
# only allows valid tokens which are not stop words and punctuation symbols
def is_token_allowed(token):
        if token.is_stop or token.is_punct:
                return False
        return True

#-------------------------------------------------------------------------
# reduces token to its lowercase lemma form
def preprocess_token(token):
        return token.lemma_.strip().lower()

#-------------------------------------------------------------------------
# returns a dictionary of tokens mapped to their indexes (helps with keeping
# track of word placement in sentences)
def token_index_dict(search_query, nlp):
        doc = nlp(search_query)
        token_index_dict = {}
        idx = 0
        for token in doc:
                if is_token_allowed(token):
                     preprocessed_token = preprocess_token(token)
                     token_index_dict[preprocessed_token] = idx
                     idx = idx + 1
        print(token_index_dict)
        return token_index_dict

token_index_dict(search_query, nlp)

#-------------------------------------------------------------------------
# preprocessing query for content search
# returns a string of valid tokens 
def query_preprocessing_content(search_query, nlp):
     doc = nlp(search_query)
     
     #array of valid tokens
     valid_token_array = []

     for token in doc:
             
             #if preprocessed_token is 'where'
             if is_token_allowed(token):
                     preprocessed_token = preprocess_token(token)
                     valid_token_array.append(preprocessed_token)

     #turns valid token array into string
     to_string =' '.join([str(item) for item in valid_token_array])
     print(to_string)


     #for token in doc:
             #token.text = word
             #token.pos = propn, aux, verb, noun
     
     #noun chunks help with content rephrasing
     chunk_array = []
     for chunk in doc.noun_chunks:
        chunk_array.append(chunk.text)
     #print(chunk_array)
        




#find all articles that have a title that is similar to apple

#content search - use noun chunks
query_preprocessing_content(search_query, nlp)