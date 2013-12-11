from dbscan.Cluster import Cluster

__author__ = 'KOL'


class DBSCAN:

    def __init__(self, min_pt, eps, d):
        """
        # initialize all fields and find all neighbor points of all points
        # @param minPt - minimum count of points for cluster
        # @param eps - maximum distance between points of cluster
        # @param d - set of initial points
        """
        self.d = d
        self.min_pt = min_pt
        self.noise = Cluster(-1)
        self.clusters = set()

        #find all neighbor points for all points and set that to field in each point
        for point in d:
            for near in d:
                if point != near and point.distance(near) <= eps:
                    point.eps_near_points.add(near)
        self.classify()

    def classify(self):
        """
        * classify given data set
        """
        j = 0
        cluster = Cluster(j)
        self.clusters.add(cluster)
        #iterate by all points
        for point in self.d:
            #if not visited yet => visit
            if not point.visited:
                point.visited = True
                #if count of neighbor points < minPt then it's point is noise
                if len(point.eps_near_points) < self.min_pt:
                    self.noise.points.add(point)
                else:
                    self.expand_cluster(point, cluster)
                    cluster = Cluster(++j)
                    self.clusters.add(cluster)
        self.clear_noise_cluster()

    def expand_cluster(self, point, cluster):
        """
        * process one point and all it neighbor points
        * @param point - given point for process
        * @param cluster - cluster for this point
        """
        #add point to new cluster
        cluster.points.add(point)
        #set for neighbor point, because we can't add items to list when we iterate on it
        tmp = set()
        #iterate by all neighbor point of input point
        for epsNearPoint in point.eps_near_points:
            #if not visited yet => visit
            if not epsNearPoint.visited:
                epsNearPoint.visited = True
                #if count of neighbor points >= min_pt then add this points to tmp set
                if len(epsNearPoint.eps_near_points) >= self.min_pt:
                    tmp.update(epsNearPoint.eps_near_points)

            #if current neighbor point is not a member of any cluster yet - add it to cluster
            if not self.belong_to_any_cluster(epsNearPoint):
                cluster.points.add(epsNearPoint)

        #if set of new neighbor points is not empty =>
        #add it to set of neighbor points of point and recursive call this method again
        #old points from neighbor set already visited and we will not do anything with them again
        if len(tmp) > 0:
            point.eps_near_points.update(tmp)
            self.expand_cluster(point, cluster)

    def belong_to_any_cluster(self, point):
        """
        * verify if any of clusters contains given point
        * @param point - point for verification
        * @return true if some cluster has this point, false otherwise
        """
        for cluster in self.clusters:
            if point in cluster.points:
                return True
        return False

    def clear_noise_cluster(self):
        """
        * if we have situation when we process boundary points at first
        * and they have neighbor points < min_pt - they will classify as noise,
        * but this points may be densely achievable or tightly linked with
        * any point in some cluster
        * in this situation we must classify this point as point of that cluster
        *
        * as result at the end of classification we will remove all classified point
        * from noise cluster if they exists in another cluster
        """
        for cluster in self.clusters:
            for point in cluster.points:
                if point in self.noise.points:
                    self.noise.points.remove(point)