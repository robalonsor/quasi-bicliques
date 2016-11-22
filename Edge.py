#!/usr/bin python3

# from Vertex import Vertex


class Edge(object):

    def __init__(self, vertex1, vertex2, value):
        assert vertex1.type_of_vertex != vertex2.type_of_vertex and vertex1 != vertex2
        if vertex1.type_of_vertex != "a":
            self.vertex1 = vertex2
            self.vertex2 = vertex1
        else:
            self.vertex1 = vertex1
            self.vertex2 = vertex2
        self.value = value

    def __str__(self):
        return "(u = "+str(self.vertex1) + ", v = " + str(self.vertex2) + ") weight = " + str(self.value)

    def __repr__(self):
        return self.__str__()

    def get_other_vertex(self, n):
        if n == self.vertex1: return self.vertex2
        if n == self.vertex2: return self.vertex1
        assert False
        return

    def remove(self, di):
        self.vertex1.delete_edge(di,self)
        self.vertex2.delete_edge(di,self)


# v1 = Vertex(1, "A")
# v2 = Vertex(2, "B")
#
# e = Edge(v1, v2, 100)
# print(e)
# vx = e.get_other_vertex(v2)
#
# print(v1)
# print(vx)
# print(e)
# print(v1.compare(v2))

# e = Edge()
