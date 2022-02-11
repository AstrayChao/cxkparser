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
    for file in os.listdir(path):
        if is_file(os.path.join(path, file)):
            print(file)
            config.file_name_list.append(str(file))
        file_suffix = file.split('.')[-1]
        if file_suffix not in ['csv', 'xlsx', 'xls']:
            continue
        full_path = os.path.join(path, file)
        if file_suffix == 'csv':
            data = pd.read_csv(full_path)
        else:
            data = pd.read_excel(full_path)
        if 'target_id' not in data:
            raise Exception("请调好格式，以target_id作为那个id的列名")
        model_list.append(data['target_id'])
    return model_list


def model_split(model_list, thread_num):
    concurrency_model_list = []
    for model in model_list:
        num_per_group = math.ceil(len(model) / thread_num)
        concurrency_model_list.append(
            [model[i:i+num_per_group] for i in range(0, len(model), num_per_group)])
    return concurrency_model_list


def parse_concurrency(model_group):
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


class cxkTask(threading.Thread):
    def __init__(self, threadID, name, task):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.task = task

    def run(self):
        parse_concurrency(self.task)
        print(f"{self.name} 线程退出")


def save(output_path, result_list, file_name):
    df = pd.DataFrame.from_dict(result_list)
    df.index += 1
    if is_file(output_path):
        df.to_excel(output_path)
    else:
        output_path = os.path.join(output_path, 'annotation_' + file_name)
        df.to_excel(output_path)


def doTask(model_list_group, thread_nums, output_path):
    thread_list = []
    for i in range(len(model_list_group)):
        for j in range(thread_nums):
            thread = cxkTask(j, "Thread-" + str(j),
                                model_list_group[i][j])
            thread_list.append(thread)
        for t in thread_list:
            t.start()
        for t in thread_list:
            t.join()
        save(output_path, config.result_list, config.file_name_list[i])
        thread_list.clear()
        config.result_list.clear()
