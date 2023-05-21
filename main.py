import sys
import re
import traceback

# done: remove any usage of pygame.transform.scale_by

try:
    import pygame as pg
    try:
        def version():
            v = pg.version
            return f"SDL version: {v.SDL}, pygame version: {v.ver}, python version: {sys.version}"

        print("[CHECKPOINT: Version] :", version())
    except Exception as e:
        print("[CHECKPOINT: Version] : Could not print Pygame's version",e)

    import game
except Exception as e:
    error_message = re.sub(r'\s+', ' ', traceback.format_exc())
    print("[Checkpoint:Error]", error_message.strip())
    print("[Checkpoint:Error]", traceback.format_exc())
