import time
from random import random
from collections import deque

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib import parse

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}


def visit(href):
    url = 'https://namu.wiki' + href
    req = Request(url, headers=headers)
    page = urlopen(req)
    bs = BeautifulSoup(page.read(), "lxml")
    internals = bs.findAll("a", {"class": "wiki-link-internal"})
    return internals


def bfs(start, links, target):
    q = deque(links)
    visited = {start['href']}
    run = 0
    while q:
        if run % 10 == 0:
            time.sleep(5 * random() + 1)
        node = q.popleft()
        history = node['history']
        conds = [node['href'] in visited,
                 node['title'].startswith(('나무위키', '파일:',)),
                 node.text.startswith(('나무위키', '파일:', ' 문단'))]
        if node['title'] == target:
            return node['history']
        elif not any(conds):
            print(run, node['title'], node.text)
            history += '/' + node['title']
            try:
                links = visit(node['href'])
                visited.add(node['href'])
                for i in range(len(links)):
                    links[i]['history'] = history
                q.extend(links)
            except Exception as e:
                print(str(e))
                print(node)
        else:
            print(run, 'not--', node['title'], node.text)
        run += 1


def main(start, target):
    href = "/w/" + parse.quote(start)
    links = visit(href)
    s = set()
    to_visit = []
    for link in links:
        if len(link['title']) > 0 and link['title'] not in s:
            link['history'] = str(start)
            s.add(link['title'])
            to_visit.append(link)
    path = bfs({'href': href}, to_visit, target)
    return path


res = main('고양이', '물티슈')
print(res)

print()
