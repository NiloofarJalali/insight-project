from lib import *
from functions import *








nlp.add_pipe ( lemmatizer , name='lemmatizer' )
nlp.add_pipe ( remove_stopwords , name="stopwords" , last=True )
nlp.add_pipe ( spacy_root , name='root' )