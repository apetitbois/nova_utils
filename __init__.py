from .nodes.jsonParser import jsonParser
from .nodes.floatList2Float import floatList2Float

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "jsonParser": jsonParser
    # "floatList2Float": floatList2Float
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "jsonParser": "JSON Parser"
    # "floatList2Float": "Float list to float"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS'] 
