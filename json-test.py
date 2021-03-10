import json
from os import listdir
from os.path import isfile, join


def load_file(filename):
    f = open(filename)
    data = json.load(f)
    return data

def load_ids_in_file(filename):
    data = load_file(filename)
    ids = [sc["lat"] + "," + sc["lng"] for sc in data]
    #ids = [sc["content"] for sc in data]
    return ids

def print_deleted(filenames):
    ids = list(load_ids_in_file(filenames[0]))

    for filename in filenames:
        file_ids = load_ids_in_file(filename)
        deleted_ids = [the_id for the_id in ids if the_id not in file_ids]
        print(filename + " " + str(deleted_ids))
        for the_id in deleted_ids:
            ids.remove(the_id)

def print_new(filenames):
    ids = list(load_ids_in_file(filenames[0]))

    for filename in filenames:
        file_ids = load_ids_in_file(filename)
        new_ids = [the_id for the_id in file_ids if the_id not in ids]
        print(filename + " " + str(new_ids))
        ids += new_ids

    return ids

def print_new_prev_deleted(filenames):
    prev_file_ids = list(load_ids_in_file(filenames[0]))
    all_ids = list()
    all_new_ids = list()
    all_deleted_ids = list()
    for filename in filenames:
        file_ids = load_ids_in_file(filename)
        new_ids = [the_id for the_id in file_ids if the_id not in prev_file_ids]
        all_new_ids += new_ids
        deleted_ids = [the_id for the_id in prev_file_ids if the_id not in file_ids]
        all_deleted_ids += deleted_ids
        all_ids += new_ids
        prev_file_ids = file_ids
    print([the_id for the_id in all_new_ids if the_id in all_deleted_ids])

def get_unique_speedcams(filenames):
    ids = list(load_ids_in_file(filenames[0]))

    for filename in filenames:
        file_ids = load_ids_in_file(filename)
        new_ids = [the_id for the_id in file_ids if the_id not in ids]
        ids += new_ids

    return ids

def main():
    path = "out_night"
    filenames = sorted([join(path, f) for f in listdir(path) if isfile(join(path, f)) and ".json" in f])

    unique = get_unique_speedcams(filenames)
    for id in unique:
        print("L.marker([" + id + "]).addTo(map)")

if __name__ == '__main__':
    main()
