from __future__ import annotations

from .Branch import DBWorkerBranch
################################################################################

__all__ = ("DatabaseBuilder",)

################################################################################
class DatabaseBuilder(DBWorkerBranch):
    """A utility class for building and asserting elements of the database."""

    def build_all(self) -> None:

        self._build_bot_tables()
        self._build_profile_tables()
        self._build_initial_records()
        
        print("Database lookin' good!")
        
################################################################################
    def _build_bot_tables(self) -> None:
        
        self.execute(
            "CREATE TABLE IF NOT EXISTS bot_config ("
            "guild_id BIGINT PRIMARY KEY,"
            "log_channel BIGINT,"
            "signup_msg_channel BIGINT,"
            "signup_msg_id BIGINT"
            ");"
        )
        
################################################################################        
    def _build_initial_records(self) -> None:

        for guild in self.bot.guilds:
            self.execute(
                "INSERT INTO bot_config (guild_id) VALUES (%s) "
                "ON CONFLICT DO NOTHING;",
                guild.id,
            )
        
################################################################################
    def _build_profile_tables(self) -> None:
        
        self.execute(
            "CREATE TABLE IF NOT EXISTS profiles ("
            "_id TEXT PRIMARY KEY,"
            "guild_id BIGINT,"
            "user_id BIGINT"
            ");"
        )
        self.execute(
            "CREATE TABLE IF NOT EXISTS details ("
            "_id TEXT PRIMARY KEY,"
            "char_name TEXT,"
            "url TEXT,"
            "color INTEGER,"
            "jobs TEXT[],"
            "rates TEXT,"
            "post_url TEXT"
            ");"
        )
        self.execute(
            "CREATE TABLE IF NOT EXISTS ataglance ("
            "_id TEXT PRIMARY KEY,"
            "gender TEXT,"
            "pronouns INTEGER[],"
            "race TEXT,"
            "clan TEXT,"
            "orientation TEXT,"
            "height INTEGER,"
            "age TEXT,"
            "mare TEXT"
            ");"
        )
        self.execute(
            "CREATE TABLE IF NOT EXISTS personality ("
            "_id TEXT PRIMARY KEY,"
            "likes TEXT[],"
            "dislikes TEXT[],"
            "personality TEXT,"
            "aboutme TEXT"
            ");"
        )
        self.execute(
            "CREATE TABLE IF NOT EXISTS images ("
            "_id TEXT PRIMARY KEY,"
            "thumbnail TEXT,"
            "main_image TEXT"
            ");"
        )
        self.execute(
            "CREATE TABLE IF NOT EXISTS additional_images ("
            "_id TEXT PRIMARY KEY,"
            "profile_id TEXT,"
            "url TEXT,"
            "caption TEXT"
            ");"
        )
        
        self._refresh_profile_view()
    
################################################################################
    def _refresh_profile_view(self) -> None:

        self.execute(
            "CREATE OR REPLACE VIEW profile_master "
            "AS "
            # Data indices 0 - 2 Internal
            "SELECT p._id,"
            "p.user_id,"
            "p.guild_id,"
            # Data indices 3 - 8 Details
            "d.char_name,"
            "d.url AS custom_url,"
            "d.color,"
            "d.jobs,"
            "d.rates,"
            "d.post_url,"
            # Data indices 9 - 12 Personality
            "pr.likes,"
            "pr.dislikes,"
            "pr.personality,"
            "pr.aboutme,"
            # Data indices 13 - 20 At A Glance
            "a.gender,"
            "a.pronouns,"
            "a.race,"
            "a.clan,"
            "a.orientation,"
            "a.height,"
            "a.age,"
            "a.mare,"
            # Data indices 21 - 22 Images
            "i.thumbnail,"
            "i.main_image "
            "FROM profiles p "
            "JOIN details d ON p._id = d._id "
            "JOIN personality pr ON p._id = pr._id "
            "JOIN ataglance a on p._id = a._id "
            "JOIN images i on p._id = i._id;"
        )
        
################################################################################
