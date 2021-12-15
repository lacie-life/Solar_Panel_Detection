import os

path = 'dirty' #root/dataset
for ind, filename in enumerate(os.listdir(path)):
    old_name = os.path.join(path, filename)
    new_name = os.path.join(path, str(ind) + '.jpg')

    os.rename(old_name, new_name)
