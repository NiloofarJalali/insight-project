from lib import *
from functions import *


def load_data(path):

        with open ( path, 'rb' ) as f:
            trip_ad = pickle.load ( f )
            Time_Table = trip_ad[ [ 'Date' , 'rating' ] ]
            # file_name = '/Users/niloofar/Documents/insight/data/cleaned/hotel2/doc_pos'
            input_data = list ( trip_ad[ 'Review' ] )
        return  input_data, Time_Table











