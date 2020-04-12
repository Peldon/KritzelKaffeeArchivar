from twitter import Twitter,OAuth
from dateutil import parser

class KritzelKaffeeTweet:
    def __init__(self, id, date, imglink, text):
         self.id = id
         self.date = date
         self.imglink = imglink
         self.text = text 


def get_tweets():
    tweets = t.statuses.user_timeline(screen_name="datGestruepp", count=200)
    earliest_tweet = min(tweets, key=lambda x: x["id"])["id"] - 1
    result = list(filter(lambda x: len(list(filter(lambda y: "kritzelkaffee" == y['text'].lower(), x['entities']['hashtags']))) > 0, tweets))
    while True:
        tweets_nextpage  = t.statuses.user_timeline(screen_name="datGestruepp", max_id=earliest_tweet, count=200)
        if not tweets_nextpage:
            break
        new_earliest = min(tweets_nextpage, key=lambda x: x["id"])["id"]
        if new_earliest == earliest_tweet:
            break
        else:
            earliest_tweet = new_earliest - 1
            result += list(filter(lambda x: len(list(filter(lambda y: "kritzelkaffee" == y['text'].lower(), x['entities']['hashtags']))) > 0, tweets_nextpage))

    return result

def convert_to_KritzelKaffeeTweet(tweets):
    result = []
    for tweet in tweets:
        if ('media' in tweet['entities']):
            postedAtDate = parser.parse(tweet['created_at'])
            result.append(KritzelKaffeeTweet(tweet['id'], postedAtDate.strftime("%d.%m.%Y"), tweet['entities']['media'][0]['media_url'], tweet['text']))
    return result

def save_csv(kritzelkaffees):
    filename = "KritzelKaffees.csv" 
    with open(filename, 'w', encoding="utf-8") as csvfile:
        csvfile.write("TwitterLink,Datum,TweetText,Bild\n")
        for k in kritzelkaffees:
            # escaping new lines is needed, but importing it in google sheets is a bit stupid, so we just remove them 
            csvfile.write("https://twitter.com/datGestruepp/status/"+str(k.id) +","+ k.date +",\""+ k.text.replace('\n',' ') +"\",=image(\""+ k.imglink + "\")\n")
    return filename

if __name__ == "__main__":
    from TwitterTokens import *
    t = Twitter(auth=OAuth(token, token_secret, consumer_key, consumer_secret))
    print('Looking for KritzelKaffee tweets')
    tweets = get_tweets()
    kritzelkaffees = convert_to_KritzelKaffeeTweet(tweets)
    print('Found ' + str(len(kritzelkaffees)) + ' KritzelKaffee tweets!')
    csvfilename = save_csv(kritzelkaffees)
    print('Wrote data to ' + csvfilename)
    print('Bye')

