# TweetsClusteringUsing_KMeans

Clustering tweets by utlizing Jaccard Distance metric and K-means clustering algorithm.

<br>

## Approach

- Compute the similarity between tweets using Jaccard Distance Metric
- Cluster tweets using the K-means clustering algorithm

## Input to K-means algorithm

1. The number of clusters K (default K=25)
2. A real world dataset sampled from Twitter during the Boston Marathon Bombing event in April 2013 that contains 251 tweets. The tweet dataset is in JSON format and can be found <a href="https://github.com/patilankita79/TweetsClusteringUsing_KMeans/blob/master/TweetClustering/Tweets.json">here</a>
3. The list of initial centroids can be found <a href="https://github.com/patilankita79/TweetsClusteringUsing_KMeans/blob/master/TweetClustering/InitialSeeds.txt">here</a>

## Compile and Run Instructions:

**Commands to run:**

```
  Tweet_Cluster_K_Means.py <numberOfClusters> <initialSeedsFile> <TweetsDataFile> <outputFile>
```
  where numberOfClusters is optional, if not given then default value 25 will be taken
  
```  
  Tweet_Cluster_K_Means.py <initialSeedsFile> <TweetsDataFile> <outputFile>
```

**Example commands:**

```
1. python Tweet_Cluster_K_Means.py 25 InitialSeeds.txt Tweets.json tweets-k-means-output.txt
2. python Tweet_Cluster_K_Means.py InitialSeeds.txt Tweets.json tweets-k-means-output.txt
```

**Results:**
After running Tweet_Cluster_K_Means.py a file  tweets-k-means-output.txt is created in your current directory which contains the results after clustering the tweets based on the initialSeeds.txt containing k initial selected cluster centroids. 
