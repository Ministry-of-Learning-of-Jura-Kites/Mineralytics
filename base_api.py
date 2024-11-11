import pandas as pd
import os
import json

def relative_to_abs(relative_path):
  dirname = os.path.dirname(os.path.abspath(__file__))
  return os.path.join(dirname,relative_path)

def load_json(path,filter):
  with open(path, 'r',encoding='utf-8') as file:
    df = pd.json_normalize(json.load(file))
  if filter!=None:
    df=filter(df)
  return df

def load_data_of_year(year,filter,max=-1):
  df = pd.DataFrame()
  folder_path = relative_to_abs('data/{year}'.format(year=year))
  files_list = os.listdir(folder_path)
  if max!=-1:
    max_files_count = min(len(files_list),max-1)
  else:
    max_files_count = len(files_list)
  for index,file in enumerate(files_list):
    if max!=-1 and index+1>max:
      break
    if index%100==0 or index+1==max_files_count:
      print("\x1b[2K\rfinished downloading {year} {percent}%...".format(year=str(year),percent=str(round((index+1)/max_files_count*100,2))),end="")
    file_abs_path = os.path.join(folder_path,file)
    if os.path.isfile(file_abs_path):
      try:
        df = pd.concat([df,load_json(file_abs_path,filter)])
      except Exception as e:
        print(e,year,index)
  print()
  return df

def load_all_data(filter):
  folders_list = os.listdir('data')
  df = pd.DataFrame()
  for folder in folders_list:
    df = pd.concat([df,load_data_of_year(folder,filter)])
  return df
