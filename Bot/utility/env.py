from typing import Union
from warnings import warn
import ast

class Enviroment:
    def __init__(self, path: str = './.env') -> None:
        self.path = path
        self.file = open(path)

        vars = self.file.readlines()
        self.vars = tuple(map(self.cleanse, vars))

        self.maps = {}
        for var in self.vars:
            try:
                k, v = var.split(' = ')
            except ValueError:
                continue

            try:
                v = ast.literal_eval(v)
            except Exception as error:
                warn('Failed to convert `{}` into a variable - {}\n\nValue: {}'.format(k, error, v), category=Warning)
                continue

            self.maps.update({k: v})

    def __call__(self, variable: str) -> Union[None, str, int, bool]:
        return self.maps.get(variable)

    @staticmethod
    def cleanse(line: str, chardet: str = '\n') -> str:
        return line.strip(chardet)
