import logging
import argparse

__author__ = 'Sergey Krushinsky'
__copyright__ = "Copyright 2018"
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "krushinsky@gmail.com"

def find_diameter(g):
    '''
    Given graph g, calculate its diameter, i.e.
    maximum eccentricity of any vertex in the graph
    '''
    v = g.vertices
    pairs = [ (v[i],v[j]) for i in range(len(v)-1) for j in range(i+1, len(v)) ]
    shortest_paths = []
    for pair in pairs:
        paths = g.find_all_paths(*pair)
        if len(paths):
            shortest = sorted(paths, key=len)[0]
            shortest_paths.append(shortest)
    shortest_paths.sort(key=len)
    if len(shortest_paths):
        return shortest_paths[-1]
    else:
        return []


if __name__ == '__main__':
    from graph import SimpleGraph

    parser = argparse.ArgumentParser(
        description='Given site map, build a graph and find its diameter')
    parser.add_argument('input',  metavar='FILE', type=str, default='sitemap.json', help='input file name')
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S',
        format='%(asctime)s - %(levelname)-8s - %(message)s',)
    try:
        g = SimpleGraph.from_json(args.input)
        path = find_diameter(g)
        if path:
            d = (len(path)-1)
            print('Length: %d' % d)
            print('\n-->'.join(path))
        else:
            print('Empty!')
    except KeyboardInterrupt:
        logging.warn('Interrupted.')
    except Exception as ex:
        logging.error(ex, exc_info=True)
