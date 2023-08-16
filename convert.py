import os


DIR = os.path.join(os.getcwd(),'videos')
files = []
for i in os.listdir(DIR):
    files.append(os.path.join(DIR, i))

files.sort(key=os.path.getmtime, reverse=True)

print(files)