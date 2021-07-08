from TagScriptEngine import Adapter, Verb, escape_content
from ast import literal_eval


class ArgumentAdapter(Adapter):
    r""" A class which will parse `*args` into your tag """

    def __init__(self, *args):
        self.args = args
        self._methods = {}

        self.object = self.__repr__()
        super().__init__()

    def __repr__(self):
        return "< TagArguments [{!r}] >".format(len(self.args))

    def get_value(self, ctx: Verb):
        should_escape = False

        if not ctx.parameter:
            return self.object
        
        parameter = ctx.parameter
        
        if ':' in parameter:
            parameter.split(':')[:3]
            _ = []
            for _slice in slices:
                if not _slice.isdigit() or _slice:
                    ## Means that the slice given was something useless
                    return str()
                if _slice:
                    _.append(int(_slice)) 
                else:
                    _.append(None)
            _slice = slice(*_)
            
            return args[_slice]
        
        try:
            value = self.args[int(ctx.parameter)]
        except (IndexError, ValueError):
            if method := self._methods.get(ctx.parameter):
                value = method()
            else:
                return str()

        if isinstance(value, tuple):
            value, should_escape = value

        if not value:
            return_value = str()
        else:
            return_value = str(value)

        if should_escape:
            return escape_content(return_value)
        return return_value
