import spacy


# To process the text, we're using the small English model, which was trained
# on a corpus of general-purpose news and web text. See here for details:
# https://spacy.io/models/en#en_core_web_sm
nlp = spacy.load("en_core_web_sm")

# Here's our original text that we want to rephrase.
text = "How many times did Russia invade Ukraine?"

# This is the template we want to fill based on the original text. The subject
# of the original sentence becomes an object attached to "love".
template_how_many = "{subject} {verb} {obj} {noun}"
#template = "Couldn't agree more, but I would add that I sincerely love {subject}, because {pronoun} {verb} {obj}."

# Calling the nlp object on a string of text returns a processed Doc object,
# which gives us access to the individual tokens (words, punctuation) and their
# linguistic annotations (part-of-speech tags, dependency labels) predicted
# by the statistical model. See here for the visualization:
# https://explosion.ai/demos/displacy?text=These%20generously%20buttered%20noodles%2C%20sprinkled%20with%20just%20a%20quarter%20cup%20of%20parsley%20for%20color%20and%20freshness%2C%20are%20the%20perfect%20blank%20canvas%20for%20practically%20any%20stew%20or%20braise&model=en_core_web_sm&cpu=0&cph=0
doc = nlp(text)

def get_root(doc):
    # Based on a processed document, we want to find the syntactic root of the
    # sentence. For this example, that should be the verb "are".
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
    # We also need to look for the object attached to the root. In this case,
    # the dependency parser predicted the object we're looking for ("canvas")
    # as "attr" (attribute), so we're using that. There are various other
    # options, though, so if you want to generalise this script, you'd probably
    # want to check for those as well.
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
    # Here, we are getting the subtree of a token – for example, if we know
    # that "noodles" is the subject, we can resolve it to the full phrase
    # "These generously buttered noodles, sprinkled with just a quarter cup of
    # parsley for color and freshness".

    # spaCy preserves the whitespace following a token in the `text_with_ws`
    # attribute. This means you'll alwas be able to restore the original text.
    # For example: "Hello world!" (good) vs. "Hello world !" (bad).
    subtree = [t.text_with_ws for t in token.subtree]
    subtree = "".join(subtree)

    # Since our template will place the subject and object in the middle of a
    # sentence, we also want to make sure that the first token starts with a
    # lowercase letter – otherwise we'll end up with things like "love These".
    subtree = subtree[0].lower() + subtree[1:]
    return subtree


# Let's put this all together!
root = get_root(doc)
print("Root:", root)

subject = get_subject(root)
print("Subject:", subject)

subject_pronoun = get_pronoun(subject)
print("Subject pronoun:", subject_pronoun)

obj = get_object(root)
print("Object:", obj)

noun = get_noun(root)
print("Noun:", noun)

subject_subtree = get_subtree(subject)
print("Subject subtree:", subject_subtree)

object_subtree = get_subtree(obj)
print("Object subtree:", object_subtree)

noun_subtree = get_subtree(noun)
print("Noun subtree:", noun_subtree)

print("Result:")
print(
    template_how_many.format(
        subject=subject_subtree,
        pronoun=subject_pronoun,
        verb=root.text,
        obj=object_subtree,
        noun=noun,
    )
)