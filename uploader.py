import generator as gen
from random import randint
from sys import platform



def get_path(*path):
    if platform == 'win32':
        _path = '\\'.join(path)
    else:
        _path = '/'.join(path)
    return _path 

class Static:
    def stc(self, x):
        self.x = x
        return self.x


St = Static()

def upload(file_bytes, filename):
    code = St.stc(gen.create_link(randint(5, 9)))
    print(f'DEBUG: Code: "{code}" File: "{filename}".')

    with open(get_path('links', code, filename), 'wb') as f:
        f.write(file_bytes)
    return code
    



