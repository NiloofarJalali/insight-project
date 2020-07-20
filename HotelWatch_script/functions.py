from lib import *

flatten = lambda l: [ item for sublist in l for item in sublist ]


def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations

def spacy_root(text):
        nlp = spacy.load("en_core_web_sm")
        doc=[]
        l=[]
        for word in text:
            ss=nlp(word)
            for chunk in ss.noun_chunks:
                l.append(chunk.root.text)
        doc.append(l)
        return(doc)


def lemmatizer ( doc ):
    nlp = English()
    lp= spacy.load("en")
    # This takes in a doc of tokens from the NER and lemmatizes them.
    # Pronouns (like "I" and "you" get lemmatized to '-PRON-', so I'm removing those.
    doc = [ token.lemma_ for token in doc if token.lemma_ != '-PRON-' ]
    doc = u' '.join ( doc )
    return nlp.make_doc ( doc )


def remove_stopwords ( doc ):
    spacy_nlp = spacy.load ( 'en_core_web_sm' )
    spacy_stopwords = spacy.lang.en.stop_words.STOP_WORDS

    # for i in no_list:
    #     STOP_WORDS.add ( i )

    # for word in STOP_WORDS:
    #     lexeme = nlp.vocab[ word ]
    #     lexeme.is_stop = True

    tokens = [ token.text for token in doc if not token.is_stop and token.is_punct != True and len ( token ) >= 3 ]
    tokens = [ i.lower () for i in tokens ]
    return tokens




def compute_coherence_values ( dictionary , corpus , texts , limit , start , step ):
    coherence_values = [ ]
    model_list = [ ]
    for num_topics in range ( start , limit , step ):

        model = gensim.models.ldamodel.LdaModel ( corpus=corpus ,
                                                  id2word=dictionary ,
                                                  num_topics=num_topics ,
                                                  random_state=100 ,
                                                  update_every=1 ,
                                                  chunksize=100 ,
                                                  passes=10 ,
                                                  alpha='auto' ,
                                                  per_word_topics=True )
        model_list.append ( model )
        coherencemodel = CoherenceModel ( model=model , texts=texts , dictionary=dictionary , coherence='c_v' )
        coherence_values.append ( coherencemodel.get_coherence () )

    return model_list , coherence_values


# build a topic model

def format_topics_sentences ( ldamodel , corpus , texts ):
    sent_topics_df = pd.DataFrame ()

    # Get main topic in each document
    for i , row_list in enumerate ( ldamodel[ corpus ] ):
        row = row_list[ 0 ] if ldamodel.per_word_topics else row_list
        # print(row)
        row = sorted ( row , key=lambda x: (x[ 1 ]) , reverse=True )

        # Get the Dominant topic, Perc Contribution and Keywords for each document
        for j , (topic_num , prop_topic) in enumerate ( row ):
            if j == 0:  # => dominant topic
                wp = ldamodel.show_topic ( topic_num )
                topic_keywords = ", ".join ( [ word for word , prop in wp ] )
                sent_topics_df = sent_topics_df.append (
                    pd.Series ( [ int ( topic_num ) , round ( prop_topic , 4 ) , topic_keywords ] ) ,
                    ignore_index=True )
            else:
                break
    sent_topics_df.columns = [ 'Dominant_Topic' , 'Perc_Contribution' , 'Topic_Keywords' ]

    # Add original text to the end of the output
    contents = pd.Series ( texts )
    sent_topics_df = pd.concat ( [ sent_topics_df , contents ] , axis=1 )
    return (sent_topics_df)


def table_process(input_data):


        def sentiment_analyzer_scores(sentence):
            analyser = SentimentIntensityAnalyzer()
            score = analyser.polarity_scores(sentence)
            return("{}".format(str(score)))

        sentiment_eval=[sentiment_analyzer_scores(i) for i in input_data]
        sent_score=[ast.literal_eval(i) for i in  sentiment_eval]
        sent_table=pd.DataFrame(sent_score)
        sent_table['Document_No']=sent_table.index
        sent_table=sent_table[['compound','Document_No']]
        # table_sentiment=table_topic.merge(sent_table, on=['Document_No'])
        # table_sentiment.loc[table_sentiment.Topic_Name=="None" ,'compound']=0
        return(sent_table)
