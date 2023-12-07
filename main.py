import discord, datetime
from discord.ext import commands
from CodeUtils import embeds
import mccommands, setup
import json
import mcrcon

bot_token = None
server_ip = None
server_rcon_port = None
server_rcon_password = None


def config_reload():
    global bot_token, server_ip, server_rcon_port, server_rcon_password
    with open('config.json', 'r') as config:
        config = json.load(config)
    bot_token = str(config["bot_token"])
    server_ip = str(config["server_ip"])
    server_rcon_port = int(config["server_rcon_port"])
    server_rcon_password = str(config["server_rcon_password"])


config_reload()
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    await bot.add_cog(mccommands.mccommands(bot))
    await bot.add_cog(setup.setup(bot))

    print(f'Logged in as {bot.user.name}')
    with open('config.json', 'r') as file:
        config_data = json.load(file)

    config_data['bot_name'] = bot.user.name

    with open('config.json', 'w') as file:
        json.dump(config_data, file, indent=4)

    print(f"|✅|{datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S')}| - All Cogs Loaded")

    await bot.tree.sync()
    print(f"|✅|{datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S')}| - bot.tree synced")





async def remove_from_whitelist(member):
    config_reload()
    data = {}
    try:
        with open('user_data.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        pass

    discord_name = str(member)
    minecraft_name = data[discord_name]["minecraft_name"]

    rcon = mcrcon.MCRcon(host=str(server_ip), password=str(server_rcon_password), port=int(server_rcon_port))
    rcon.connect()
    rcon.command(f'whitelist remove {minecraft_name}')
    rcon.command(f'kick {minecraft_name} Du bist nicht mehr auf der Whitelist!')
    rcon.disconnect()
    print(f"|🖥|{datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S')}| - removed {minecraft_name} from the whitelist")


def is_mcname_permission_allowed(member):
    with open('user_data.json', 'r') as file:
        data = json.load(file)

    discord_name = str(member)
    if discord_name in data:
        return data[discord_name]["permission"]

    return False


async def set_mcname_permission(member, permission):
    with open('user_data.json', 'r+') as file:
        data = json.load(file)

        discord_name = str(member)
        if discord_name not in data:
            data[discord_name] = {"minecraft_name": "", "permission": False}

        data[discord_name]["permission"] = permission

        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()

bot.run(str(bot_token))
