class Island:
    def __init__(self, coordinates=None):
        if coordinates is None:
            coordinates = []
        self.coordinates = coordinates

    def add_coordinates(self, coord):
        if coord not in self.coordinates:
            self.coordinates.append(coord)

    def get_coordinates(self):
        return self.coordinates
