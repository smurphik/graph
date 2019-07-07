#! /usr/bin/env python3

import sys

try:
    # for methods Graph.gen_rand_tree() & Graph.draw()
    import networkx as nx
    from random import randint, random
    import matplotlib.pyplot as plt
    from matplotlib import MatplotlibDeprecationWarning
    from warnings import filterwarnings
    filterwarnings("ignore", category=MatplotlibDeprecationWarning)
    # for testing
    import os
except:
    pass

class Node:

    def __init__(self, num):
        self.num = num
        self.neighbs = []
        self.nedges = []
        self.marker = False
        self.val = None

    def add_neigh(self, oth, edge_weight=None):
        self.neighbs.append(oth)
        oth.neighbs.append(self)
        e = Edge(self, oth, edge_weight)
        self.nedges.append(e)
        oth.nedges.append(e)
        return e

    def __repr__(self):
        return '({}: {}{}{})'.format(
            self.num,
            [i.num for i in self.neighbs],
            ', val: {}'.format(self.val) if self.val != None else '',
            ', Marked' if self.marker else '',
            )

class Edge:

    def __init__(self, n0, n1, weight=None):
        self.ends = [n0, n1]
        self.weight = weight
        self.marker = False

    def __repr__(self):
        return '<{} -- {}{}{}>'.format(
            self.ends[0].num,
            self.ends[1].num,
            ', weight: {}'.format(self.weight) if self.weight != None else '',
            ', Marked' if self.marker else '',
            )

class Graph:

    def __init__(self, N=None, E=None):
        self.N = N
        self.E = E
        self.nodes = []
        self.edges = []
        self.OFFSET = 1

    def read_edges(self, file=sys.stdin):

        nodes = {}

        for _ in range(self.E):

            # read line
            vals_arr = file.readline().split()
            i, j = tuple(int(x) for x in vals_arr[:2])
            if len(vals_arr) > 2:
                try:
                    val = int(vals_arr[2])
                except ValueError:
                    val = float(vals_arr[2])
            else:
                val = None

            # create nodes
            if i not in nodes:
                nodes[i] = Node(i)
            if j not in nodes:
                nodes[j] = Node(j)

            # connect nodes
            e = nodes[i].add_neigh(nodes[j], val)
            self.edges.append(e)

        self.nodes = [nodes[i] for i in range(self.OFFSET,
                                              len(nodes) + self.OFFSET)]

        if self.N == None:
            self.N = len(self.nodes)
        else:
            assert self.N == len(self.nodes), \
                   'N = {}, len = {}'.format(self.N, len(self.nodes))

    def read_nodes(self, file=sys.stdin):

        self.nodes = [Node(i) for i in range(self.OFFSET, self.N + self.OFFSET)]
        for i in range(self.OFFSET, self.N + self.OFFSET):
            ni = self.nodes[i-self.OFFSET]
            ints = tuple(int(x) for x in file.readline().split())
            for j in ints:
                nj = self.nodes[j-self.OFFSET]
                if nj not in ni.neighbs:
                    e = ni.add_neigh(nj)
                    self.edges.append(e)

        if self.E == None:
            self.E = len(self.edges)
        else:
            assert self.E == len(self.edges), \
                   'E = {}, len = {}'.format(self.E, len(self.edges))

    def write_edges(self, file=sys.stdout):
        for e in self.edges:
            print('{} {}{}'.format(
                      e.ends[0].num, e.ends[1].num,
                      ' {}'.format(e.weight) if e.weight != None else ''),
                  file=file)

    def write_nodes(self, file=sys.stdout):
        sorted_nodes = sorted(self.nodes, key = lambda x: x.num)
        for n in sorted_nodes:
            print(' '.join(str(x.num) for x in n.neighbs), file=file)

    def gen_rand_tree(self, weighted=False, is_weights_int=True):

        if self.E != None:
            print('Number of edges will be changed')

        # Make tree
        tries = max(1000, self.N ** 2)
        g = nx.random_powerlaw_tree(self.N, tries=tries)
        relabel_map = {i: i+1 for i in range(self.N)}
        nx.relabel_nodes(g, relabel_map)

        # Store data to self. fields
        self.E = len(g.edges())
        self.nodes = [Node(i) for i in range(self.OFFSET, self.N + self.OFFSET)]
        for nx_e in g.edges():
            i, j = nx_e[0], nx_e[1]
            ni, nj = self.nodes[i], self.nodes[j]
            e = ni.add_neigh(nj)
            self.edges.append(e)

        # Set random weights
        if weighted:
            for e in self.edges:
                w = randint(0, 10) if is_weights_int else round(random()*10, 1)
                e.weight = w

    def check(self):

        assert len(self.nodes) == self.N
        assert len(self.edges) == self.E

        self.drop_edge_markers()
        for node in self.nodes:
            assert len(node.neighbs) == len(node.nedges), \
                    ('Incorrect node {}'.format(node) + '\nlen(.neighbs): '
                     '{}'.format(len(node.neighbs)) + '\nlen(.nedges): '
                     '{}'.format(len(node.nedges)))
            for neith, nedge in zip(node.neighbs, node.nedges):
                assert len(nedge.ends) == 2, \
                       'Too many ends of edge {}:\n{}'.format(nedge, nedge.ends)
                assert node in nedge.ends, \
                       ('Edge {}'.format(nedge) + ' exists in node '
                        '{}'.format(node) + ' neighbors list, '
                        'but not vice versa')
                oth_end = \
                    nedge.ends[0] if node is nedge.ends[1] else nedge.ends[1]
                assert neith is oth_end, \
                       ('Node {}'.format(neith) + ' should be the end of edge '
                        '{}'.format(nedge) + ' instead of {}'.format(oth_end))
                nedge.marker = True

        for e in self.edges:
            assert e.marker, 'Isolated edge {}'.format(e)
            e.marker = False

    #TODO: del_node, del_edge, change_end

    def drop_node_markers(self):
        for node in self.nodes:
            node.marker = False

    def init_node_vals(self, val):
        for node in self.nodes:
            node.val = val

    def drop_edge_markers(self):
        for edge in self.edges:
            edge.marker = False

    def init_edge_weights(self, val):
        for edge in self.edges:
            edge.val = val

    def draw(self, weighted=False):

        # Make graph & fill data for .dot output
        g = nx.Graph()
        for n in self.nodes:
            g.add_node(n.num, color = 'red' if n.marker else 'black')
        for e in self.edges:
            if weighted:
                g.add_edge(e.ends[0].num, e.ends[1].num, label=e.weight,
                           color = 'red' if e.marker else 'black')
            else:
                g.add_edge(e.ends[0].num, e.ends[1].num,
                           color = 'red' if e.marker else 'black')

        # Fill data for NetworkX draw
        pos = nx.spring_layout(g)
        ecol_map = ['red' if e.marker else 'black' for e in self.edges]
        ncol_map = ['red' if n.marker else 'gray' for n in self.nodes]
        nx.draw_networkx(g, pos=pos, node_color=ncol_map, edge_color=ecol_map,
                         with_labels=True)
        if weighted:
            elab_map = nx.get_edge_attributes(g,'label')
            nx.draw_networkx_edge_labels(g, pos=pos, edge_labels=elab_map)

        # Save & show
        nx.drawing.nx_pydot.write_dot(g, 'fig.dot')
        plt.axis('off')
        plt.savefig('fig.png')
        plt.show()

    def __repr__(self):
        return '\n'.join(str(node) for node in self.nodes[1:])

    def __getitem__(self, i):
        return self.nodes[i - self.OFFSET]

if __name__ == '__main__':

    ### Test

    # Generate, print, draw, check
    N = 11
    g0 = Graph(N)
    g0.gen_rand_tree(True, False)
    g0.write_edges()
    g0.draw(True)
    g0.check()

    # Write by edges, read, check
    g0.write_edges(file=open('tmp_rand_tree.txt', 'w'))
    g1 = Graph(N, N-1)
    f = open('tmp_rand_tree.txt')
    g1.read_edges(f)
    g1.check()
    assert g0.N == g1.N
    assert g0.E == g1.E
    assert g0.edges[3].ends[0].num == g1.edges[3].ends[0].num
    assert g0.edges[3].ends[1].num == g1.edges[3].ends[1].num
    assert g0.edges[3].weight == g1.edges[3].weight

    # Write by nodes, read, check, mark, draw
    g1.write_nodes(open('tmp_rand_tree.txt', 'w'))
    g2 = Graph(N)
    g2.read_nodes(open('tmp_rand_tree.txt'))
    g2.check()
    assert g0.N == g2.N
    assert g0.E == g2.E
    assert g0.edges[3].ends[0].num == g2.edges[3].ends[0].num
    assert g0.edges[3].ends[1].num == g2.edges[3].ends[1].num
    for e in g2[3].nedges:
        e.marker = True
    g2[6].marker = g2[9].marker = True
    g2.draw()
    os.remove('tmp_rand_tree.txt')

