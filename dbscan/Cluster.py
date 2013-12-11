__author__ = 'KOL'


class Cluster:
    def __init__(self, id):
        self.id = id
        self.points = set()

    def __str__(self):
        return "Cluster {id=" + str(self.id) + ", points=[\n\t" + "\n\t".join(str(p) for p in self.points) + "\n]}"