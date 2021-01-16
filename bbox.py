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

    def get_children_bboxes(self, zoom=12):
        children = list()

        for child in mercantile.tiles(*self.to_mercantile_bbox(), zooms=zoom):
            children.append(BBox.from_mercantile_bbox(mercantile.bounds(child), str(child)))

        return children
