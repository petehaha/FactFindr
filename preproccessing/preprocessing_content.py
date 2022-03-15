import spacy

nlp = spacy.load("en_core_web_sm")

#############################
def preprocessing_content(text):
    template = text

    # TEMPLATE ANSWERS FOR HOW QUESTIONS
    substring_how = "how"
    substring_many = "many"
    substring_old = "old"
    template_how_many = "{subject} {verb} {obj} {noun}"
    template_how_old = "{subject} {verb} years old"
    if substring_how in text.lower():
        if substring_many in text.lower():
            template = template_how_many
        if substring_old in text.lower():
            template = template_how_old

    # TEMPLATE ANSWERS FOR WHERE QUESTIONS
    substring_where = "where"
    substring_born = "born"
    template_where = "{subject} {verb} located"
    template_born = "{subject} was {verb}"
    if substring_where in text.lower():
        template = template_where
        if substring_born in text.lower():
            template = template_born

    # TEMPLATE ANSWERS FOR WHO QUESTIONS
    substring_who = "who"
    substring_is = "is"
    template_who_is = "{subject} {verb}"
    template_who_did = "{verb} {obj}"
    if substring_who in text.lower():
        template = template_who_did
        if substring_is in text.lower():
            template = template_who_is

    # TEMPLATE ANSWERS FOR WHY QUESTIONS
    substring_why = "why"
    template_why = "{subject} {verb} because"
    if substring_why in text.lower():
        template = template_why

    # Calling the nlp object on a string of text returns a processed Doc object,
    # which gives us access to the individual tokens (words, punctuation) and their
    # linguistic annotations (part-of-speech tags, dependency labels) predicted
    # by the statistical model. See here for the visualization:
    # https://explosion.ai/demos/displacy?text=These%20generously%20buttered%20noodles%2C%20sprinkled%20with%20just%20a%20quarter%20cup%20of%20parsley%20for%20color%20and%20freshness%2C%20are%20the%20perfect%20blank%20canvas%20for%20practically%20any%20stew%20or%20braise&model=en_core_web_sm&cpu=0&cph=0
    doc = nlp(text)

    def get_root(doc):
        # Based on a processed document, we want to find the syntactic root of the
        # sentence (verb)
        for token in doc:
            if token.dep_ == "ROOT":
                return token

    def get_subject(root):
        # If we know the root of the sentence, we can use it to find its subject.
        # Here, we're checking the root's children for a token with the dependency
        # label 'nsubj' (nominal subject).
        for token in root.children:
            if token.dep_ == "nsubj":
                return token

    def get_noun(root):
        for token in root.children:
            if token.dep_ == "pobj" or token.dep_ == "compound" or token.dep_ == "npadvmod":
                return token

    def get_object(root):
        # We also need to look for the object attached to the root.
        for token in root.children:
            if token.dep_ == "dobj":
                return token

    def get_pronoun(token):
        # Based on the subject token, we need to decide which pronoun to use.
        # For example, "noodle" would require "it", whereas "noodles" needs "they".
        # You might also just want to skip singular nouns alltogether and focus
        # on the plurals only, which are much simpler to deal with in English.

        # spaCy currently can't do this out-of-the-box, but there are other
        # rule-based or statistical systems that can do this pretty well. For
        # simplicity, we just mock this up here and always use "they".
        return "they"

    def get_subtree(token):
        if token.subtree is not None:
            subtree = [t.text_with_ws for t in token.subtree]
            subtree = "".join(subtree)

            # Since our template will place the subject and object in the middle of a
            # sentence, we also want to make sure that the first token starts with a
            # lowercase letter
            subtree = subtree[0].lower() + subtree[1:]
        return subtree

    # Let's put this all together!
    root = get_root(doc)
    # print("Root:", root)

    subject = get_subject(root)
    # print("Subject:", subject)

    subject_pronoun = get_pronoun(subject)
    # print("Subject pronoun:", subject_pronoun)

    obj = get_object(root)
    # print("Object:", obj)

    noun = get_noun(root)
    # print("Noun:", noun)

    if subject is not None:
        subject_subtree = get_subtree(subject).lower()
        # print("Subject subtree:", subject_subtree)
    else:
        subject_subtree = None

    if obj is not None:
        object_subtree = get_subtree(obj)
        # print("Object subtree:", object_subtree)
    else:
        object_subtree = None

    if noun is not None:
        noun_subtree = get_subtree(noun)
        # print("Noun subtree:", noun_subtree)
    else:
        noun_subtree = None

    # print("Result:")

    if template != text:
        template = template.format(subject=subject_subtree,
                                   pronoun=subject_pronoun,
                                   verb=root.text,
                                   obj=object_subtree,
                                   noun=noun)
    else:
        pass

    # print(template.split())

    return template.split()
