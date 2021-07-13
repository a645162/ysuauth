import os
import re

path = os.getcwd()
files = os.listdir(path)
# print(files)
for filename in files:
    result = re.search(r".*\.log", filename.strip())
    if result is not None:
        name1 = result.group()
        print("Remove file ", name1)
        os.remove(name1)
