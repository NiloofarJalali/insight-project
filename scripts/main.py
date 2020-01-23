from lib import *
from functions import *

def process(input_data, no_list,time_table,start, limit, step,file_name,verbose)

    nlp = English ()
    lp = spacy.load ( "en" )
    nlp.Defaults.stop_words.update ( stop_words )

    for word in STOP_WORDS:
        lexeme = nlp.vocab[ word ]
        lexeme.is_stop = True
    nlp.add_pipe ( lemmatizer , name='lemmatizer' )
    nlp.add_pipe ( remove_stopwords , name="stopwords" , last=True )
    nlp.add_pipe ( spacy_root , name='root' )
    

    if verbose == True:

        doc_list = [ ]
        for doc in tqdm ( input_data ):
            pr = nlp ( doc )
            doc_list.append ( pr )

        dd = [ flatten ( i ) for i in doc_list ]

        with open ( file_name , 'wb' ) as f:
            pickle.dump ( dd , f )


    else:

        with open ( file_name , 'rb' ) as f:
            dd = pickle.load ( f )

    words = corpora.Dictionary ( dd )
    corpus = [ words.doc2bow ( doc ) for doc in dd ]

    model_list , coherence_values = compute_coherence_values ( dictionary=words , corpus=corpus , texts=dd , start=start ,
                                                               limit=limit , step=step )
    opt = coherence_values.index ( max ( coherence_values ) )
    optimal_model = model_list[ opt ]

    df_topic_sents_keywords = format_topics_sentences ( ldamodel=optimal_model , corpus=corpus , texts=input_data )

    # Format
    df_dominant_topic = df_topic_sents_keywords.reset_index ()
    df_dominant_topic.columns = [ 'Document_No' , 'Dominant_Topic' , 'Topic_Perc_Contrib' , 'Keywords' , 'Text' ]
    df_dominant_topic = df_dominant_topic.merge ( time_table , left_index=True , right_index=True )

    return (df_dominant_topic)

