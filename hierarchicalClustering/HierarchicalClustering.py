import numpy
from hierarchicalClustering.Cluster import Cluster
from hierarchicalClustering.InterClassSimilarityType import InterClassSimilarityType

__author__ = 'KOL'


class HierarchicalClustering:

    def __init__(self, d, min_pt, eps, similarity_type):
        """
        * initialise and classify set of given points
        * @param d - set of initial points
        * @param eps - similarity of clusters, if similarity less then eps we can join this clusters
        * @param minPt - minimum number of points for cluster? if cluster has less number of points this cluster is noise
        * @param similarityType - type of counting similarity between clusters
        """
        self.d = d
        self.eps = eps
        self.min_pt = min_pt
        self.all_clusters = []
        self.result_clusters = []
        self.noise_cluster = Cluster(-1)
        self.similarity_type = similarity_type

        self.classify()

    def classify(self):
        """
        * classify given data set
        """
        step = 0
        one_step_clusters = []
        prev_step_clusters = None
        #create clusters with only one point
        for point in self.d:
            cluster = Cluster(step)
            cluster.points.add(point)
            one_step_clusters.append(cluster)

        #add list of clusters to list of lists of clusters as clusters of 0 step
        self.all_clusters.append(one_step_clusters)
        #create similarity matrix
        s = numpy.zeros((len(one_step_clusters), len(one_step_clusters)))
        #fill similarity matrix
        for i in range(0, len(one_step_clusters)):
            for j in range(0, len(one_step_clusters)):
                s[i][j] = self.sim(one_step_clusters[i], one_step_clusters[j])
        step += 1

        #while previous cluster not equals new cluster
        while one_step_clusters != prev_step_clusters:
            prev_step_clusters = one_step_clusters
            one_step_clusters = []
            #iterate on all clusters
            for i in range(0, len(prev_step_clusters)):
                c = prev_step_clusters[i]
                #if not processes yet => process
                if not c.processed:
                    c.processed = True
                    #find closest cluster
                    closest = self.find_closest_cluster(prev_step_clusters, s[i])
                    #if found
                    if None != closest:
                        #process closest cluster
                        closest.processed = True
                        #create new cluster of current step
                        cluster = Cluster(step)
                        cluster.points.update(c.points)
                        cluster.points.update(closest.points)
                        #join points from 2 clusters in new cluster
                        #and add this cluster to list of clusters for current step
                        one_step_clusters.append(cluster)
                    else:
                        #if not found closest add this cluster to list of clusters for current step
                        one_step_clusters.append(c)
            #add list of all clusters for current step to list of list
            self.all_clusters.append(one_step_clusters)
            #create and fill new similarity matrix for clusters of current step
            s = numpy.zeros((len(one_step_clusters), len(one_step_clusters)))
            #fill similarity matrix
            for i in range(0, len(one_step_clusters)):
                for j in range(0, len(one_step_clusters)):
                    s[i][j] = self.sim(one_step_clusters[i], one_step_clusters[j])
                s[i][i] = 0
            #set all clusters as not processed
            for cluster in one_step_clusters:
                cluster.processed = False
            step += 1
        #clusters on 2 last steps equals that mean we classified all point
        #lets process results (find noise and create for noise points one specific cluster)
        #and create list with clusters (without noise)
        self.process_results()

    def process_results(self):
        """
        * process list of clusters that program get on last step
        * if number of points in any cluster less then minPt points from this cluster is noise
        """

        for cluster in self.all_clusters[len(self.all_clusters)-1]:
            if len(cluster.points) < self.min_pt:
                self.noise_cluster.points.update(cluster.points)
            else:
                self.result_clusters.append(cluster)

    def find_closest_cluster(self, clusters, s):
        """
        * find cluster that more similar to this cluster
        * @param clusters - list of all clusters on current step
        * @param s - line of similarity matrix for this cluster
        * @return closest cluster or null if no any closest cluster
        """
        idx = -1
        dist = 1e9
        #finding cluster: distance from this cluster to closest less then eps and closest cluster is not processed yet
        #and closest not equals this cluster
        for i in range(1, len(s)):
            if s[i] != 0 and dist > s[i] and s[i] < self.eps and not clusters[i].processed:
                dist = s[i]
                idx = i
        if idx != -1:
            s[idx] = 0
            return clusters[idx]
        else:
            return None

    def sim(self, ci, cj):
        """
        * Define Inter-Cluster Similarity
        * 1. use min distance between 2 points from 2 clusters
        * 2. use max distance between 2 points from 2 clusters
        * 3. use all distances between each points of 2 clusters
        * @param ci - first cluster
        * @param cj - second cluster
        * @return similarity of clusters (distance between clusters)
        """
        if InterClassSimilarityType.MAX == self.similarity_type:
            max_distance = 0
            for dk in ci.points:
                for dp in cj.points:
                    if dk != dp and max_distance < dk.distance(dp):
                        max_distance = dk.distance(dp)
            return max_distance
        elif InterClassSimilarityType.MIN == self.similarity_type:
            min_distance = 1e9
            for dk in ci.points:
                for dp in cj.points:
                    if dk != dp and min_distance > dk.distance(dp):
                        min_distance = dk.distance(dp)
            return min_distance
        else:
            sum_distances = 0
            new_cluster = set()
            new_cluster.update(ci.points)
            new_cluster.update(cj.points)
            for dk in new_cluster:
                for dp in new_cluster:
                    if dk != dp:
                        sum_distances += dk.distance(dp)
            return sum_distances/((len(ci.points) + len(cj.points))*((len(ci.points) + len(cj.points) - 1)))