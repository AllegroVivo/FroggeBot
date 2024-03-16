from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from discord import Interaction, User, ButtonStyle
from discord.ui import Button

from UI.Common import FroggeView, CloseMessageButton, CloseMessageView, ProfileSectionButton

if TYPE_CHECKING:
    from Classes import Profile
################################################################################

__all__ = ("ProfilePreView",)

################################################################################        
class ProfilePreView(FroggeView):

    def __init__(self, owner: User, profile: Profile):

        super().__init__(owner, close_on_complete=True)

        self.profile: Profile = profile
        
        button_list = [
            ProfilePreviewButton(),
            AboutMePreviewButton(self.profile.aboutme),
            CloseMessageButton()
        ]
    
        for btn in button_list:
            self.add_item(btn)

################################################################################
class ProfilePreviewButton(Button):

    def __init__(self):
        super().__init__(
            style=ButtonStyle.primary,
            label="Main Profile",
            disabled=False,
            row=0
        )

    async def callback(self, interaction: Interaction):
        profile, _ = self.view.profile.compile()
        view = CloseMessageView(interaction.user)

        await interaction.respond(embed=profile, view=view)
        await view.wait()

################################################################################
class AboutMePreviewButton(ProfileSectionButton):

    def __init__(self, aboutme: Optional[str]):
        super().__init__(
            label="About Me Section",
            disabled=aboutme is None,
            row=0
        )
        
        self.set_style(aboutme)

    async def callback(self, interaction: Interaction):
        _, aboutme = self.view.profile.compile()
        view = CloseMessageView(interaction.user)

        await interaction.respond(embed=aboutme, view=view)
        await view.wait()

################################################################################
