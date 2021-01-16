import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import mercantile


class BBox:
    def __init__(self, west, south, east, north, name="BBox"):
        self.west = west
        self.south = south
        self.east = east
        self.north = north
        self.name = name

    @classmethod
    def from_mercantile_bbox(cls, mercantile_bbox: mercantile.LngLatBbox, name="BBox"):
        return cls(mercantile_bbox.west, mercantile_bbox.south, mercantile_bbox.east, mercantile_bbox.north, name)

    def __str__(self):
        return "west = {}, south = {}, east = {}, north = {}".format(self.west, self.south, self.east, self.north)

    def print_graphically(self):
        nr_dashes = 50
        print("{}: {}".format(self.name, (nr_dashes - len(self.name) - 2) * "-"))
        print("\t\t\t\t\tN")
        print("\t\t\t{}\t\t".format(self.north))
        print("W\t{}\t\t{}\tE".format(self.west, self.east))
        print("\t\t\t{}\t\t".format(self.south))
        print("\t\t\t\t\tS")
        print(nr_dashes * "-")

    def to_mercantile_bbox(self):
        return self.west, self.south, self.east, self.north


def print_children(bbox: BBox):
    tile = mercantile.bounding_tile(*bbox.to_mercantile_bbox())
    children = mercantile.children(tile, zoom=12)
    mercantile.children()

    for child in children:
        BBox.from_mercantile_bbox(mercantile.bounds(child), str(child)).print_graphically()
    print("Children at Z=12: %d" % len(children))


def main():
    sqlquery = "SELECT lat AS latitude,long AS longitude FROM 'blitzermob' WHERE type=1"
    db = sqlite3.connect("blitzerm.sqlite")

    bbox_de = BBox(west=5.98865807458, south=47.3024876979, east=15.0169958839, north=54.983104153, name="Germany")
    bbox_de.print_graphically()

    df = pd.read_sql_query(sqlquery, db)
    bbox_db = BBox(west=df.longitude.min(), east=df.longitude.max(),
                   south=df.latitude.min(), north=df.latitude.max(), name="Database")

    BBox.from_mercantile_bbox(mercantile.bounds(mercantile.bounding_tile(*bbox_de.to_mercantile_bbox())), "Germany master tile").print_graphically()
    print_children(bbox_de)

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