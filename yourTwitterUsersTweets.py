#Author: Raghavendra Deshmukh
#Program Purpose: Learning Python and Twitter APIs with Pandas Dataframe etc
#Activity: Will Extract the Followers of a given Twitter Handle and ranks them on the basis of # of Tweets, Their Followers etc

#Imports
import tweepy as tw
import pandas as pd

#Setup the Twitter API
tw_bearer_token = "Your Bearer Token"

#Use Twitter API v2
twclient = tw.Client(bearer_token=tw_bearer_token, wait_on_rate_limit=True)

handle = 'Your Desired Twitter Handle'

#Refer: https://developer.twitter.com/en/docs/twitter-api/users/lookup/api-reference/get-users-id
#Refer: https://docs.tweepy.org/en/stable/client.html#tweepy.Client.get_user
user = twclient.get_user(username=handle, user_fields=['public_metrics'])
print("Basic Details of the User whose details are being Searched")
print(f"User ID: {user.data.id}, Username:  {user.data.username}, User Name: {user.data.name}, Count Followers: {user.data.public_metrics['followers_count']}, Count Following: {user.data.public_metrics['following_count']}")

#Now find the list of Twitter Handles followed by this user
#Assign the Twitter ID.  Note that Twitter ID is NOT EQUAL to Twitter Handle
id = user.data.id
#Refer: https://docs.tweepy.org/en/stable/client.html#tweepy.Client.get_users_following
#Refer: https://developer.twitter.com/en/docs/twitter-api/users/follows/api-reference/get-users-id-following
followers = twclient.get_users_following(id=id, user_fields=['public_metrics'], max_results=1000)
influencer_collection = pd.DataFrame()
for follower in followers.data:
    id = follower.id
    name = follower.username
    followers = follower.public_metrics['followers_count']
    tweet_count = follower.public_metrics['tweet_count']

    followerdata = [{'User ID': id, 'Name':name, 'Followers': followers, 'Tweet Count': tweet_count}]
    tempdf = pd.DataFrame(followerdata)
    influencer_collection = pd.concat([influencer_collection, tempdf])
    influencer_collection = influencer_collection.reset_index(drop=True)

influencer_collection = influencer_collection.sort_values(by=['Followers', 'Tweet Count'], ascending=False)

#Choose only the Top 15 of the Twitter Accounts that are most popular among the ones you follow
top_influencers = influencer_collection.head(15)
print("The Top 15 of the Twitter Accounts you follow are below: ")
print(top_influencers)

for index, hdl in top_influencers.iterrows():
    #####
    print(f"############ START Tweets of User: {hdl['Name']} ##########")
    try:
        #Get the Tweets for the user using get_users_tweets API
        #Refer: https://developer.twitter.com/en/docs/twitter-api/tweets/timelines/api-reference/get-users-id-tweets
        #Refer: https://docs.tweepy.org/en/stable/client.html#tweepy.Client.get_users_tweets
        tweets = twclient.get_users_tweets(id=hdl['User ID'], exclude='retweets', tweet_fields=['public_metrics'], max_results=100)
        tweets_for_user = pd.DataFrame()
        for tweet in tweets.data: #Loop the Tweets
            #Frame the TweetData
            tweetdata = [{'Tweet ID': tweet.id, 'Text': tweet.text, 'Likes': tweet.public_metrics['like_count'], 'Retweets': tweet.public_metrics['retweet_count'], 'Created': tweet.created_at}]
            tempdf = pd.DataFrame(tweetdata)
            tweets_for_user = pd.concat([tweets_for_user, tempdf])
            tweets_for_user = tweets_for_user.reset_index(drop=True)
    #####
    except Exception as e:
        pass    
    
    try:    
        #Sort the Tweets by Likes and Retweets
        tweets_for_user = tweets_for_user.sort_values(by=['Likes', 'Retweets'], ascending=False)
        tweets_for_user = tweets_for_user.head(10) #Get the Top 10 Tweets to Print
        for index, twt in tweets_for_user.iterrows():
            id = twt['Tweet ID']
            likes = twt['Likes']
            retweets = twt['Retweets']
            text = twt['Text']
            print (f"ID:{id}, Likes:{likes}, Retweets:{retweets}, Tweet: {text}")
    except Exception as e:
        pass    

     
    print(f"############ END Tweets of User: {hdl['Name']} ##########")
    print(" ")
