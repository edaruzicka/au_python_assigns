PIPES = {
    "ST": "straight",
    "CO": "corner",
    "CR": "cross",
    "JT": "junction-t",
    "DI": "diagonals",
    "OU": "over-under"
}

class Tile:
    """
    A Tile.
    """
    def __init__(self, name, select = True):
        self._name = name
        self._select = select
        self._id = "tile"
    
    def get_name(self):
        return self._name

    def get_id(self):
        return self._id
    
    def set_select(self, select):
        self._select = select

    def can_select(self):
        if self._select == True:
            return True
        else:
            return False
    
    def __str__(self):
        str_repre = "Tile ('" + self.get_name() + "', " + str(self.can_select()) + ")"
        return str_repre
    
    def __repr__(self):
        return str(self)


class Pipe(Tile):
    """
    A Pipe.
    
    def __init__(self, orientation):
        super.__init__()
        self._orientation
    """
    def __init__(self, name, orientation = 0, select = True):
        super().__init__(name, select)

        self._orientation = orientation
        self._id = "pipe"
        
    def get_connected(self, side):
        conected_sides = []
        name = self.get_name()
        ori = self.get_orientation()

        # get all connected sides
        if name == "straight":
            for x in range(ori, ori+4, 2):
                conected_sides.append(sides[x%4])
        elif name == "corner":
            for x in range(ori, ori+2, 1):
                conected_sides.append(sides[x%4])
        elif name == "cross":
            for x in range(ori, ori+4, 1):
                conected_sides.append(sides[x%4])
        elif name == "junction-t":
            for x in range(ori+1, ori+4, 1):
                conected_sides.append(sides[x%4])

        # if desired side is in connected sides, remove side from list, else there are no connected sides
        if side in conected_sides:
            conected_sides.remove(side)
        else:
            conected_sides = []

        return conected_sides

    def rotate(self, direction):
        if self._orientation == 0 and direction < 0:
            self._orientation = 3
        elif self._orientation == 3 and direction > 0:
            self._orientation = 0
        else:
            self._orientation += direction

    def get_orientation(self):
        return self._orientation

    def __str__(self):
        str_repre = "Pipe ('" + self.get_name() + "', " + str(self.get_orientation()) + ")"        
        return str_repre

    def __repr__(self):
        return str(self)


class SpecialPipe(Pipe):
    """
    A special Pipe.
    """
    def __init__(self, name, orientation = 0, select = False):
        super().__init__(name, orientation, select)
        self._id = "special_pipe"

    def rotate(self, direction):
        pass

    def __str__(self):
        str_repre = self.get_name() + "(" + str(self.get_orientation()) + ")"
        return str_repre

    def __repr__(self):
        return str(self)


class StartPipe(SpecialPipe):
    """
    A start Pipe.
    """
    def __init__(self, orientation = 0, name = "StartPipe", select = False):
        super().__init__(name, orientation, select)
    
    def get_connected(self, side=None):
        conect_sides = []
        if self.get_orientation() == 0:
            conect_sides.append("N")
        elif self.get_orientation() == 1:
            conect_sides.append("E")
        elif self.get_orientation() == 2:
            conect_sides.append("S")
        elif self.get_orientation() == 3:
            conect_sides.append("W")

        return conect_sides


class EndPipe(SpecialPipe):
    """
    An end Pipe.
    """
    def __init__(self, orientation = 0, name = "EndPipe", select = False):
        super().__init__(name, orientation, select)

    def get_connected(self, side=None):
        conect_sides = []
        if self.get_orientation() == 0:
            conect_sides.append("S")
        elif self.get_orientation() == 1:
            conect_sides.append("W")
        elif self.get_orientation() == 2:
            conect_sides.append("N")
        elif self.get_orientation() == 3:
            conect_sides.append("E")

        return conect_sides


connect_mapping = {
    "ST0": ["N", "S"],
    "ST1": ["E", "W"],
    "ST2": ["N", "S"],
    "ST3": ["E", "W"],
    
    "CO0": ["N", "E"],
    "CO1": ["S", "E"],
    "CO2": ["S", "W"],
    "CO3": ["N", "W"],
    
    "CR0": ["N", "S", "E", "W"],
    "CR1": ["N", "S", "E", "W"],
    "CR2": ["N", "S", "E", "W"],
    "CR3": ["N", "S", "E", "W"],

    "JT0": ["S", "E", "W"],
    "JT1": ["N", "S", "W"],
    "JT2": ["N", "E", "W"],
    "JT3": ["N", "S", "E"],
    }

connect_mapping_i = {
    "ST": [2],
    "CO": [1],
    "CR": [1, 2 , 3],
    "JT": [1, 2],
}

sides = {
    0: "N",
    1: "E",
    2: "S",
    3: "W",
    "N": 0,
    "E": 1,
    "S": 2,
    "W": 3
    }

t_list = connect_mapping["ST0"]
t_list.remove("N")
# print(t_list)

def get_connected_test(name, orientation, side):
    if name not in PIPES:
        raise InvalidCommand
    
    range(0, 3, 2)

ori = 0
side = "N"

# ST straight
result = []
for x in range(ori, ori+4, 2):
    result.append(sides[x%4])
if side in result:
    result.remove(side)
else:
    result = []
print(result)

# CO corner
result = []
for x in range(ori, ori+2, 1):
    result.append(sides[x%4])
if side in result:
    result.remove(side)
else:
    result = []
print(result)

# CR cross
result = []
for x in range(ori, ori+4, 1):
    result.append(sides[x%4])
if side in result:
    result.remove(side)
else:
    result = []
print(result)

# JT junction-t
result = []
for x in range(ori+1, ori+4, 1):
    result.append(sides[x%4])
if side in result:
    result.remove(side)
else:
    result = []
print(result)

# DI diagonals
result = []
result2 = []
for x in range(ori, ori+2, 1):
    result.append(sides[x%4])
for x in range(ori+2, ori+4, 1):
    result2.append(sides[x%4])
    
if side in result:
    result.remove(side)
    print(result)
elif side in result2:
    result2.remove(side)
    print(result2)
