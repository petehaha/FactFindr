import spacy

nlp = spacy.load("en_core_web_sm")

def query_preprocessing_title(search_query, nlp):
    doc = nlp(search_query)

    # pulling out entities will help with title search
    entity_array = []
    for ent in doc.ents:
        entity_array.append(ent.text)
    print(entity_array)
    return entity_array