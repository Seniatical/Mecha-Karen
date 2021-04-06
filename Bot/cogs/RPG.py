## COMING SOON!
## UNIQUE ECONOMY SYSTEM
## SELF-DRIVEN ECONOMY
## Meh Related.
## PARTNERING WITH PLEB

from .RPG import Cog
from .RPG import Support
from .RPG import Use
from .RPG import EcoOwner

def setup(bot):
    bot.add_cog(Cog(bot))
    bot.add_command(Use)
    bot.add_cog(Support(bot))
    bot.add_cog(EcoOwner(bot))
