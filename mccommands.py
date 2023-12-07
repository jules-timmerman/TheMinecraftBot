import datetime
import setup
import discord
from discord.ext import commands
from discord import  app_commands
from CodeUtils import embeds
import json
import mcrcon

bot_owner_id = None
server_ip = None
server_rcon_port = None
server_rcon_password = None
bot_name = None

def config_reload():
    global server_ip, server_rcon_port, server_rcon_password, bot_name, bot_owner_id
    with open('config.json', 'r') as config:
        config = json.load(config)
    bot_owner_id = int(config["bot_owner_id"])
    server_ip = config["server_ip"]
    server_rcon_port = config["server_rcon_port"]
    server_rcon_password = config["server_rcon_password"]
    bot_name = config["bot_name"]

class mccommands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    config_reload()

    @app_commands.command(name="mc-setname",description="this command connects your Minecraft account to your Discord account")
    async def mcsetname(self, interaction: discord.Interaction, mcname: str):
        config_reload()
        try:
            await add_to_whitelist(mcname)
            print(f"|🖥|{datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S')}| - added {mcname} to whitelist")
            await interaction.response.send_message(embed=embeds.MCWhitelistaddEmbed())
        except Exception as e:
            await interaction.response.send_message(embed=embeds.MCError())
            print(f"|❌|{datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S')}| - {e}")

    @app_commands.command(name="mc-help", description="this will return some help hopefully.")
    async def mchelp(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed=embeds.Help(), view = HelpView())


async def add_to_whitelist(minecraft_name):
    config_reload()
    rcon = mcrcon.MCRcon(host=str(server_ip), password=str(server_rcon_password), port=int(server_rcon_port))
    rcon.connect()
    rcon.command(f'whitelist add {minecraft_name}')
    rcon.disconnect()



class HelpView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(HelpGithubButton("GitHub",discord.ButtonStyle.url,None, "https://4bones.de"))
        self.add_item(HelpGithubButton("Wiki", discord.ButtonStyle.url, None, "https://github.com/fourbones/TheMinecraftBot/wiki"))
        self.add_item(HelpGithubButton("Setup", discord.ButtonStyle.green, "⚙️", None))

class HelpGithubButton(discord.ui.Button):
    def __init__(self, Buttonname, Buttonstyle, emoji, url):
        super().__init__(label=Buttonname, style=Buttonstyle, emoji=emoji, url=url)
        self.Name = Buttonname

    async def callback(self, interaction: discord.Interaction):
        config_reload()
        if self.Name == "Setup" and int(interaction.user.id) == int(bot_owner_id):
            await interaction.response.send_modal(setup.SetupModal())
        else:
            await interaction.response.send_message(embed=embeds.NotOwner())
