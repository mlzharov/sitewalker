import sys
from os.path import dirname
import pprint
from io import StringIO
import nose
from nose.tools import ok_, eq_, raises, assert_tuple_equal, assert_greater

ROOTDIR = dirname(dirname(dirname(__file__)))
sys.path.append(ROOTDIR)

# import application packages
from sitewalker import SimpleGraph, find_diameter


def create_directed_graph():
	nodes = {
        'A' : ['D', 'F'],
        'B' : ['C'],
        'C' : ['E'],
        'D' : ['C', 'E'],
        'E' : ['F'],
        'F' : []}

	return SimpleGraph(nodes)


def create_undirected_graph():
	nodes = {
        'A' : ['D', 'F'],
        'B' : ['C'],
        'C' : ['B', 'D', 'E'],
        'D' : ['A', 'C', 'E'],
        'E' : ['C', 'D', 'F'],
        'F' : ['A', 'E']}

	return SimpleGraph(nodes)



def test_vertices():
	g = create_directed_graph()
	assert_tuple_equal(g.vertices, ('A', 'B', 'C', 'D', 'E', 'F'))

def test_edges():
	g = create_directed_graph()
	assert_tuple_equal(
		g.edges,
		(('A', 'D'), ('A', 'F'), ('B', 'C'), ('C', 'E'),
		 ('D', 'C'), ('D', 'E'), ('E', 'F'))
	)

def test_add_new_vertex():
	g1 = create_directed_graph()
	g2 = create_directed_graph()
	g2.add_vertex('G')
	assert_greater(len(g2.vertices), len(g1.vertices))

def test_add_dup_vertex():
	g1 = create_directed_graph()
	g2 = create_directed_graph()
	g2.add_vertex('A')
	eq_(len(g2.vertices), len(g1.vertices))


@raises(AssertionError)
def test_add_wrong_edge():
	g = create_directed_graph()
	g.add_edge('G', 'A')

def test_add_new_edge():
	g = create_directed_graph()
	g.add_edge('A', 'C')
	ok_(('A', 'C') in g.edges)

def test_add_dup_edge():
	g1 = create_directed_graph()
	g2 = create_directed_graph()
	g2.add_edge('A', 'F')
	eq_(len(g2.edges), len(g1.edges))



def test_diameter():
	# Shortest paths:
	# ['A', 'F'],
	# ['B', 'C'],
	# ['C', 'D'],
	# ['C', 'E'],
	# ['D', 'E'],
	# ['E', 'F'],
	# ['A', 'D', 'C'],
	# ['A', 'D', 'E'],
	# ['B', 'C', 'D'],
	# ['B', 'C', 'E'],
	# ['C', 'E', 'F'],
	# ['D', 'A', 'F'],
	# ['A', 'D', 'C', 'B'],
	# ['B', 'C', 'E', 'F']]

	g = create_undirected_graph()
	path = find_diameter(g)
	eq_(3, len(path) - 1)

if __name__ == '__main__':
    nose.runmodule(argv=['-d', '-s', '--verbose'])
