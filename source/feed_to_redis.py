import json
import redis
import urllib.request
import source.base_api as base_api
import pyunpack
import os

redis_instance = redis.Redis(host="localhost", port=6379, db=0)
# urllib.request.urlretrieve(
#     "https://drive.usercontent.google.com/download?id=107WikNVtve-QY7I7-pMsdFFHpAnNFxmO&export=download&authuser=0&confirm=t&uuid=ee5e1d68-b3ed-44b8-8b1f-fd8ba89a21a6&at=APvzH3opualeRJvfk4YjiiYkRXtw:1733467797847",
#     base_api.relative_to_abs(["temp-data.zip"]),
# )
# print("download completed")
os.mkdir(base_api.relative_to_abs(["data"]))
pyunpack.Archive(base_api.relative_to_abs(["temp-data.zip"])).extractall(
    base_api.relative_to_abs(["data"])
)
os.unlink(base_api.relative_to_abs(["temp-data.zip"]))

folders_list = os.listdir(base_api.relative_to_abs(["data"]))
for folder in folders_list:
    if not os.path.isdir(base_api.relative_to_abs(["data", folder])):
        continue
    current_file_list = os.listdir(base_api.relative_to_abs(["data", folder]))
    for file in current_file_list:
        with open(base_api.relative_to_abs(["data", folder, file])) as data:
            read = json(data.read())
            eid = read["abstracts-retrieval-response"]["coredata"]["eid"]
            redis_instance.set("{folder}{eid}", json.dumps(read, separators=(",", ":")))
