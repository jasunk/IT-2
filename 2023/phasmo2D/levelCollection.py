import level

level1 = \
    [
        level.Room("Boys Bedroom", [0,0], [600, 400],  "blue", [level.Thing(1,[20,20])]),
        level.Room("Main bathroom", [0,-250], [400, 250],  "red", []),
        level.Room("Foyer", [400,-650], [200, 650],  "yellow", []),
        level.Room("Nursery", [0,-1100], [400, 600],  "pink", []),
        level.Room("Foyer", [600,-850], [200, 850], "green", []),
        level.Room("Foyer", [400,-1100],[200,450],"green",[]),
        level.Room("Master bedroom", [0, -1500],[600,400], "blue",[]),
        level.Room("Master bedroom bathroom", [0, -1900],[400,400], "red",[]),
        level.Room("Master bedroom closet", [400, -1900],[200,400], "orange",[]),
        level.Room("Living Room", [600,-1750], [600, 700], "magenta",[]),
        level.Room("Hallway Living", [600, -1050], [1500, 200], "brown", []),
        level.Room("Kitchen",[1400, -850],[700, 500],"cyan",[]),
        level.Room("Dining room", [1400,-1550],[700,700], "gray", []),
        level.Room("Utility",[1000,-850],[400,500],"orange",[]),
        level.Room("Stairs",[1200,-1450],[200,400],"dark gray",[]),
        level.Room("Garage", [1000, -350], [800, 750], "gray", [])
    ]