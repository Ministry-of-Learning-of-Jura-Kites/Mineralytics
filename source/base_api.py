from datetime import datetime
from itertools import repeat
from pathos.multiprocessing import ProcessingPool as Pool
from pathos.helpers import mp as multiprocess
import pandas as pd
import os
import json
from typing import Callable, List
import traceback

UPDATE_PERCENT_EVERY = 40  # every n updates -> update loading bar


def relative_to_abs(relative_path: List[any]) -> str:
    dirname = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(dirname, "..", *map(str, relative_path))


def load_json(path: str, filter: Callable[[pd.DataFrame],pd.DataFrame]) -> pd.DataFrame:
    with open(path, "r", encoding="utf-8") as file:
        df = pd.json_normalize(json.load(file))
    if filter != None:
        df = filter(df)
    return df

def download_function(counter,counter_lock,start_time,max,has_exit,has_exit_lock,filter):
      def download(index: int, file: str):
        if has_exit.value:
          return
        try:
            data = load_json(relative_to_abs(["data", file]), filter)
            with counter_lock:
                counter.value += 1
            if counter.value % UPDATE_PERCENT_EVERY == 0 or counter.value == max:
                print(
                    "\33[2K\rdownloading all data... [{time}] {percent}%".format(
                        time=str(datetime.now() - start_time).split(".", 2)[0],
                        percent=round(counter.value / max * 100, 2),
                    ),
                    end="",
                )
            if counter.value == max:
                print()
            return data
        except Exception as e:
            print("error:",traceback.format_exc(),"\nfrom index:", index,", file:",file)
            with has_exit_lock:
              has_exit.value=True
      return download

def load_data_of_year(year: int, filter:  Callable[[pd.DataFrame],pd.DataFrame], max_files_count: int=-1):
    
    def read_data():
      folder_path = relative_to_abs(["data", year])
      files_list = os.listdir(folder_path)
      actual_max_files_count = max_files_count
      if actual_max_files_count != -1:
          actual_max_files_count = min(len(files_list), actual_max_files_count)
      else:
          actual_max_files_count = len(files_list)
      return (map(lambda file: os.path.join(str(year),file),files_list),max_files_count)

    return load_data(read_data,filter)


def load_data(read_data: Callable[[],None],filter: Callable[[pd.DataFrame],pd.DataFrame]):
    manager = multiprocess.Manager()
    counter = manager.Value(0, 0)
    counter_lock = manager.Lock()

    has_exit_manager = multiprocess.Manager()
    has_exit = has_exit_manager.Value(0, False)
    has_exit_lock = has_exit_manager.Lock()
    
    start_time = datetime.now()

    files_list,max_files_count=read_data()

    pool = Pool()

    print()
    
    data = pool.map(download_function(counter,counter_lock,start_time,max_files_count,has_exit,has_exit_lock,filter), range(0, max_files_count), files_list)
    if has_exit.value:
      exit(1)
    df = pd.concat(data)
    return df


def load_all_data(filter: Callable[[pd.DataFrame],pd.DataFrame]):
  def read_data():
    files_list = []
    folders_list = os.listdir(relative_to_abs(["data"]))
    for folder in folders_list:
        current_file_list = os.listdir(relative_to_abs(["data", folder]))
        files_list += map(lambda file: os.path.join(folder,file), current_file_list)
    return (files_list,len(files_list))
  return load_data(read_data,filter)