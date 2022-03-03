import os
from bs4 import BeautifulSoup
import pandas as pd
import requests
import math
import threading
from cxkParser.config import config


def not_empty(str):
    return str and str.strip()


def is_file(path):
    return os.path.isfile(path)


def read_data(path):
    model_list = []
    type_list = ['csv', 'xlsx', 'xls']
    for file in os.listdir(path):
        file_suffix = file.split('.')[-1]
        if is_file(os.path.join(path, file)) and file_suffix in type_list:
            print(file)
        if file_suffix not in type_list:
            continue
        config.file_name_list.append(str(file))
        full_path = os.path.join(path, file)
        if file_suffix == 'csv':
            data = pd.read_csv(full_path)
        else:
            data = pd.read_excel(full_path)
        if 'target_id' not in data:
            raise Exception("id column name must be target_id.")
        model_list.append(data['target_id'])
    return model_list


def model_split(model_list, thread_num):
    concurrency_model_list = []
    for model in model_list:
        num_per_group = math.ceil(len(model) / thread_num)
        concurrency_model_list.append(
            [model[i:i+num_per_group] for i in range(0, len(model), num_per_group)])
    return concurrency_model_list


def parse(model_group):
    for id in model_group:
        full_url = config.base_url + id + config.url_suffix
        doc = requests.get(full_url).text
        doc = BeautifulSoup(doc, features="lxml")
        flag = doc.find(
            "div", id="pfam-domain-list")
        if flag is None:
            config.result_list.append(
                {"target_id": str(id), "annotation": None})
        else:
            annotation = flag.get_text().strip().splitlines()
            annotation = list(filter(not_empty, annotation))
            config.result_list.append(
                {"target_id": str(id), "annotation": annotation[3]})
        print(f"{id}: done")


class Cxk_Task(threading.Thread):
    def __init__(self, thread_id, name, task):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.task = task

    def run(self):
        parse(self.task)
        print(f"{self.name} thread done")


def save(output_path, result_list, file_name):
    df = pd.DataFrame.from_dict(result_list)
    df.index += 1
    if is_file(output_path):
        df.to_excel(output_path)
    else:
        output_path = os.path.join(output_path, 'annotation_' + file_name)
        df.to_excel(output_path)


def do_task(model_list_group, thread_nums, output_path):
    thread_list = []
    for i in range(len(model_list_group)):
        for j in range(thread_nums):
            thread = Cxk_Task(j, "Thread-" + str(j),
                              model_list_group[i][j])
            thread_list.append(thread)
        for t in thread_list:
            t.start()
        for t in thread_list:
            t.join()
        save(output_path, config.result_list, config.file_name_list[i])
        thread_list.clear()
        config.result_list.clear()
