import json
from os import listdir
from os.path import isfile, join


def load_file(filename):
    f = open(filename)
    data = json.load(f)
    return data


def load_json_files(filenames):
    jsons = list()
    for file in filenames:
        jsons.append(load_file(file))
    return jsons


def dump_formatted_json(data, filename):
    outfile = open(filename, "w")
    json_string = json.dumps(data, indent=4, ensure_ascii=False)
    outfile.write(json_string)
    outfile.close()


def dump_json(data, filename):
    outfile = open(filename, "w")
    json_string = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
    outfile.write(json_string)
    outfile.close()


def get_json_filenames_in_dir(path):
    filenames = sorted([join(path, f) for f in listdir(path) if isfile(join(path, f)) and ".json" in f])

    return filenames

