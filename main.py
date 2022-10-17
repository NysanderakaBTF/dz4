import json
import hashlib
import os
import sys

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
    print(li)
    global d
    db = json.loads(open('db.json').read())
    for i in li:
        print(i)
        if i.find('.') != -1:
            if len(db.get(i)) == 0:
                if isinstance(d[i + "_comands"], list):
                    for q in d[i + "_comands"]:
                        os.system(str(q))

                else:
                    os.system(str(d[i + "_comands"]))
            elif db.get(i):
                if db[i] != md5(i):
                    try:
                        if isinstance(d[i + "_comands"], list):
                            for q in d[i + "_comands"]:
                                os.system(str(q))

                        else:
                            os.system(str(d[i + "_comands"]))
                        db[i] = md5(i)
                    except KeyError:
                        db[i] = md5(i)
                        run_make(li)


            else:
                try:
                    if isinstance(d[i + "_comands"], list):
                        for q in d[i + "_comands"]:
                            os.system(str(q))

                    else:
                        os.system(str(d[i + "_comands"]))
                    db[i] = md5(i)
                except KeyError:
                    db[i] = md5(i)
                    run_make(li)

        else:
            if isinstance(d[i + "_comands"], list):
                for q in d[i + "_comands"]:
                    os.system(str(q))

            else:
                os.system(str(d[i + "_comands"]))
    file = open("db.json", "w")
    file.write(json.dumps(db))
    file.close()


d = get_com_dict(f)
g = form_graph(len(col), d)
print(d)
makellist = g.topologicalSort()

args = sys.argv
if len(args)>1:
    if args[1]=='clean':
        run_make(['clean_comands'])
    else:
        i = makellist.index(args[1])
        run_make(makellist[:(i+1)])
else:
    run_make(makellist)
