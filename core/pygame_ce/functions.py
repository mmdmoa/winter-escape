from core.common.names import *

def scale_by(surface:Surface,factor):
    return pg.transform.scale(surface,[surface.get_width()*factor,surface.get_height()*factor])
