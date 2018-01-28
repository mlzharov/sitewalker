# sitewalker

Traverse site and represent it as a graph.

One script, given a URL, does a website crawl with depth up to N,
and writes some data to a JSON file. Other scripts help to explore graph based on
the saved data.

Please, note: this is only a demo (or prototype), not a production-ready software!

## Requirements

* Python >= 3.5
* Requests library

## Installation

```
$ pip install -r requirements.txt
```

Or:

```
$ python setup.py develop
```

Python virtual environment is strongly recommended.

## Testing

```
$ python tests/test_graph.py
```

## Running

### Site scrapping

First, traverse a site, e.g.

```
$ python sitewalker/traverse.py -d4  http://python.org/
```

* Sitemap named **"sitemap.json"** will be saved to a JSON file. You may choose
  another file name via **-o** command line parameter
* **-d4** means maximal depth of 4 levels.

To see all available options, type:

```
$ python sitewalker/traverse.py --help
```

#### Logging

* To see extra logging, set **'DEBUG_SCRAPER'** environment variable to **1**.
* To see detailed logging, set **'DEBUG_SCRAPER'** to **2**.


### Exploring

To calculate the graph **diameter**:

```
$ python sitewalker/diameter.py sitemap.json
```

Sample output:

```
Length: 2
/
-->/psf-landing/
-->/psf/volunteer
```

Length shows the longest distance, in graph edges, between two nodes. Next goes
the list of the path nodes.

- - -

## Caveats

This program is not capable of working with dynamic sites, such as Single Page
Applications. Futher, it makes some naive assumptions:

* URLs from the same domain belong to the same site, which is not always true.
* Different domains mean different sites. So, *weather.yandex.ru* and
  *tv.yandex.ru* are recognized as different sites.
* **.WWW** prefixes in domain names are not important. Thus, *www.python.org* is
  the same entry as *python.org*. It works in most cases.
* Parameter and query parts of an URL do not determine page addresses. E.g.
  *http://example.com/* and  *http://example.com/?foo=bar* are treated as the
  same page. There are few web frameworks that generate different pages for
  different queries.

## TODOs

1. Add more methods for exploring site maps, including visualization.
1. Add configuration file.
1. Make site traversal asynchronous.
1. Replace recursive traversal function with Producer/Consumer design.
1. Add proxy support.
1. Allow unlimited depth.
1. Add width limit (maybe, based on graph diameter).
1. Use  [NetworkX](https://networkx.github.io/) library instead of custom graph.
