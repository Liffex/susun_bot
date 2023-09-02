import os

import discord
from discord import app_commands
from dotenv import load_dotenv
from mcstatus import JavaServer
from mcstatus.status_response import JavaStatusResponse


def get_server_status(host):
    server = JavaServer.lookup(host)

    try:
        server.status()
        return server.status()
    except (TimeoutError, ConnectionRefusedError):
        return False


class MinecraftClient(discord.Client):
    async def on_ready(self):
        print(f"MinecraftClient is UP as {self.user}")
        await minecraftCommandTree.sync()

    async def on_connect(self):
        print(f"MinecraftClient successfully connected to server")


dotenv_path = os.path.join('.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

server_host = os.getenv("SERVER_HOST")
api_token = os.getenv("APIKEY")

intents = discord.Intents.default()
intents.message_content = True
minecraftClient = MinecraftClient(intents=intents)
minecraftCommandTree = app_commands.CommandTree(minecraftClient)


@minecraftCommandTree.command(name="players", description="Список игроков онлайн")
async def players(interaction: discord.Interaction):
    await interaction.response.defer()

    server_status = get_server_status(server_host)
    if isinstance(server_status, JavaStatusResponse):
        sample = server_status.players.sample
        if sample is None:
            await interaction.followup.send('Сервер пуст')
        else:
            player_list = []
            for player in sample:
                player_list.append(player.name)
            await interaction.followup.send(f"Игроки на сервере: {', '.join(player_list)}")
    else:
        await interaction.followup.send('Сервер оффлайн')


@minecraftCommandTree.command(name="online", description="Количество игроков онлайн")
async def players(interaction: discord.Interaction):
    await interaction.response.defer()

    server_status = get_server_status(server_host)
    if isinstance(server_status, JavaStatusResponse):
        await interaction.followup.send(
            f"Сейчас на сервере {server_status.players.online} из {server_status.players.max} игроков")
    else:
        await interaction.followup.send('Сервер оффлайн(')


@minecraftCommandTree.command(name="server", description="Статус сервера")
async def check_online(interaction: discord.Interaction):
    await interaction.response.defer()

    server_status = get_server_status(server_host)
    if isinstance(server_status, JavaStatusResponse):
        await interaction.followup.send('Сервер онлайн')
    else:
        await interaction.followup.send('Сервер оффлайн')


@minecraftCommandTree.command(name="ip", description="Адрес сервера")
async def ip_command(interaction: discord.Interaction):
    await interaction.response.send_message(f"Подключиться к серверу можно по адресу {server_host}")

minecraftClient.run(api_token)
