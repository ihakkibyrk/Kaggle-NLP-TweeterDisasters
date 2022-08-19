def clean_text(result):
    import re
    '''
    Cleans the text (in str format)
    '''
    # Remove URLs
    result = re.sub(r'http\S+','',result.lower())
    result = re.sub(r'http','',result)
    # Remove websites
    result = re.sub(r'www\S+','',result)
    # Covert standalone 'nt' to 'not'
    result = re.sub("n\'t", ' not ', result)
    # Remove emails
    result = re.sub(r'([a-zA-Z0-9_.+-]+)@([a-zA-Z0-9_.+-]+)\.([a-zA-Z0-9_.+-]+)','', result)
    # Remove punctuation
    result = re.sub(r'!|"|#|\$|%|&|:|;|-|^|\*|,|\(|\)|\[|\]|@|\.|\'|=|>|=>|<|=<|\?|\/|\||\+|=/','',result)
    result = re.sub(r'_|__',' ',result)
    # Remove xxx words
    result = re.sub(r'x{2,}','',result)
    # Remove nonsense words
    result = re.sub(r'û_|û_ ûó|û|û÷|ûª|åê|ûó|û||û|û|ª','',result)

    # Remove sequences of numbers mixed with letters - eg. USD50
    result = re.sub(r'[a-z]{1,}[0-9]{1,}[\/,:.-]{0,2}[0-9]{0,15}','',result, flags=re.IGNORECASE)
    # Remove sequences of numbers mied with letter - eg. 50 USD
    result = re.sub(r'[0-9]{1,}[\/,:.-]{0,2}[0-9]{0,15}[a-z]{1,3}', '', result, flags=re.IGNORECASE) 
    # Remove sequences of time
    result = re.sub(r'\s([0-9]{1,4}[\/,:.-][0-9]{1,4}\s?(?:AM|PM|am|pm))', '', result) 
    # Remove sequnces only
    result = re.sub(r'\s([0-9]{1,4}\s?(?:AM|PM|am|pm))', '', result) 
    # Remove sequences of data or time only numbers
    result = re.sub(r'[0-9]{1,4}[\/,:.-][0-9]{1,4}[\/,:.-]{0,1}[0-9]{1,4}', '', result) 
    # Remove standalone digits longer than 1
    result = re.sub(r'[0-9]{1,20}', '', result) 
    # Remove 1 & 2 letter words
    result = re.sub(r'\b[a-z]{1,2}\b', '', result)
    # Remove sequences of white spaces always in the last step
    result = re.sub(r'\s+',' ', result)

    return result.strip()

# Define function for lemmatization
def spacy_lemmatizer(text, nlp, stopwords, remove_stopwords=True):
    '''
    Converts text(str) to a list of lemmas without pronon and punct.
    It is also possible to remove the stopwords.

    text - text in str format
    nlp - language model from spacy created with spacy load()
    stopwords - list of stopwords
    
    '''

    doc = nlp(text)
    lemmas = [token.lemma_.lower() for token in doc if not
                (token.is_punct or token.is_digit or token.lemma_ == '-PRON-')]

    if remove_stopwords:
        lemmas = [lemma for lemma in lemmas if lemma not in stopwords]

    return lemmas

def remove_nonenglish(lemmas, corpus):
    '''
    Remove lemmas outside of the specified language corpus
    '''
    lemmas = [lemma for lemma in lemmas if lemma in corpus]
    return lemmas

# Function for finding words in lemmas
def keyword_finder_lemmas(lemmas, lexicon):
    '''
    Creates a list of keywords from lexicon appearing in the list of lemmas(list)
    '''
    keys = []
    for word in lexicon:
        if word in lemmas:
            keys.append(word)
    if len(keys) == 0:
        return []
    else:
        return keys


# Function for finding words in cleaned text
def keyword_finder_text(text, lexicon):
    '''
    Creates a list of keywords from lexicon appearing in the text (str)
    '''

    import re

    keys = []
    for word in lexicon:
        try:
            keys.append(re.search(word, text).group(0))
        except AttributeError:
            pass
    if len(keys) == 0:
        return []
    else:
        return keys
















