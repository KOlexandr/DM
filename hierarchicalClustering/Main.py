from hierarchicalClustering.HierarchicalClustering import HierarchicalClustering
from hierarchicalClustering.InterClassSimilarityType import InterClassSimilarityType
from dbscan.CustomPoint import CustomPoint
from pylab import *

__author__ = 'KOL'


def print_clusters(clusters):
    """
    * print string representation of all clusters from given list
    """
    print("Clusters:")
    for cluster in clusters:
        if len(cluster.points) > 0:
            print(cluster)
    print("\n")


def read_points_from_file(path_to_file):
    """
    * read coordinate of points from file and create set of points
    * @param pathToFile - path to file with data
    * @return - set of points for classification
    """
    points = set()
    file = open(path_to_file, "r")
    strings = file.readlines()
    file.close()
    for string in strings:
        split = string[0:len(string)-1].split(",")
        coordinates = []
        for i in split:
            coordinates.append(float(i))
        points.add(CustomPoint(coordinates, len(coordinates)))
    return points


def plot_cluster(cluster, style):
    """
    * plot one cluster (all points from one cluster)
    """
    x = []
    y = []
    for point in cluster.points:
        x.append(point.coordinates[0])
        y.append(point.coordinates[1])
    plot(x, y, style, markersize=10)


def plot_all_results(clusters, noise):
    """
    * plot all clusters of clustered data and noise cluster
    """
    some_colors = ["b", "g", "k", "m", "y", "c"]
    j = 0
    plot_cluster(noise, 'ro')
    for i in clusters:
        style = some_colors[j] + "*"
        plot_cluster(i, style)
        j += 1
    savefig("clusters.png")
    show()


def main():
    """
    * main function
    """
    points_set = read_points_from_file("test.txt")

    # this are tests for 3 different type of counting similarity between clusters
    # for each type we must use specific parameters of eps
    # classification with eps which i use take good results, its same as in DBSCAN,
    # but classification with type GROUP_AVERAGE classify one noise point as part of one of clusters
    # all type is usable, and all has some strengths and limitations
    # one type of counting similarity better for one data and worse for another
    # as result i can say that type GROUP_AVERAGE worse for test data then MIN and MAX

    #hc = HierarchicalClustering(points_set, 3, 6, InterClassSimilarityType.MIN)
    #hc = HierarchicalClustering(points_set, 3, 20, InterClassSimilarityType.MAX)
    hc = HierarchicalClustering(points_set, 3, 6, InterClassSimilarityType.GROUP_AVERAGE)

    print_clusters(hc.result_clusters)
    print("Noise:\n" + str(hc.noise_cluster))
    plot_all_results(hc.result_clusters, hc.noise_cluster)

#calling main function
main()