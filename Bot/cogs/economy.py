## COMING SOON!
## UNIQUE ECONOMY SYSTEM
## SELF-DRIVEN ECONOMY
## Meh Related.

from .Economy import Cog
from .Economy import Support
from .Economy import Use
from .Economy import EcoOwner

def setup(bot):
    bot.add_cog(Cog(bot))
    bot.add_command(Use)
    bot.add_cog(Support(bot))
    bot.add_cog(EcoOwner(bot))
