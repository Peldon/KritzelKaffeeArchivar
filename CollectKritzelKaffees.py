from twitter import Twitter,OAuth
from dateutil import parser

class KritzelKaffeeTweet:
    def __init__(self, id, date, imglink, text):
         self.id = id
         self.date = date
         self.imglink = imglink
         self.text = text 
         self.guestname = ""


def is_KritzelKaffeeTweet(tweet):
    if ('media' not in tweet['entities']):
        return False
    hasHashtagInText = tweet['text'].lower().find("kritzelkaffee") >= 0
    hasHashtag = len(list(filter(lambda y: "kritzelkaffee" == y['text'].lower(), tweet['entities']['hashtags']))) > 0
    return hasHashtagInText or hasHashtag

def get_tweets():
    tweets = t.statuses.user_timeline(screen_name="datGestruepp", exclude_replies=True, count=200)
    earliest_tweet = min(tweets, key=lambda x: x["id"])["id"] - 1
    result = list(filter(is_KritzelKaffeeTweet, tweets))
    while True:
        print("Found "+str(len(result)) + " tweets so far")
        print("Looking for tweets with max_id="+str(earliest_tweet))
        tweets_nextpage = t.statuses.user_timeline(screen_name="datGestruepp", max_id=earliest_tweet, exclude_replies=True, count=200)
        if not tweets_nextpage:
            print("no more tweets found")
            break
        new_earliest = min(tweets_nextpage, key=lambda x: x["id"])["id"]
        if new_earliest == earliest_tweet:
            print("new_earliest == earliest_tweet")
            break
        else:
            earliest_tweet = new_earliest - 1
            result += list(filter(is_KritzelKaffeeTweet, tweets_nextpage))

    return result

def convert_to_KritzelKaffeeTweet(tweets):
    result = []
    for tweet in tweets:
        postedAtDate = parser.parse(tweet['created_at'])
        result.append(KritzelKaffeeTweet(tweet['id'], postedAtDate.strftime("%d.%m.%Y"), tweet['entities']['media'][0]['media_url'], tweet['text']))
    return result

def save_csv_clean(kritzelkaffees):
    filename = "KritzelKaffees.csv" 
    with open(filename, 'w', encoding="utf-8") as csvfile:
        csvfile.write("TwitterLink,Datum,TweetText,Bild,Gast\n")
        for k in kritzelkaffees:
            # TODO escape chars in text properly!? having " and \n in there will break the csv
            csvfile.write(str(k.id) + ',' + k.date + ',"' + k.text.replace('\n',' ').replace('"', "'") + '","' + k.imglink + '","' + k.guestname.replace('"', "'") + '"\n')
    return filename

def save_csv_for_googlesheet(kritzelkaffees):
    filename = "KritzelKaffeesGoogleSheet.csv" 
    with open(filename, 'w', encoding="utf-8") as csvfile:
        csvfile.write("TwitterLink,Datum,TweetText,Bild,Gast\n")
        for k in kritzelkaffees:
            csvfile.write("https://twitter.com/datGestruepp/status/"+str(k.id) +","+ k.date +",\""+ k.text.replace('\n',' ').replace('"', "'") +"\",=image(\""+ k.imglink +"\"),\""+ k.guestname +"\"\n")
    return filename

if __name__ == "__main__":
    from TwitterTokens import *
    t = Twitter(auth=OAuth(token, token_secret, consumer_key, consumer_secret))
    print('Looking for KritzelKaffee tweets')
    tweets = get_tweets()
    kritzelkaffees = convert_to_KritzelKaffeeTweet(tweets)
    print('Found ' + str(len(kritzelkaffees)) + ' KritzelKaffee tweets!')
    
    # TODO read guest names and add them to the kritzelkaffees

    csvfilename = save_csv_clean(kritzelkaffees)
    print('Wrote data to ' + csvfilename)
    csvfilename = save_csv_for_googlesheet(kritzelkaffees)
    print('Wrote data to ' + csvfilename)
    print('Bye')

