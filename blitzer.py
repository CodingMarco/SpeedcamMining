import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from bbox import BBox
import blitzer_downloader
import requests
import time


def main():
    sqlquery = "SELECT lat AS latitude,long AS longitude FROM 'blitzermob' WHERE type=1"
    # https://cdn2.atudo.net/api/3.0/?type=0,1,2,3,4,5,6&z=7&box=48.369631,1.356501,53.838,20.231013
    url_mask = "https://cdn2.atudo.net/api/3.0/?type=0,1,2,3,4,5,6&z=12&box={},{},{},{}"
    db = sqlite3.connect("blitzerm.sqlite")

    bbox_de = BBox(west=5.98865807458, south=47.3024876979, east=15.0169958839, north=54.983104153, name="Germany")
    bbox_de.print_graphically()

    df = pd.read_sql_query(sqlquery, db)
    bbox_db = BBox(west=df.longitude.min(), east=df.longitude.max(),
                   south=df.latitude.min(), north=df.latitude.max(), name="Database")

    children = bbox_de.get_children_bboxes(8)

    print("Nr. of children: %d" % len(children))

    time_start = time.perf_counter()

    for child in children:
        child_url = url_mask.format(child.south, child.west, child.north, child.east)
        response = requests.get(child_url, headers=blitzer_downloader.blitzer_app_headers)
        res_json = response.json()["pois"]
        #rps = 1/(time.perf_counter() - time_start)
        #print("{} r/s, url: {}, response: {}".format(rps, child_url, res_json))
        #time_start = time.perf_counter()

    rps = len(children) / (time.perf_counter() - time_start)
    print("{} r/s".format(rps))


    print("Nr. of children: %d" % len(children))



    exit()

    #os.system("wget https://render.openstreetmap.org/cgi-bin/export?bbox={},{},{},{}&scale=26500000&format=png".format(BBox[0], BBox[2], BBox[1], BBox[3]))
    ruh_m = plt.imread("map.png")

    fig, ax = plt.subplots(figsize=(8, 7))
    ax.scatter(df.longitude, df.latitude, zorder=1, alpha=0.9, c='r', s=10)
    ax.set_title('Mobile und teilstationäre Blitzer')
    ax.set_xlim(bbox[0], bbox[1])
    ax.set_ylim(bbox[2], bbox[3])
    ax.imshow(ruh_m, zorder=0, extent=bbox, aspect='auto')
    #plt.axis('equal')
    plt.show()


if __name__ == '__main__':
    main()