import json
import hashlib
import os
from make_graph import Graph

d = {}
f = open('makefile.txt').readlines()
col = set()


def get_com_dict(f):
    global col
    d = {}
    prevss = ""
    for i in f:
        i = i.replace('\n', '')
        ss = i.split(' ')
        if i != '' and i[0] != ' ' and i[0] != '\t':
            d[ss[0][:-1]] = ss[1:]
            prevss = ss[0][:-1]
            col.add(prevss)
            for _ in ss[1:]:
                col.add(_)
        else:
            try:
                d.setdefault(prevss + "_comands", i)
            except KeyError:
                d[prevss + "_comands"] = i
    return d


def form_graph(col, d={}):
    g = Graph(col)
    for i in d.keys():
        if not str(i).__contains__("_comands"):
            if isinstance(d[i], list):
                for qq in d[i]:
                    g.addEdge(qq, i)
            else:
                g.addEdge(d[i], i)
    return g


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def run_make(li):
    global d
    db = json.loads(open('db.json').read())
    for i in li:
        if i.find('.') != -1:
            if db[i] != md5(i):
                if isinstance(d[i + "_comands"], list):
                    for q in d[i + "_comands"]:
                        os.system(str(q))

                else:
                    os.system(str(d[i + "_comands"]))
                db[i] = md5(i)
        else:
            if isinstance(d[i + "_comands"], list):
                for q in d[i + "_comands"]:
                    os.system(str(q))

            else:
                os.system(str(d[i + "_comands"]))


d = get_com_dict(f)
g = form_graph(len(col), d)

makellist = g.topologicalSort()
run_make(makellist)
