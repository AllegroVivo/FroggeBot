from __future__ import annotations

from discord import Cog
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Classes import FroggeBot
################################################################################
class Internal(Cog):

    def __init__(self, bot: FroggeBot):

        self.bot: FroggeBot = bot

################################################################################
    @Cog.listener("on_ready")
    async def load_internals(self) -> None:

        print("Loading internals...")
        await self.bot.load_all()
        
        print("FroggeBot Online!")

################################################################################
    @Cog.listener("on_guild_join")
    async def on_guild_join(self, guild) -> None:

        self.bot.fguilds.add_new_guild(guild)

################################################################################
def setup(bot: FroggeBot) -> None:

    bot.add_cog(Internal(bot))

################################################################################
