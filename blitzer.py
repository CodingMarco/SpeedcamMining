import asyncio
from bbox import BBox
import blitzer_downloader
import time
import sys


async def main():
    bbox_de = BBox(west=5.98865807458, south=47.3024876979, east=15.0169958839, north=54.983104153, name="Germany")

    tiles = bbox_de.get_children_bboxes(12)

    time_start = time.perf_counter()

    speedcams = await blitzer_downloader.download_speedcams(tiles)

    elapsed = (time.perf_counter() - time_start)
    rps = len(tiles) / elapsed

    for speedcam in speedcams:
        print(speedcam)

    print("Fetched {} tiles / {} speedcams in {} seconds; {} tiles/second;".format(len(tiles), len(speedcams), elapsed, rps), file=sys.stderr)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(main())
    loop.run_until_complete(future)
