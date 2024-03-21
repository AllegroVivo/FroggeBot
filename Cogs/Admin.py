from typing import TYPE_CHECKING

from discord import (
    ApplicationContext,
    Cog,
    SlashCommandGroup,
    Option,
    OptionChoice,
    SlashCommandOptionType,
)

from Classes.Profiles.ProfileHelp import ProfileHelp
from Utilities import ImageType

if TYPE_CHECKING:
    from Classes import FroggeBot
################################################################################
class Admin(Cog):

    def __init__(self, bot: "FroggeBot"):

        self.bot: "FroggeBot" = bot

################################################################################

    admin = SlashCommandGroup(
        name="admin",
        description="Commands for administering Profile creation and management."
    )

################################################################################
    @admin.command(
        name="details",
        description="View and edit Name, URL, Color, Jobs, and Rates."
    )
    async def profile_details(
        self,
        ctx: ApplicationContext,
        user: Option(
            SlashCommandOptionType.user,
            name="user",
            description="The user whose profile to view/edit.",
            required=True
        )
    ) -> None:

        profile = self.bot[ctx.guild_id].get_profile(user)
        await profile.set_details(ctx.interaction)

################################################################################
    @admin.command(
        name="ataglance",
        description="View and edit Gender, Age, Height, and more."
    )
    async def profile_ataglance(
        self,
        ctx: ApplicationContext,
        user: Option(
            SlashCommandOptionType.user,
            name="user",
            description="The user whose profile to view/edit.",
            required=True
        )
    ) -> None:

        profile = self.bot[ctx.guild_id].get_profile(user)
        await profile.set_ataglance(ctx.interaction)

################################################################################
    @admin.command(
        name="personality",
        description="View and edit Personality, Likes, Dislikes, and Bio."
    )
    async def profile_personality(
        self,
        ctx: ApplicationContext,
        user: Option(
            SlashCommandOptionType.user,
            name="user",
            description="The user whose profile to view/edit.",
            required=True
        )
    ) -> None:

        profile = self.bot[ctx.guild_id].get_profile(user)
        await profile.set_personality(ctx.interaction)
        
################################################################################
    @admin.command(
        name="images",
        description="View and edit Thumbnail, Main Image, and Additional Images."
    )
    async def profile_personality(
        self,
        ctx: ApplicationContext,
        user: Option(
            SlashCommandOptionType.user,
            name="user",
            description="The user whose profile to view/edit.",
            required=True
        )
    ) -> None:

        profile = self.bot[ctx.guild_id].get_profile(user)
        await profile.set_images(ctx.interaction)

################################################################################
    @admin.command(
        name="add_image",
        description="Add a Thumbnail, Main Image, or Additional Image to your profile."
    )
    async def profile_add_image(
        self,
        ctx: ApplicationContext,
        user: Option(
            SlashCommandOptionType.user,
            name="user",
            description="The user whose image to edit.",
            required=True
        ),
        section: Option(
            name="field",
            description="Which profile field you want to set with the provided image.",
            choices=[
                OptionChoice(
                    name=ImageType.Thumbnail.proper_name,
                    value=str(ImageType.Thumbnail.value)  # type: ignore
                ),
                OptionChoice(
                    name=ImageType.MainImage.proper_name,
                    value=str(ImageType.MainImage.value)  # type: ignore
                ),
                OptionChoice(
                    name=ImageType.AdditionalImage.proper_name,
                    value=str(ImageType.AdditionalImage.value)  # type: ignore
                )
            ],
            required=True
        ),
        file: Option(
            SlashCommandOptionType.attachment,
            name="file",
            description="The image file to set in the specified field.",
            required=True
        )
    ):

        profile = self.bot[ctx.guild_id].get_profile(user)
        await profile.assign_image(ctx.interaction, ImageType(int(section)), file)

################################################################################
    @admin.command(
        name="preview",
        description="Preview your profile before finalizing it."
    )
    async def profile_preview(
        self,
        ctx: ApplicationContext,
        user: Option(
            SlashCommandOptionType.user,
            name="user",
            description="The user whose profile to view/edit.",
            required=True
        )
    ) -> None:
        
        profile = self.bot[ctx.guild_id].get_profile(user)
        await profile.preview(ctx.interaction)
        
################################################################################
    @admin.command(
        name="finalize",
        description="Finalize and post/update your profile"
    )
    async def profile_finalize(
        self, 
        ctx: ApplicationContext,
        user: Option(
            SlashCommandOptionType.user,
            name="user",
            description="The user whose profile to finalize.",
            required=True
        ),
        channel: Option(
            SlashCommandOptionType.channel,
            name="channel",
            description="The channel to post the profile in.",
            required=True
        )
    ) -> None:

        profile = self.bot[ctx.guild_id].get_profile(user)
        await profile.post(ctx.interaction, channel)

        return

################################################################################
    @admin.command(
        name="export",
        description="Export your profile to import in another server."
    )
    async def profile_export(
        self,
        ctx: ApplicationContext,
        user: Option(
            SlashCommandOptionType.user,
            name="user",
            description="The user whose profile to export.",
            required=True
        )
    ) -> None:

        profile = self.bot[ctx.guild_id].get_profile(user)
        await profile.export(ctx.interaction)
        
################################################################################
def setup(bot: "FroggeBot") -> None:

    bot.add_cog(Admin(bot))

################################################################################
