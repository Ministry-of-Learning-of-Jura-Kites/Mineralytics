from datetime import datetime
from itertools import repeat
from multiprocessing import Manager
from pathos.multiprocessing import ProcessingPool as Pool
import pandas as pd
import os
import json

UPDATE_PERCENT_EVERY = 40  # every n updates -> update loading bar


def relative_to_abs(relative_path):
    dirname = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(dirname, *map(str, relative_path))


def load_json(path, filter):
    with open(path, "r", encoding="utf-8") as file:
        df = pd.json_normalize(json.load(file))
    if filter != None:
        df = filter(df)
    return df


def load_data_of_year(year, filter, max=-1):
    manager = Manager()
    counter = manager.Value(0, 0)
    lock = manager.Lock()
    start_time = datetime.now()

    folder_path = relative_to_abs(["data", year])
    files_list = os.listdir(folder_path)
    if max != -1:
        max_files_count = min(len(files_list), max)
    else:
        max_files_count = len(files_list)

    def download(index, file):
        file_abs_path = os.path.join(folder_path, file)
        if os.path.isfile(file_abs_path):
            try:
                data = load_json(file_abs_path, filter)
                with lock:
                    counter.value += 1
                    if (
                        counter.value % UPDATE_PERCENT_EVERY == 0
                        or counter.value == max_files_count
                    ):
                        print(
                            "\rdownloading {message}... [{time}] {percent}%".format(
                                message=year,
                                time=str(datetime.now() - start_time).split(".", 2)[0],
                                percent=round(counter.value / max_files_count * 100, 2),
                            ),
                            end="",
                        )
                    if counter.value == max_files_count:
                        print()
                return data
            except Exception as e:
                print(e, year, index)

    pool = Pool()
    df = pd.concat(
        pool.map(download, range(0, max_files_count), files_list[0:max_files_count])
    )

    return df


def load_all_data(filter):
    manager = Manager()
    counter = manager.Value(0, 0)
    lock = manager.Lock()
    start_time = datetime.now()
    files_list = []
    folders_list = os.listdir(relative_to_abs(["data"]))
    for folder in folders_list:
        current_file_list = os.listdir(relative_to_abs(["data", folder]))
        files_list += map(lambda file: folder + "/" + file, current_file_list)
    max = len(files_list)

    def download(index, file):
        try:
            data = load_json(relative_to_abs(["data", file]), filter)
            with lock:
                counter.value += 1
                if counter.value % UPDATE_PERCENT_EVERY == 0 or counter.value == max:
                    print(
                        "\rdownloading all data... [{time}] {percent}%".format(
                            time=str(datetime.now() - start_time).split(".", 2)[0],
                            percent=round(counter.value / max * 100, 2),
                        ),
                        end="",
                    )
                if counter.value == max:
                    print()
            return data
        except Exception as e:
            print(e, index)

    pool = Pool()
    df = pd.concat(pool.map(download, range(0, len(files_list)), files_list))
    return df
