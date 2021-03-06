import asyncio
import time
import sys
import json
from datetime import datetime

from bbox import BBox
import speedcam_downloader

logfile = open("log.txt", "w")


def write_log(text):
    now = datetime.now()
    logfile.writelines([now.strftime("%d.%m.%Y, %H:%M:%S Uhr    |    ") + text + "\n"])
    logfile.flush()
    print(now.strftime("%d.%m.%Y, %H:%M:%S Uhr    |    ") + text + "\n")


async def main():
    bbox_de = BBox(west=5.98865807458, south=47.3024876979, east=15.0169958839, north=54.983104153, name="Germany")

    tiles = bbox_de.get_children_bboxes(12)  # Optimal: 12

    for i in range(1000000, 1000100):
        try:
            jsonfile = open("out/speedcams_{}.json".format(i), "w")

            time_start = time.perf_counter()

            speedcams = await speedcam_downloader.download_speedcams(tiles, "DE")

            elapsed = (time.perf_counter() - time_start)
            rps = len(tiles) / elapsed

            write_log("Fetched {} tiles / {} speedcams in {} seconds; {} tiles/second;".format(len(tiles), len(speedcams), elapsed, rps))

            json_string = json.dumps(speedcams, indent=4, ensure_ascii=False)
            jsonfile.write(json_string)
            jsonfile.close()

            time.sleep(10)
        except Exception as ex:
            print("Error: " + str(ex))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(main())
    loop.run_until_complete(future)
