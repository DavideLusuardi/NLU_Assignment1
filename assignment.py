import spacy
from spacy.symbols import nsubj, dobj, iobj

nlp = spacy.load("en_core_web_sm")

def path_to_token(token):
    """Extract the path from the ROOT to a specific token.
    
    Parameters
    ----------
    token : spacy.tokens.token.Token
    
    Returns
    -------
    list
        The list of dependency relations from the ROOT to the token
    """

    path = list()
    while token.head != token:
        path.append(token.dep_)
        token = token.head

    path.append(token.dep_)
    return path[::-1]


def extract_path(sentence):
    """Extract for each token a path of dependency relations from the ROOT to the token.    

    Parse the sentence to get a Doc object of spaCy.
    For each token find the path of dependency relations from the ROOT to the token.

    Parameters
    ----------
    sentence : str
        The sentence to be parsed and tokenized
    
    Returns
    -------
    dict
        A dict of lists of dependency relations with the tokens of the sentence as keys
    """

    # TODO: can be a DFS search
    doc = nlp(sentence)
    paths = dict()

    for token in doc:
        paths[token] = path_to_token(token)

    return paths

def extract_subtree(sentence):
    """Extract the subtree of each token in the sentence. 

    Parse the sentence to get a Doc object of spaCy.
    For each token find its subtree.

    Parameters
    ----------
    sentence : str
        The sentence to be parsed and tokenized
    
    Returns
    -------
    dict
        A dict of lists of tokens representing the subtree with the tokens of the sentence as keys
    """

    doc = nlp(sentence)
    subtrees = dict()

    for token in doc:
        subtrees[token] = list(token.subtree)

    return subtrees

def check_subtree(sentence, words):
    """Check if the given list of words forms a subtree in the dependency graph of the sentence.

    Parameters
    ----------
    sentence : str
        The sentence to be parsed and tokenized
    words : list
        A list of strings representing the list of tokens
    
    Returns
    -------
    bool
    """

    subtrees = extract_subtree(sentence)

    for st in subtrees.values():
        if len(st) != len(words):
            continue

        subtree_found = True
        for token, word in zip(st, words):
            if token.text != word:
                subtree_found = False
                break
        
        if subtree_found:
            return True
    
    return False
    

def get_head(span):
    """Get the head of the span.

    Parse the span to get a Doc object of spaCy.
    Find the head of the span.

    Parameters
    ----------
    span : str
        The span to be parsed and tokenized
    
    Returns
    -------
    spacy.tokens.token.Token
        The head of the span
    """

    doc = nlp(span)
    for token in doc:
        if token.head == token:
            return token
    
    return None # error


def extract_nsubj_dobj_iobj(sentence):
    """Extract sentence subject (nsubj), direct object (dobj) and indirect object (iobj) spans.

    Parameters
    ----------
    sentence : str
        The sentence to be parsed and tokenized
    
    Returns
    -------
    dict
        A dictionary containing for each key (subject, direct object and indirect object) a list of spans.
        If for example there are more subjects in the sentence, the entry "nsubj" will be a list containing 
        all the subject spans.
    """

    doc = nlp(sentence)
    spans = {"nsubj":[], "dobj":[], "iobj":[]}
    
    for token in doc:
        if token.dep == nsubj:
            spans["nsubj"].append(list(token.subtree))
        if token.dep == dobj:
            spans["dobj"].append(list(token.subtree))
        if token.dep == iobj or token.dep_ == "dative": # depends on spaCy version
            spans["iobj"].append(list(token.subtree))

    return spans

    

if __name__ == "__main__":
    # testing of the implemented functions

    def display(sentence):
        from spacy import displacy
        doc = nlp(sentence)
        displacy.serve(doc, style="dep")

    example = 'I saw the man with a telescope.'
    print(check_subtree(example, "with a telescope".split()))

    # display(example)

    test_sentences = [
        "I saw the man with a telescope.",
        "Joe waited for the train.",
        "Mary and Samantha arrived at the bus station early but waited until noon for the bus.",
        "I looked for Mary and Samantha at the bus station, but they arrived at the station before noon and left on the bus before I arrived.",
        "Because Mary and Samantha arrived at the bus station before noon, I did not see them at the station.",
        "While he waited at the train station, Joe realized that the train was late.",
        "After they left on the bus, Mary and Samantha realized that Joe was waiting at the train station.",
        "Sue passed Ann the ball.",
        "The teacher gave the class some homework.",
        "I read her the letter."
    ]

    for sentence in test_sentences:
        print("\n"+"-"*150)
        print(sentence)
        print("-"*150)

        print("PATHS TO TOKENS: ", extract_path(sentence))
        print("SUBTREES: ", extract_subtree(sentence))
        print("HEAD: ", get_head(sentence))
        print(extract_nsubj_dobj_iobj(sentence))
