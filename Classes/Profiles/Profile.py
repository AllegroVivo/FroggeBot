from __future__ import annotations

import json
from typing import TYPE_CHECKING, Optional, Any, Type, TypeVar, Dict, Tuple, List

from discord import (
    User,
    NotFound,
    Interaction,
    Colour,
    Attachment,
    Embed,
    TextChannel,
    Forbidden,
    EmbedField,
    Message,
    File
)

from Assets import BotEmojis, BotImages
from UI.Common import CloseMessageView, ConfirmCancelView
from UI.Profiles import AdditionalImageCaptionModal, ProfilePreView
from Utilities import (
    Utilities as U,
    FroggeColor,
    ImageType,
    TooManyImagesError,
    NS,
    CharNameNotSetError,
    ExceedsMaxLengthError,
    ChannelTypeError,
    InsufficientPermissionsError
)
from .ProfileAtAGlance import ProfileAtAGlance
from .ProfileDetails import ProfileDetails
from .ProfileImages import ProfileImages
from .ProfilePersonality import ProfilePersonality

if TYPE_CHECKING:
    from Classes import ProfileManager, FroggeBot
################################################################################

__all__ = ("Profile",)

P = TypeVar("P", bound="Profile")

################################################################################
class Profile:
    
    __slots__ = (
        "_mgr",
        "_user",
        "_id",
        "_details",
        "_aag",
        "_personality",
        "_images",
    )

################################################################################
    def __init__(self, mgr: ProfileManager, user: User, **kwargs) -> None:
        
        self._mgr: ProfileManager = mgr
        self._user: User = user
        self._id: str = kwargs.pop("_id")
        
        self._details: ProfileDetails = ProfileDetails(self, **kwargs)
        self._aag: ProfileAtAGlance = ProfileAtAGlance(self, **kwargs)
        self._personality: ProfilePersonality = ProfilePersonality(self, **kwargs)
        self._images: ProfileImages = ProfileImages(self, **kwargs)
    
################################################################################    
    @classmethod
    def new(cls: Type[P], mgr: ProfileManager, user: User) -> P:
        
        new_id = mgr.bot.database.insert.profile(mgr.guild_id, user.id)
        return cls(mgr, user, _id=new_id)
    
################################################################################
    @classmethod
    async def load(cls: Type[P], mgr: ProfileManager, data: Dict[str, Any]) -> Optional[P]:
        
        profile = data["profile"]
        addl_imgs = data["additional_images"]
        
        try:
            user = await mgr.bot.fetch_user(profile[1])
        except NotFound:
            return
        
        self: P = cls.__new__(cls)
        
        self._mgr = mgr
        self._user = user
        self._id = profile[0]
        
        self._details = ProfileDetails.load(self, profile[3:9])
        self._personality = ProfilePersonality.load(self, profile[9:13])
        self._aag = ProfileAtAGlance.load(self, profile[13:21])
        self._images = ProfileImages.load(self, profile[21:23], addl_imgs)
        
        return self
        
################################################################################
    @classmethod
    def from_dict(cls: Type[P], mgr: ProfileManager, user: User, data: Dict[str, Any]) -> P:
        
        self: P = cls.__new__(cls)
        
        self._mgr = mgr
        self._user = user
        self._id = mgr.bot.database.insert.profile(mgr.guild_id, user.id)
        
        self._details = ProfileDetails.from_dict(self, data["details"])
        self._aag = ProfileAtAGlance.from_dict(self, data["aag"])
        self._personality = ProfilePersonality.from_dict(self, data["personality"])
        self._images = ProfileImages.from_dict(self, data["images"])
        
        return self
    
################################################################################
    @property
    def bot(self) -> FroggeBot:
        
        return self._mgr.bot
    
################################################################################    
    @property
    def manager(self) -> ProfileManager:
        
        return self._mgr
    
################################################################################
    @property
    def id(self) -> str:
        
        return self._id
    
################################################################################
    @property
    def user(self) -> User:
        
        return self._user
    
################################################################################
    @property
    def char_name(self) -> str:
        
        return self._details.name
    
################################################################################
    @property
    def color(self) -> Optional[Colour]:
        
        if self._details.color is not None:
            return self._details.color
        
        return FroggeColor.embed_background()
    
################################################################################
    @property
    def aboutme(self) -> Optional[str]:
        
        return self._personality.aboutme
    
################################################################################
    async def set_details(self, interaction: Interaction) -> None:
        
        await self._details.menu(interaction)
        
################################################################################
    async def set_ataglance(self, interaction: Interaction) -> None:
        
        await self._aag.menu(interaction)
        
################################################################################
    async def set_personality(self, interaction: Interaction) -> None:
        
        await self._personality.menu(interaction)
        
################################################################################
    async def set_images(self, interaction: Interaction) -> None:
        
        await self._images.menu(interaction)
        
################################################################################
    async def assign_image(self, interaction: Interaction, img_type: ImageType, file: Attachment) -> None:
        
        if img_type is ImageType.AdditionalImage and len(self._images.additional) >= 10:
            error = TooManyImagesError()
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        if img_type is ImageType.AdditionalImage:
            modal = AdditionalImageCaptionModal()

            await interaction.response.send_modal(modal)
            await modal.wait()
    
            if not modal.complete:
                return

            image_url = await self.bot.dump_image(file)
            self._images.add_additional(image_url, modal.value)
            return
        
        await interaction.response.defer()
        image_url = await self.bot.dump_image(file)
        
        if img_type is ImageType.Thumbnail:
            self._images.set_thumbnail(image_url)
        else:
            self._images.set_main_image(image_url)
        
        confirm = U.make_embed(
            color=self.color,
            title="Image Assigned",
            description=(
                f"{img_type.proper_name} has been assigned to your profile.\n"
                "Run the `/profile images` command to view the changes!"
            )
        )
        
        await interaction.respond(embed=confirm, ephemeral=True)
    
################################################################################
    async def progress(self, interaction: Interaction) -> None:

        em_final = self._details.progress_emoji(self._details._post_url)
        value = (
            self._details.progress() +
            self._aag.progress() +
            self._personality.progress() +
            self._images.progress() +
            f"{U.draw_line(extra=15)}\n"
            f"{em_final} -- Finalize"
        )

        progress = U.make_embed(
            color=self.color,
            title="Profile Progress",
            description=value,
            timestamp=False
        )
        view = CloseMessageView(interaction.user)

        await interaction.response.send_message(embed=progress, view=view)
        await view.wait()

################################################################################
    async def post(self, interaction: Interaction, channel: TextChannel) -> None:

        if self.char_name is None:
            error = CharNameNotSetError()
            await interaction.response.send_message(embed=error, ephemeral=True)
            return

        main_profile, aboutme = self.compile()

        if len(main_profile) > 5999:
            error = ExceedsMaxLengthError(len(main_profile))
            await interaction.response.send_message(embed=error, ephemeral=True)
            return

        embeds = [main_profile]
        if aboutme is not None:
            embeds.append(aboutme)

        profile_msg = await self.fetch_post_message(interaction.client)  # type: ignore
        if profile_msg is not None:
            try:
                await profile_msg.edit(embeds=embeds)
            except NotFound:
                self._details.post_url = None

            await interaction.respond(embed=self.success_message())
            return

        if not isinstance(channel, TextChannel):
            error = ChannelTypeError(channel, "TextChannel")
            await interaction.respond(embed=error, ephemeral=True)
            return

        try:
            post_msg = await channel.send(embeds=embeds)
        except Forbidden:
            error = InsufficientPermissionsError(channel, "Send Messages")
            await interaction.respond(embed=error, ephemeral=True)
            return
        else:
            self._details.post_url = post_msg.jump_url

        await interaction.respond(embed=self.success_message())

        return

################################################################################
    def compile(self) -> Tuple[Embed, Optional[Embed]]:

        char_name, url, color, jobs, rates_field = self._details.compile()
        ataglance = self._aag.compile()
        likes, dislikes, personality, aboutme = self._personality.compile()
        thumbnail, main_image, additional_imgs = self._images.compile()

        if char_name is None:
            char_name = f"Character Name: {str(NS)}"
        elif url is not None:
            char_name = f"{BotEmojis.Envelope}  {char_name}  {BotEmojis.Envelope}"

        description = "** **"
        if jobs is not None:
            description = (
                f"{U.draw_line(text=jobs)}\n"
                f"{jobs}\n"
                f"{U.draw_line(text=jobs)}"
            )

        fields: List[EmbedField] = []
        if ataglance is not None:
            fields.append(ataglance)
        if rates_field is not None:
            fields.append(rates_field)
        if likes is not None:
            fields.append(likes)
        if dislikes is not None:
            fields.append(dislikes)
        if personality is not None:
            fields.append(personality)
        if additional_imgs is not None:
            additional_imgs.value += U.draw_line(extra=14)
            fields.append(additional_imgs)

        main_profile = U.make_embed(
            color=color,
            title=char_name,
            description=description,
            url=url,
            thumbnail_url=thumbnail,
            image_url=main_image,
            fields=fields
        )

        return main_profile, aboutme
    
################################################################################
    async def fetch_post_message(self, client: FroggeBot) -> Optional[Message]:

        post_url = self._details.post_url
        if post_url is None:
            return

        parts = post_url.split("/")
        channel_id = int(parts[5])
        msg_id = int(parts[6])

        profile_msg = None
        try:
            channel = await client.fetch_channel(channel_id)
        except:
            return
        else:
            try:
                profile_msg = await channel.fetch_message(msg_id)
            except:
                self._details.post_url = None

        return profile_msg

################################################################################
    def success_message(self) -> Embed:

        return U.make_embed(
            color=Colour.brand_green(),
            title="Profile Posted!",
            description=(
                "Hey, good job, you did it! Your profile was posted successfully!\n"
                f"{U.draw_line(extra=37)}\n"
                f"(__Character Name:__ ***{self.char_name}***)\n\n"

                f"{BotEmojis.ArrowRight}  [Check It Out HERE!]"
                f"({self._details.post_url})  {BotEmojis.ArrowLeft}\n"
                f"{U.draw_line(extra=16)}"
            ),
            thumbnail_url=BotImages.ThumbsUpFrog,
            footer_text="By Allegro#6969",
            footer_icon=BotImages.ThumbsUpFrog,
            timestamp=True
        )

################################################################################
    async def preview(self, interaction: Interaction) -> None:

        prompt = U.make_embed(
            color=self.color,
            title="Preview Profile",
            description=(
                "Select the button below corresponding to the section\n"
                "of your profile you would like to preview."
            ),
            timestamp=False
        )
        view = ProfilePreView(interaction.user, self)

        await interaction.response.send_message(embed=prompt, view=view)
        await view.wait()

        return
        
################################################################################
    async def export(self, interaction: Interaction) -> None:
        
        prompt = U.make_embed(
            color=self.color,
            title="Export Profile",
            description=(
                "Clicking the button below will export your profile to a file.\n\n"
                
                "To import this profile into another server, use the `/profile import` "
                "command and provide it the file you receive."
            )
        
        )
        view = ConfirmCancelView(interaction.user)
        
        await interaction.respond(embed=prompt, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return

        with open("profile.json", "w") as fp:
            json.dump(self._to_dict(), fp)
            
        file = File("profile.json")
        confirm = U.make_embed(
            color=self.color,
            title="Profile Exported",
            description=(
                "Your profile has been exported to the file above.\n"
                "You can now download it and import it into another\n"
                "server using the `/profile import` command!"
            )
        )
        
        await interaction.respond(embed=confirm, file=file)
    
################################################################################
    def _to_dict(self) -> Dict[str, Any]:
        
        return {
            "guild_id": self._mgr.guild_id,
            "details": self._details._to_dict(),
            "aag": self._aag._to_dict(),
            "personality": self._personality._to_dict(),
            "images": self._images._to_dict()
        }
    
################################################################################
    def update_all(self) -> None:
        
        self._details.update()
        self._aag.update()
        self._personality.update()
        self._images.update()
        
################################################################################
