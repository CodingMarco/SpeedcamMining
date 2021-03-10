import sc_utils


def main():
    filenames = sc_utils.get_json_filenames_in_dir("out_night")
    jsons = sc_utils.load_json_files(filenames)
    unique_speedcams = jsons[0]

    prev_sc = jsons[0]
    for json in jsons:
        for speedcam in json:
            if not any(sc["content"] == speedcam["content"] for sc in prev_sc):
                unique_speedcams.append(speedcam)
        prev_sc = json

    sc_utils.dump_json(unique_speedcams, "speedcams.json")


if __name__ == '__main__':
    main()

