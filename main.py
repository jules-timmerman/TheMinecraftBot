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



bot.run(str(bot_token))
