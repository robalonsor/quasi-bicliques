#!/usr/bin python3

class Cluster(object):
    def __init__(self, u_set, v_set,quality=0):
        self.u_set = u_set
        self.v_set = v_set

    def __str__(self):
        return "Cluster: {u = "+str(self.u_set) + ", v = " + str(self.v_set) + "}"

    def __repr__(self):
        return self.__str__()

    def avg_density(self):
        pass
