import json
from operator import itemgetter
import logging

__author__ = 'Sergey Krushinsky'
__copyright__ = "Copyright 2018"
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "krushinsky@gmail.com"

class SimpleGraph:
    '''Simple graph represented by a dictionary.
    May be either directed or undirected depending on the dictionary.
    '''
    def __init__(self, data=None):
        '''
        Initializer.
        data is dictionary where keys are nodes and values are
        lists of connected nodes.
        '''
        if data is None:
            data = {}
        self._data = data
        self._edges = None

    def __str__(self):
        return json.dumps(self._data, sort_keys=True, indent=4)

    @property
    def vertices(self):
        '''Return tuple of all the vertices'''
        return tuple(self._data.keys())

    @property
    def edges(self):
        '''
        Return edges represented as tuple sets with one
        (a loop back to the vertex) or two vertices.
        '''
        if self._edges is None:
            self._edges = []
            for vtx in self._data: 
                for neighbour in self._data[vtx]:
                    if not (vtx, neighbour) in self._edges:
                        self._edges.append((vtx, neighbour))
            # TODO: sort function for custom types 
            self._edges = sorted(self._edges, key=itemgetter(0,1))
        return tuple(self._edges)

    def add_vertex(self, vtx):
        '''Add new vertex if it doesn't exist in the graph.'''
        self._data.setdefault(vtx, [])

    def add_edge(self, a, b):
        '''Add edge from a to b if it doesn't exist.
        '''
        assert a in self._data, 'No such vertex: {}'.format(a)
        assert b in self._data, 'No such vertex: {}'.format(b)
        if not b in self._data[a]:
            self._data[a].append(b)
            self._edges = None

    @classmethod
    def from_json(cls, path):
        '''Return new Graph based on data from JSON file.'''
        with open(path) as f:
            logging.info('loading graph from %s...', path)
            return SimpleGraph(json.loads(f.read()))

    def find_all_paths(self, start_vtx, end_vtx, path=None):
        """Find all paths from start_vtx to end_vtx"""
        if path is None:
            path = []
        path = path + [start_vtx]
        if start_vtx == end_vtx:
            return [path]
        if start_vtx not in self._data:
            return []
        paths = []
        for v in self._data[start_vtx]:
            if not v in path:
                ext_paths = self.find_all_paths(v, end_vtx, path)
                for p in ext_paths:
                    paths.append(p)
        return paths


