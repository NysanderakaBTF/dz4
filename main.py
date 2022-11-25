import os
import sys
import json
import hashlib

from graph import Graph


def create_dictionary_commands(make_file, count_commands):
    previous = ""
    dictionary_commands = {}

    for line in make_file:
        line = line.replace('\n', '')
        words = line.split(' ')
        if line != '' and line[0] != ' ' and line[0] != '\t':
            dictionary_commands[words[0][:-1]] = words[1:]
            previous = words[0][:-1]
            count_commands.add(previous)
            for i in words[1:]:
                count_commands.add(i)
        else:
            # try:
            dictionary_commands.setdefault(previous + "_comands", line)
            # except KeyError:
            #     dictionary_commands[prevss + "_comands"] = i
    return dictionary_commands


def create_graph(count_commands, dictionary_commands):
    graph = Graph(count_commands)
    for key in dictionary_commands.keys():
        if "_comands" not in str(key):
            if isinstance(dictionary_commands[key], list):
                for i in dictionary_commands[key]:
                    graph.insert_node(i, key)
            else:
                graph.insert_node(dictionary_commands[key], key)
    return graph


def get_hash_file(file_name):
    hash_md5 = hashlib.md5()
    with open(file_name, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def run_make(make_list, dictionary_commands):
    make_list.reverse()
    cache = json.loads(open('__cache__').read())
    if not isinstance(cache, dict):
        cache = {}
    for i in make_list:
        if i.find('.') != -1:
            if cache.get(i) == None:
                if isinstance(dictionary_commands[i + "_comands"], list):
                    for command in dictionary_commands[i + "_comands"]:
                        os.system(str(command))
                else:
                    os.system(str(dictionary_commands[i + "_comands"]))
                try:
                    if cache[i] != get_hash_file(i):
                        cache[i] = get_hash_file(i)
                except:
                    cache[i] = get_hash_file(i)
            elif cache.get(i):
                if cache[i] != get_hash_file(i):
                    try:
                        if isinstance(dictionary_commands[i + "_comands"], list):
                            for command in dictionary_commands[i + "_comands"]:
                                os.system(str(command))
                        else:
                            os.system(str(dictionary_commands[i + "_comands"]))
                        cache[i] = get_hash_file(i)
                    except KeyError:
                        cache[i] = get_hash_file(i)
                        run_make(make_list, dictionary_commands)
        else:
            if isinstance(dictionary_commands[i + "_comands"], list):
                for command in dictionary_commands[i + "_comands"]:
                    os.system(str(command))
            else:
                os.system(str(dictionary_commands[i + "_comands"]))
    generate_cache(cache)


def generate_cache(cache):
    file = open("__cache__", "w")
    file.write(json.dumps(cache))
    file.close()


def create_sub_graph(command, graph, dictionary_commands):
    if command in dictionary_commands.keys():
        if isinstance(dictionary_commands[command], list):
            if len(dictionary_commands[command]) == 0:
                graph.insert_node(command, command)
            for qq in dictionary_commands[command]:
                graph.insert_node(qq, command)
                create_sub_graph(qq, graph, dictionary_commands)
        else:
            graph.insert_node(dictionary_commands[command], command)
    return graph


if __name__ == "__main__":

    dictionary_commands = {}
    makefile = open('makefile.txt').readlines()
    count_commands = set()

    dictionary_commands = create_dictionary_commands(makefile, count_commands)
    graph = create_graph(len(count_commands), dictionary_commands)

    make_list = graph.sort_topologial()

    args = sys.argv
    if len(args) > 1:
        if args[1] == 'clean':
            run_make([args[1]], dictionary_commands)
            generate_cache({})
        else:
            graph = create_sub_graph(args[1], Graph(0), dictionary_commands)
            sort_list_graph = graph.sort_topologial()
            run_make(sort_list_graph, dictionary_commands)
    else:
        run_make(make_list, dictionary_commands)
