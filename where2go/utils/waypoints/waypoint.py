import random, re
from typing import Any, Union
from typing import TypedDict
from mcdreforged.api.all import ServerInterface

formatting_codes = "0123456789abcdef"

class WaypointDict(TypedDict):
    pos: tuple
    dimension: int
    name: str
    title: str
    color: str


class Waypoint:

    def __init__(self, pos: tuple, dimension: str, name: str, title: str = None, color: Union[int, str] = None) -> None:
        '''Create a waypoint

Parameters
----
pos : tuple (pos_x: int, pox_y: int, pox_z: int)

dimension : str
  "overworld", "the_nether", "the_end"

name : str
  The name of the waypoint

color : int | str
  0-9 | a-f
  A minecraft formatting code representing the color of the waypoint
  If None, randomly generate'''

        self.pos: tuple = pos
        self.dimension: str = dimension
        self.name: str = name
        if not title:
            title = name[0] if len(name) > 0 else ""
        self.title: str = title
        if type(color) == int:
            color = str(formatting_codes[color]) if color < len(formatting_codes) else random.choice(formatting_codes)
        elif type(color) != str or color not in formatting_codes:
            color = random.choice(formatting_codes)
        self.color: str = color
     

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, Waypoint) and self.pos == __value.pos
    

    def distance(self, pos):
        return sum([(i-k)**2 for i,k in zip(self.pos, pos)])**0.5
    

    def is_close_to(self, pos: tuple, distance: int):
        return sum([(i-k)**2 for i,k in zip(self.pos, pos)]) <= distance**2


    def to_dict(self) -> WaypointDict:
        return {
            "pos": self.pos,
            "dimension": self.dimension,
            "name": self.name,
            "title": self.title,
            "color": self.color
        }


    def transform_xaero_waypoint(content: str):
        # xaero-waypoint:NAME:TITLE:X:Y:Z:COLOR:false:0:DIMENSION
        result = re.fullmatch("xaero-waypoint:(.+):(.+):(-?[0-9]+):(-?[0-9]+):(-?[0-9]+):([0-9]{0,2}):.+:Internal-(.+)-waypoints", content)
        if not result:
            return
        name, title, x, y, z, color, dimension = result.groups()
        dimension = dimension.replace("-","_")
        return Waypoint((int(x), int(y), int(z)), dimension, name, title, int(color))
    

    def get_xaero_waypoint(self, dimensions_map = {"overworld": "Internal-overworld-waypoints", "the_nether": "Internal-the-nether-waypoints", "the_end": "Internal-the-end-waypoints"}):
        return f"xaero-waypoint:{self.name}:{self.title}:{':'.join(map(str,self.pos))}:{formatting_codes.index(self.color)}:false:0:{dimensions_map[self.dimension]}"
    
    def get_xaero_waypoint_add(self):
        return f"xaero_waypoint:{self.name}:{self.title}:{':'.join(map(str,self.pos))}:{formatting_codes.index(self.color)}:false:0:Internal-{self.dimension}-waypoints"
