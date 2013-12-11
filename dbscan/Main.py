from dbscan.CustomPoint import CustomPoint
from dbscan.DBSCAN import DBSCAN
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
    dbscan = DBSCAN(4, 6, points_set)
    print_clusters(dbscan.clusters)
    print("Noise:\n" + str(dbscan.noise))
    plot_all_results(dbscan.clusters, dbscan.noise)

#calling main function
main()