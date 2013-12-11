from math import sqrt
import random

__author__ = 'KOL'


class CustomPoint(object):

    def __init__(self, coordinates, dimension):
        self.visited = False
        self.dimension = dimension
        self.coordinates = coordinates
        #Neps(p)={q є D|dist(p,q) <= eps}
        self.eps_near_points = set()

    def __str__(self):
        return "Point{coordinates=" + str(self.coordinates) + ", dimension=" + str(self.dimension) + '}'

    def __eq__(self, y):
        return self.dimension == y.dimension and self.coordinates == y.coordinates

    def __hash__(self):
        return super().__hash__()

    def distance(self, point):
        """
        * count distance between this point and another
        * @param point - another point
        * @return Euclidean distance
        """
        dist = 0
        for i in range(0, len(self.coordinates)):
            dist += (self.coordinates[i] - point.coordinates[i]) * (self.coordinates[i] - point.coordinates[i])
        return sqrt(dist)

    @staticmethod
    def get_random_point(min_boundaries, max_boundaries, dimension):
        """
        * create Point with random x and y coordinates
        * @param maxBoundaries - max values for all coordinates
        * @param minBoundaries -- max values for all coordinates
        * @param dimension - dimension of space (count of coordinates)
        * @return new object Point
        """
        coordinates = []
        for i in range(0, dimension):
            coordinates.append(random.uniform(min_boundaries[i], max_boundaries[i]))
        return CustomPoint(coordinates, dimension)