from lib import *



def scraping ( headers=headers , url_list , review_name , review_url , date_name , date_url , score_name , score_url ):
    def get_page ( url ):
        responce = requests.get ( url , headers=headers )
        soup = BeautifulSoup ( responce.text , 'lxml' )
        return soup

    Review_list = [ ]
    for u in url_list:
        soup = get_page ( u )
        review = soup.find_all ( review_name , class_=review_url )
    for i in range ( len ( review ) ):
        Review_list.append ( review[ i ].text )

    Review_Date = [ ]
    for u in url_list:
        soup = get_page ( u )
        review = soup.find_all ( date_name , class_=date_url )
    for i in range ( len ( review ) ):
        Review_Date.append ( review[ i ].text )

    Date = [ ]
    for i in Review_Date:
        Date.append ( i.replace ( "Date of stay:" , '' ) )

    rating = [ ]
    for u in url_list:
        soup = get_page ( u )
        review = soup.find_all ( score_name , class_=score_url )
        rating.append ( review )

    flatten = lambda l: [ item for sublist in l for item in sublist ]
    rating = flatten ( rating )
    Review_Score = [ ]
    for i in rating:
        Review_Score.append ( i.span[ 'class' ][ 1 ] )

    rating_final = [ ]
    for i in Review_Score:
        rating_final.append ( i.replace ( "bubble_" , '' ) )

    scrape_df = pd.DataFrame ( {'Review': Review_list , 'rating': rating_f , "Date": Date} )

    with open ( 'data/scrape_new' , 'wb' ) as f:
        pickle.dump ( scrape_df , f )

    return scrape_df



url_list=['https://www.tripadvisor.ca/Hotel_Review-g34438-d4091412-Reviews-YVE_Hotel_Miami-Miami_Florida.html#REVIEWS']
for i in range(5,2660,5):
      url_list.append('https://www.tripadvisor.ca/Hotel_Review-g34438-d4091412-Reviews-or{}-YVE_Hotel_Miami-Miami_Florida.html#REVIEWS'.format(i))

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
review_name='q'
review_url='location-review-review-list-parts-ExpandableReview__reviewText--gOmRC'
date_name='span'
date_url="location-review-review-list-parts-EventDate__event_date--1epHa"
score_name='div'
score_url='location-review-review-list-parts-RatingLine__bubbles--GcJvM'



if __name__ == '__main__':
    scrape_final =scraping ( headers=headers , url_list , review_name , review_url , date_name , date_url , score_name ,score_url )


