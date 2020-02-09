from lib import *
from functions import *



def load_data ( path ):

    with open ( path , 'rb' ) as f:
        trip_ad = pickle.load ( f )
        Time_Table = trip_ad[ [ 'Date' , 'rating' ] ]
        # file_name = '/Users/niloofar/Documents/insight/data/cleaned/hotel2/doc_pos'
        input_data = list ( trip_ad[ 'Review' ] )
    return input_data , Time_Table




def process(input_data, no_list,time_table,start, limit, step,file_name,verbose):
    if verbose == True:
        nlp = spacy.load("en_core_web_sm")
        nlp = English ()
        nlp = spacy.load ( "en" )
        nlp.Defaults.stop_words.update ( stop_words )
        for i in no_list:
            STOP_WORDS.add ( i )
        for word in STOP_WORDS:
            lexeme = nlp.vocab[ word ]
            lexeme.is_stop = True

        nlp.add_pipe ( lemmatizer , name='lemmatizer' )
        nlp.add_pipe ( remove_stopwords , name="stopwords" , last=True )
        nlp.add_pipe ( spacy_root , name='root' )

        doc_list = [ ]
        for doc in tqdm ( input_data ):
            pr = nlp ( doc )
            doc_list.append ( pr )

        doc_curpus = [ flatten ( i ) for i in doc_list ]

        with open ( file_name , 'wb' ) as f:
            pickle.dump ( doc_curpus , f )


    else:

        with open ( file_name , 'rb' ) as f:
            doc_curpus = pickle.load ( f )

    words = corpora.Dictionary ( doc_curpus )
    corpus = [ words.doc2bow ( doc ) for doc in doc_curpus ]

    model_list , coherence_values = compute_coherence_values ( dictionary=words , corpus=corpus , texts=doc_curpus , start=start ,
                                                               limit=limit , step=step )
    opt = coherence_values.index ( max ( coherence_values ) )
    optimal_model = model_list[ opt ]

    df_topic_sents_keywords = format_topics_sentences ( ldamodel=optimal_model , corpus=corpus , texts=input_data )

    # Format
    df_dominant_topic = df_topic_sents_keywords.reset_index ()
    df_dominant_topic.columns = [ 'Document_No' , 'Dominant_Topic' , 'Topic_Perc_Contrib' , 'Keywords' , 'Text' ]
    df_dominant_topic = df_dominant_topic.merge ( time_table , left_index=True , right_index=True )



    with open ( 'result/Topic' , 'wb' ) as f:
        pickle.dump (  df_dominant_topic , f )

    sentiment_table=table_process(input_data)

    with open ('result/sentiment_table' , 'wb' ) as f:
        pickle.dump ( sentiment_table , f )



    return df_dominant_topic, sentiment_table






if __name__ == '__main__':
    input_data,Time_Table=load_data ( path='data/trip_sentence')
    stop_words=['hotel','night','nothing','would','could','want','go','recommend','everything','be','was','good','ok','great','poor','miami','YVE',"friday","saturday",'monday','week','carlos','cruise']

    file_name = 'data/doc_pos'
    Topic,sentiment_table =process ( input_data= input_data , no_list=stop_words , time_table=Time_Table , start=3 ,
                      limit=15 , step=1 , file_name=file_name , verbose=False, )
