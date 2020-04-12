from twitter import Twitter,OAuth

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
            result.append(KritzelKaffeeTweet(tweet['id'], tweet['created_at'], tweet['entities']['media'][0]['media_url'], tweet['text']))
    return result

def save_csv(kritzelkaffees):
    filename = "KritzelKaffees.csv" 
    with open(filename, 'w', encoding="utf-8") as csvfile:
        for k in kritzelkaffees:
            csvfile.write(str(k.id) +",'"+ k.date +"',"+ repr(k.text) +",'"+ k.imglink + "'\n")
    return filename

def save_html(kritzelkaffees):
    filename = "KritzelKaffees.html"
    with open('html/'+filename, 'w', encoding="utf-8") as htmlfile:
        from HtmlTemplate import htmlstart, htmlend
        htmlfile.write(htmlstart)
        for k in kritzelkaffees:
            htmlfile.write("<tr>\n")
            htmlfile.write("<td>"+k.date+"</td>\n")
            htmlfile.write("<td>"+str(k.id)+"???</td>\n")
            htmlfile.write("<td>"+k.text+"</td>\n")
            htmlfile.write("<td><img src='"+k.imglink+"' width='200px'></td>\n")
            htmlfile.write("</tr>\n")
        htmlfile.write(htmlend)
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
#    htmlfilename = save_html(kritzelkaffees)
#    print('Wrote data to ' + htmlfilename)
    print('Bye')

