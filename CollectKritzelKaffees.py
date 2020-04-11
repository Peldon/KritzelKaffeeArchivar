from twitter import *


def get_tweets(api=None, screen_name=None):
    
    tweets = t.statuses.user_timeline(screen_name="datGestruepp", count=200)
    earliest_tweet = min(tweets, key=lambda x: x["id"])["id"] - 1
    print("getting tweets before:", earliest_tweet)

    result = list(filter(lambda x: len(list(filter(lambda y: "kritzelkaffee" == y['text'], x['entities']['hashtags']))) > 0, tweets))

    while True:
        tweets_nextpage  = t.statuses.user_timeline(screen_name="datGestruepp", max_id=earliest_tweet, count=200)
        if not tweets_nextpage:
            break
        new_earliest = min(tweets_nextpage, key=lambda x: x["id"])["id"] - 1
        if new_earliest == earliest_tweet:
            break
        else:
            earliest_tweet = new_earliest
            print("getting tweets before:", earliest_tweet)
            result += list(filter(lambda x: len(list(filter(lambda y: "kritzelkaffee" == y['text'], x['entities']['hashtags']))) > 0, tweets_nextpage))

    return result


if __name__ == "__main__":
    from TwitterTokens import *
    t = Twitter(auth=OAuth(token, token_secret, consumer_key, consumer_secret))

    tweets = get_tweets()
    print(len(tweets))
#    for tweet in tweets:
#        print(tweet)
