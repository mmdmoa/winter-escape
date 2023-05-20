import sys
import re
import traceback

try:
    import game
except Exception as e:
    error_message = re.sub(r'\s+', ' ', traceback.format_exc())
    print("[Checkpoint:Error]", error_message.strip())
    print("[Checkpoint:Error]", traceback.format_exc())