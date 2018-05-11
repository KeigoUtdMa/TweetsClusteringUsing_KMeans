# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 23:05:54 2018

@author: patil
"""

import json,sys

# Reading json file in a dictionary
def getTweets(tweetsJsonFile):
    tweets = {}
    with open(tweetsJsonFile) as json_data:
        for line in json_data:
            tweet = json.loads(line)
            tweets[str(tweet["id"])] = tweet["text"]
            print(tweets)
    return tweets


def getCentroids(initialSeedsFile):
    with open(initialSeedsFile) as centroid_tweet_file:
        return centroid_tweet_file.read().rsplit(",\n")


def getCentroidsDict(centroids):
    centroids_dict = {}
    numOfClusters = len(centroids)
    for idx in range(0, numOfClusters):
        centroids_dict[idx] = centroids[idx]
    return centroids_dict

def countWords(list_of_words):
    counts_dict = {}
    for word in list_of_words:
        if word in counts_dict:
            counts_dict[word] = counts_dict[word] + 1
        else:
            counts_dict[word] = 1
    return counts_dict

def intersection(tweetdata_one, tweetdata_two):
    result_intesection = 0
    for word in tweetdata_one:
        while tweetdata_one[word] != 0 and word in tweetdata_two:
            if word in tweetdata_two:
                tweetdata_two[word] = tweetdata_two[word] - 1
                tweetdata_one[word] = tweetdata_one[word] - 1
                if tweetdata_two[word] == 0:
                    tweetdata_two.pop(word, None)
                result_intesection += 1
    return result_intesection

def union(tweetdata_one, tweetdata_two):
    result_union = 0
    for word in tweetdata_one:
        if word in tweetdata_two:
            result_union = result_union + max(tweetdata_one[word], tweetdata_two[word])
            tweetdata_two.pop(word, None)
        else:
            result_union = result_union + tweetdata_one[word]
    for word in tweetdata_two:
        result_union = result_union + tweetdata_two[word]
    return result_union




def jaccard_distance(tweetDataOne, tweetDataTwo):
    tweetDataOne_count = countWords(tweetDataOne)
    tweetDataTwo_count = countWords(tweetDataTwo)
    tweetdata_union = union(dict(tweetDataOne_count), dict(tweetDataTwo_count))
    tweetdata_intersect = intersection(dict(tweetDataOne_count), dict(tweetDataTwo_count))
    return 1.0 - tweetdata_intersect * 1.0 / tweetdata_union


def form_clusters(tweets_dict, centroid_dict):
    clusters = {}
    for i in range(len(centroid_dict)):                 # Initialize clusters
        clusters[i] = []

    for tweet_id in tweets_dict:
        min_distance = 1
        clusterId = 0
        for index in centroid_dict:
            jaccardDistance = jaccard_distance(tweets_dict[centroid_dict[index]], tweets_dict[tweet_id], )
            if(jaccardDistance < min_distance):
                min_distance = jaccardDistance
                clusterId = index
        clusters[clusterId].append(tweet_id)
    return clusters


def find_new_centroids(cluster, tweets):
    min_distance = 1
    min_cluster_id = cluster[0]
    for cluster_tweet_id in cluster:
        distance = 0
        for other_cluster_tweetid in cluster:
            distance = distance + jaccard_distance(tweets[cluster_tweet_id], tweets[other_cluster_tweetid] )
        mean = distance/len(cluster)
        if mean < min_distance:
            min_distance = mean
            min_cluster_id = cluster_tweet_id
    return min_cluster_id

def sum_squared_error(clusters, centroids, tweet_data):
    sse = 0
    for cluster in clusters:
        for tweet_id in clusters[cluster]:
            sse += jaccard_distance(tweet_data[tweet_id], tweet_data[centroids[cluster]]) ** 2
    return sse

def main():
    # number_of_clusters = 25
    # initial_seeds_file = "InitialSeeds.txt"
    # tweets_data_file = "Tweets.json"
    # outputfile = "out.txt"

    if len(sys.argv) == 5:
        number_of_clusters = int(sys.argv[1])
        initial_seeds_file = sys.argv[2]
        tweets_data_file = sys.argv[3]
        outputfile = sys.argv[4]
    elif len(sys.argv) == 4:
        number_of_clusters = 25
        initial_seeds_file = sys.argv[1]
        tweets_data_file = sys.argv[2]
        outputfile = sys.argv[3]
    
    tweets_dict = getTweets(tweets_data_file)
    #print("Tweets Dictionary: ", tweets_dict)
    centroids = getCentroids(initial_seeds_file)
    #print("Centroids: ", centroids)

    if len(centroids) != number_of_clusters:
        print("Mismatch between number of values in Initial seed file and number of clusters entered")
        sys.exit(1)


    while True:
        new_centroids = []
        centroids_dict = getCentroidsDict(centroids)
        clusters = form_clusters(tweets_dict, centroids_dict)
        for cluster in clusters:
            new_centroids.append(find_new_centroids(clusters[cluster], tweets_dict))
        if new_centroids == centroids:
            break
        else:
            centroids = new_centroids

    output_result_file = open(outputfile, 'w')
    output_result_file.write("\n\nClusters:\n")
    for cluster in clusters:
        output_result_file.write(str(cluster))
        output_result_file.write("\t")
        for tweet in clusters[cluster]:
            output_result_file.write(tweet)
            output_result_file.write(", ")
        output_result_file.write("\n")

    output_result_file.write("\n\n")
    output_result_file.write("SSE: ")
    output_result_file.write(str(sum_squared_error(clusters, centroids, tweets_dict)))


main()