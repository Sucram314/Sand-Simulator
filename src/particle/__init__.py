from .particle import *
from .empty import *
from .sand import *
from .water import *
from .wall import *
from .dirt import *
from .stone import *
from .smoke import *
from .fire import *
from .wood import *
from .ice import *
from .snow import *
from .lava import *
from .salt import *

ID_TO_CLASS = [Empty,Wall,Sand,Water,Dirt,Stone,Smoke,Fire,Wood,Ice,Snow,Lava,Salt]
N_TYPES = len(ID_TO_CLASS)
MOVABLE = {SAND,WATER,DIRT,STONE,SMOKE,SNOW,LAVA,SALT}