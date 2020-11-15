import sys
import json
import math

"""
Verifying the user input arguments
"""
if len(sys.argv) > 5:
    print("[Error:] Expected arguments not more than 4, Recieved more arguments: ")
    sys.exit(1)
if len(sys.argv) < 4:
    print("[Error:] Expected arguments not less than 3, Recieved less arguments: ")
    sys.exit(1)
if len(sys.argv) == 5:
    numOfClusters = int(sys.argv[1])
    initialSeedsFile = sys.argv[2]
    tweetsDataFile = sys.argv[3]
    outputFile = sys.argv[4]
elif len(sys.argv) == 4:
    print("[Default:] Number of Clusters : 25")
    numOfClusters = 25
    initialSeedsFile = sys.argv[1]
    tweetsDataFile = sys.argv[2]
    outputFile = sys.argv[3]

"""
Initializing the centroid tweet Ids in to a dictionary
"""
tweetCentroidIds = {}
with open(initialSeedsFile) as tweet_centroid:
    centroids = tweet_centroid.read().rsplit(",\n")
    if len(centroids) == numOfClusters:
        for id in range(0, numOfClusters):
            tweetCentroidIds[id] = centroids[id]
    else:
        print ("[Error]: Initial seed file contains values not equal to the clusters entered")
        sys.exit(1)
print(centroids)



"Function to read json file and store tweet id and its text in a dictionary"
def readJson(tweetJson):
    for line in tweetJson:
        readTweets = json.loads(line)
        tweetsJsonData[str(readTweets["id"])] = readTweets["text"]

"""
Initializing a dictionary with key as tweet Id and values with corresponding text/tweet
"""
tweetsJsonData = {}
with open(tweetsDataFile) as tweetJson:
    readJson(tweetJson)
"""
This function return the count of unique words in each tweet
"""
def tweetWords(wordsList):
    counts = {}
    for word in wordsList:
        if word in counts:
            counts[word] = counts[word] + 1
        else:
            counts[word] = 1
    return counts

"""
Function to check number of words of one tweet matches another tweet
"""
def tweetIntersection(tweet1, tweet2):
    result = 0
    for word in tweet1:
        while tweet1[word] != 0 and word in tweet2:
            if word in tweet2:
                tweet2[word] = tweet2[word] - 1
                tweet1[word] = tweet1[word] - 1
                if tweet2[word] == 0:
                    tweet2.pop(word, None)
                result += 1
    return result

"""
Function to word count of tweets in comparison, counting the matching words only once
"""
def tweetUnion(tweet1, tweet2):
    result = 0
    for word in tweet1:
        if word in tweet2:
            result = result + max(tweet1[word], tweet2[word])
            tweet2.pop(word, None)
        else:
            result = result + tweet1[word]
    for word in tweet2:
        result = result + tweet2[word]
    return result

"""
Function to calculate whether two tweets are similar or not
If returned value is small both tweets have more similarities or else they are less similar
"""
def jaccard_distance(tweet_a, tweet_b):
    tweet1Words = tweetWords(tweet_a)           #tweet_a.split()
    tweet2Words = tweetWords(tweet_b)           #tweet_b.split()
    tweetWordsUnion = tweetUnion(dict(tweet1Words), dict(tweet2Words))
    tweetWordsIntersect = tweetIntersection(dict(tweet1Words), dict(tweet2Words))
    return 1.0 - tweetWordsIntersect*1.0/tweetWordsUnion

"""
Function to assign tweets to a cluster
"""
def formClusters(tweetCentroidIds, tweetsJsonData):
    clusters = {}
    for index in range(len(tweetCentroidIds)):
        clusters[index] = []
    for tweet in tweetsJsonData:
        minJaccardDist = 1
        cluster = 0
        for centroidId in tweetCentroidIds:
            tweetCentroidDist = 1
            tweetCentroidDist = jaccard_distance(tweetsJsonData[tweetCentroidIds[centroidId]], tweetsJsonData[tweet])
            if tweetCentroidDist < minJaccardDist:
                minJaccardDist = tweetCentroidDist
                cluster = centroidId
        clusters[cluster].append(tweet)
    return clusters

"""
Function to recalculate centroid for a cluster taking all the tweets in account
"""
def recalculateCentroid(cluster, tweet_data):
    centroidId = cluster[0]
    min_distance = 1
    for tweet in cluster:
        total_distance = 0
        for other_tweet in cluster:
            total_distance = total_distance + jaccard_distance(tweet_data[tweet], tweet_data[other_tweet])
        mean_distance = total_distance * 1.0 / len(cluster)
        if mean_distance < min_distance:
            min_distance = mean_distance
            centroidId = tweet
    return centroidId
"""
Function to calculate the squared sum of errors(SSE)
"""
def sse(clusters, centroid_values, tweet_data):
    result = 0
    for cluster in clusters:
        for tweet in clusters[cluster]:
            result += math.pow(jaccard_distance(tweet_data[tweet], tweet_data[centroid_values[cluster]]),2)
    return result

"""
K-means clustering until centroid remains same
"""
updateCentroidIds = {}
while True:
    clusters = formClusters(tweetCentroidIds, tweetsJsonData)
    for cluster in clusters:
        updateCentroidIds[cluster] = recalculateCentroid(clusters[cluster], tweetsJsonData)
    if updateCentroidIds == tweetCentroidIds:
        sseValue = str(sse(clusters, updateCentroidIds, tweetsJsonData))
        print ("SSE: " + sseValue)
        break
    else:
        tweetCentroidIds = updateCentroidIds


"""
Writing the sse value and clusters in to the output file
"""
fileToOutput = open(outputFile, 'w')
fileToOutput.write("SSE Value: ")
fileToOutput.write(sseValue)
fileToOutput.write("\n\nClusters:\n\n")
for cluster in clusters:
    fileToOutput.write(str(cluster))
    fileToOutput.write("\t")
    for tweet in clusters[cluster]:
        fileToOutput.write(tweet)
        fileToOutput.write(", ")
    fileToOutput.write("\n\n")