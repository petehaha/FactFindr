import spacy

#initializes nlp
nlp = spacy.load("en_core_web_sm")


search_query = "Is Apple looking at buying a UK startup for $1 billion?"
def query_preprocessing_title(search_query, nlp):
     doc = nlp(search_query)
     
     #pulling out entities will help with title search
     #can query database for titles can include 1 or more elements of the array
     entity_array = []
     for ent in doc.ents:
        entity_array.append(ent.text) 
        print(entity_array)

query_preprocessing_title(search_query, nlp)


def query_preprocessing_content(search_query, nlp):
     doc = nlp(search_query)
     
     #turns each word in query into token (each token has property)
     #index each token
     #for token in doc:
             #token.text = word
             #token.pos = propn, aux, verb, noun
     
     #noun chunks help with content rephrasing
     for chunk in doc.noun_chunks:
        print(chunk.text)

#find all articles that have a title that is similar to apple

#content search - use noun chunks
query_preprocessing_content(search_query, nlp)