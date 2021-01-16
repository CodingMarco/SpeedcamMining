import matplotlib.pyplot as plt
from bbox import BBox


def draw_map(map_bbox: BBox):
    ruh_m = plt.imread("map.png")

    fig, ax = plt.subplots(figsize=(8, 7))
    #           long,   lat
    ax.scatter(list(), list(), zorder=1, alpha=0.9, c='r', s=10)
    ax.set_title('Mobile und teilstationäre Blitzer')
    ax.set_xlim(map_bbox.west, map_bbox.east)
    ax.set_ylim(map_bbox.south, map_bbox.north)
    ax.imshow(ruh_m, zorder=0, extent=(map_bbox.west, map_bbox.south, map_bbox.east, map_bbox.north), aspect='auto')
    plt.show()
