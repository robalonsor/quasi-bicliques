#!/usr/bin python3
from Vertex import Vertex
from Edge import Edge


class Cluster(object):
    def __init__(self, u_set, v_set,quality=0):
        self.u_set = u_set
        self.v_set = v_set

    def avg_density(self):
        pass
