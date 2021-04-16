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
    print(words)

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
        A dict of lists of tokens representing the span for subject, direct object and indirect object
    """

    doc = nlp(sentence)
    spans = {"nsubj":[], "dobj":[], "iobj":[]}
    
    for token in doc:
        if token.dep == nsubj:
            spans["nsubj"] = list(token.subtree)
        if token.dep == dobj:
            spans["dobj"] = list(token.subtree)
        if token.dep == iobj:
            spans["iobj"] = list(token.subtree)

    return spans

    

if __name__ == "__main__":

    def display(sentence):
        from spacy import displacy
        doc = nlp(sentence)
        displacy.serve(doc, style="dep")

    example = 'I saw the man with a telescope.'
    print(extract_path(example))
    print(extract_subtree(example))
    print(check_subtree(example, "with a telescope".split()))
    print(extract_nsubj_dobj_iobj(example))

    # display(example)