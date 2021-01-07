import os

class Config(object):
    SECREY_KEY = os.environ.get("SECRET_KEY") or b'\xdf\xf0\xe5\x1e\n\xf5zI\xdbsh\xd5\xf0\x1f\x0e4'
   
    