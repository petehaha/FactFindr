import spacy


nlp = spacy.load("en_core_web_sm")

def preprocessing_title(search_query, nlp):
    doc = nlp(search_query)

    def get_root(doc):
        # Based on a processed document, we want to find the syntactic root of the
        # sentence (verb)
        for token in doc:
            if token.dep_ == "ROOT":
                return token

    def get_object(root):
        # We also need to look for the object attached to the root.
        for token in root.children:
            if token.dep_ == "dobj":
                return token

    def get_subtree(token):
        if token.subtree is not None:
            subtree = [t.text_with_ws for t in token.subtree]
            subtree = "".join(subtree)

            # Since our template will place the subject and object in the middle of a
            # sentence, we also want to make sure that the first token starts with a
            # lowercase letter
            subtree = subtree[0].lower() + subtree[1:]
        return subtree

    root = get_root(doc)
    obj = get_object(root)
    if obj is not None:
        object_subtree = get_subtree(obj)
        # print("Object subtree:", object_subtree)
    else:
        object_subtree = None


    template = search_query
     # TEMPLATE ANSWERS FOR WHO QUESTIONS
    substring_who = "who"
    substring_is = "is"
    template_who_did = "{obj}"

    if substring_who in search_query.lower() and substring_is not in search_query.lower():
        template = template_who_did
        template = template.format(obj=object_subtree)
        return template.split()
    else:
        # pulling out entities will help with title search
        entity_array = []
        for ent in doc.ents:
            entity_array.append(ent.text)
        # print(entity_array)
        return entity_array