from pathlib import Path
import json
from sys import stderr
from collections import defaultdict
from random import randint
#import os
#os.system("python function_wrapper.py"
from code_todos.function_wrapper import function_execution_logger
def read_from_json(fpath):
    try:
        with open(fpath, 'r') as fobject:
            return json.load(fobject)
    except OSError as err:
        stderr.write(f"OS Error while trying to open file json.\n{err}\n")
    except json.JSONDecodeError as err:
        stderr.write(f"JSON error while trying to read from json file.\n{err}\n")
@function_execution_logger
def get_team_members_with_max_completed(fpath):
    todos = read_from_json(fpath)
    res_dictionary = defaultdict(int)
    for todo in todos:
        if todo['completed'] != True:
            continue
        res_dictionary[todo['userId']]+=1
    # for key, elem in res_dictionary.items():
    #     print(f"{key}:{elem}")
    # for item in res_dictionary.items(): # vidimo da je item tuple
    #     print(item)
    sorted_dict_tuple =  sorted(res_dictionary.items(), key = lambda elem:elem[1], reverse=True)
    max_completed = sorted_dict_tuple[0][1]
    # print(max_completed)
    return [key for key,val in res_dictionary.items() if val == max_completed]


@function_execution_logger
def write_prioritised_todos(todos):
    for todo in todos:
        todo['priority'] = randint(1,5)
    try:
        with open(Path.cwd()/'../data/todos_prioritised.json', 'w') as fobj:
            json.dump(todos,fobj,indent=4)
    except OSError as err:
        stderr.write(f"OS Error . \n{err}\n")


def write_into_csv(key, val_list):
    import csv
    fname = Path.cwd()/'../data/tasks/'
    name = str(key) +'.csv'
    fname = fname/f"{name}"

    try:
        with open(fname,'w') as fobject:
            csv_writer = csv.writer(fobject)
            for elem in sorted(val_list, key=lambda el:el['priority'],reverse=False):
                csv_writer.writerow((elem['id'],elem['priority'],elem['title']))
    except OSError as err:
        stderr.write(f"OS error.\n{err}\n")

@function_execution_logger
def write_into_csv_prioritised_incompleted_tasks(todos_prioritised):
    dict_incompleted = defaultdict(list)
    for todo in todos_prioritised:
        if todo['completed'] == False:
            dict_incompleted[todo['userId']].append(todo)
    # for key, val in dict_incompleted.items():
    #     print(f"{key}:{val}")
    for key, elem in dict_incompleted.items():
        #za userId upisati ovo --> (task_id, task_priority, task_title)
        write_into_csv(key,elem)


if __name__=='__main__':
    todos = read_from_json(Path.cwd()/'../data/todos.json')
    print(type(todos))
    # for elem in todos:
    #     print(elem)
    members_id = get_team_members_with_max_completed(Path.cwd()/'../data/todos.json')
    # for id in members_id:
    #    print(id)

    # todos = read_from_json(Path.cwd()/'../data/todos.json')
    # write_prioritised_todos(todos)
    #
    # todos_prioritised = read_from_json(Path.cwd()/'../data/todos_prioritised.json')
    # write_into_csv_prioritised_incompleted_tasks(todos_prioritised)

