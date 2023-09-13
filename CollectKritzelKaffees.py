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

def get_tweets(since_id):
    tweets = t.statuses.user_timeline(screen_name="datGestruepp", exclude_replies=True, count=200, since_id=since_id)
    earliest_tweet = min(tweets, key=lambda x: x["id"])["id"] - 1
    result = list(filter(is_KritzelKaffeeTweet, tweets))
    while True:
        if since_id > earliest_tweet:
            break
        print("Found "+str(len(result)) + " tweets so far")
        print("Looking for tweets with max_id="+str(earliest_tweet))
        tweets_nextpage = t.statuses.user_timeline(screen_name="datGestruepp", max_id=earliest_tweet, exclude_replies=True, count=200, since_id=since_id)
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

#this is a test to get older tweets since timeline does only return up to 3500 tweets in the unpaid api
def get_old_tweets():
    #listOfTweetIds = "1105730340549812225,1105350896777482240,1105005014739812352,1104646720842055681,1104277600598441984,1103910018510815232,1103539207069487104,1103172201103179778,1102808510243524608,1102453151540695041,1102109447411908608,1101733728961945600,1101363389497044992,1100643151432290305,1100277071564156928,1099919690334457856,1099562804191858688,1099207758811987968,1098823537522032641,1098484442023297024,1098136309795819520,1097734604117684226,1097385490905513985,1097016802117382144,1096647543885303809,1096305218936020992,1095928687516631041,1095587803138871297,1095195865189371904,1094847010694418432,1094516778867351555,1094133307992870912,1093765219212541953,1093387858168201217,1093051432616583169,1092662219551268865,1092318266377334784,1091951490674159622,1091594899135361025,1091234270406955008,1090506226084077574,1090131423179223040,1089786576652173312,1089429834252632064,1089061208018296832,1088680233794981889,1088338588973051904,1087969307110318081,1087602656292433920,1087243567725248513,1086884044405653504,1086554020964118528,1086156519786401793,1085793491169497088,1085434792404021248,1085046866847416320,1084717691213107201,1084362384049930240,1083990619876401153,1083638639639359488,1083253945957527552,1082901669632004096,1082514799139979264,1082166376662515713,1081827038795874304,1081458486708523008,1081082289466019845,1080747703993282560,
    #listOfTweetIds = "1080383979998580737,1080033968521654272,1079658683339030528,1079307858288742401,1078931451587035136,1078561723009896449,1078168613767516160,1077805229989609474,1077452995263107072,1077075112975912960,1076716154125721600"
    listOfTweetIds = "1100994326258241536,1129622945423396865,1155009927099740160,1155372315900882944,1155734702617055232,1156097090222796800,1160068738596638721,1165504075233992706"
    tweets = t.statuses.lookup(_id=listOfTweetIds, include_entities=True, trim_user=True)
    return list(filter(is_KritzelKaffeeTweet, tweets))


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
        csvfile.write("TwitterID,TwitterLink,Datum,TweetText,BildLink,Bild,Gast\n")
        for k in kritzelkaffees:
            csvfile.write(str(k.id) +",https://twitter.com/datGestruepp/status/"+ str(k.id) +","+ k.date +",\""+ k.text.replace('\n',' ').replace('"', "'") +"\","+k.imglink+",=image(\""+ k.imglink +"\"),\""+ k.guestname +"\"\n")
    return filename

if __name__ == "__main__":
    from TwitterTokens import *
    t = Twitter(auth=OAuth(token, token_secret, consumer_key, consumer_secret))
    print('Looking for KritzelKaffee tweets')
    #tweets = get_old_tweets()
    tweetsNewerThanId = 1563405957492776960 # 27.08.2022
    tweets = get_tweets(tweetsNewerThanId)
    kritzelkaffees = convert_to_KritzelKaffeeTweet(tweets)
    kritzelkaffees.sort(key=lambda k: k.id)
    print('Found ' + str(len(kritzelkaffees)) + ' KritzelKaffee tweets!')
    
    # TODO read guest names and add them to the kritzelkaffees

    csvfilename = save_csv_clean(kritzelkaffees)
    print('Wrote data to ' + csvfilename)
    csvfilename = save_csv_for_googlesheet(kritzelkaffees)
    print('Wrote data to ' + csvfilename)
    print('Bye')

