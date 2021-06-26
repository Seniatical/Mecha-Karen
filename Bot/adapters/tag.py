from TagScriptEngine import Adapter, Verb, escape_content


class TagAdapter(Adapter):
    r"""
    Adapter for a TAG object

    Attributes
    ----------

    content:str:The raw data of the tag
    name:str:The name of the tag
    guild:int:The ID of your server
    author:int:The user who created the tag (ID)
    uses:int:A number showing how many times this tag has been used
    nsfw:bool:A boolean showing if the tag should be used in a NSFW channel
    mod:bool:A boolean showing if users require `manage_messages` permissions
    created_at:datetime.datetime:A datetime object which represents the creation date of the tag
    updated_at:datetime.datetime:A datetime object representing when your tag was last updated
    """

    def __init__(self, tag):
        self._attributes = {
            'content': tag.content,
            'name': tag.name,
            'guild': tag.guild,
            'author': tag.author,
            'uses': tag.uses,
            'nsfw': tag.nsfw,
            'mod': tag.mod
        }
        
        super().__init__()

    def get_value(self, ctx: Verb) -> str:
        should_escape = False

        if not ctx.parameter:
            return str(self.object)

        try:
            value = self._attributes[ctx.parameter]
        except KeyError:
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
