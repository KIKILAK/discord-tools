import requests
import os
import discord
from discord.ext import commands
import aiohttp
import asyncio

title = r"""
░  ░░░░  ░░        ░░       ░░░  ░░░░  ░░░      ░░░░      ░░░  ░░░░  ░░░      ░░
▒  ▒  ▒  ▒▒  ▒▒▒▒▒▒▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒  ▒▒  ▒▒▒  ▒▒▒  ▒▒▒▒▒▒▒
▓        ▓▓      ▓▓▓▓       ▓▓▓        ▓▓  ▓▓▓▓  ▓▓  ▓▓▓▓  ▓▓     ▓▓▓▓▓▓      ▓▓
█   ██   ██  ████████  ████  ██  ████  ██  ████  ██  ████  ██  ███  █████████  █
█  ████  ██        ██       ███  ████  ███      ████      ███  ████  ███      ██
"""
print(title)

# Configura los intents del bot
intents = discord.Intents.default()
intents.guilds = True  # Permite recibir eventos de guilds
intents.messages = True  # Permite recibir eventos de mensajes
intents.webhooks = True  # Permite recibir eventos de webhooks

# Inicializa el bot de Discord
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print("\n")
    print(f'[⤓] Bot {bot.user} connected')
    print("\n")
    await mostrar_menu()  # Muestra el menú después de que el bot esté conectado

async def mostrar_menu():
    # Ejecuta el menú
    while True:
        print("-----------------(menu)-----------------")
        print("\n")
        print("1.- Normal Webhook spam")
        print("2.- Discord Bot Webhook Sender")
        print("\n")
        
        opcion = input("[+] Selecciona una opción (1 o 2): ")

        if opcion == "1":
            await send_webhooks_1()  # Cambiado a await
        elif opcion == "2":
            await enviar_webhooks_discord()  # Cambiado a await
        else:
            print("[x] Opción no válida. Por favor, selecciona 1 o 2.")

async def send_webhooks_1():
    webhook_url = input("--------(-💀-)[BlackCord]/[#Paste webhook URL] $ ")
    message_to_spam_wbh = input("--------(-💀-)[BlackCord]/[#Message to send] $ ")
    count_of_msgs_to_send_wbh = int(input("--------(-💀-)[BlackCord]/[#Amount of messages] $ "))

    for i in range(count_of_msgs_to_send_wbh):
        data = {
            "content": message_to_spam_wbh
        }
        response = requests.post(webhook_url, json=data)

        if response.status_code == 204:
            print(f"[+] Webhook {i + 1} enviado con éxito\n")
            print("\n")
        else:
            print(f"[!] error al enviar el webhook {i + 1} Codigo de estado: {response.status_code}\n")
            print("\n")

async def enviar_webhooks_discord():
    token = input("[*] Introduce el token de tu bot: ")
    server_id = int(input("[*] Introduce el ID del servidor: "))
    message_content = input("[*] Introduce el mensaje que deseas enviar: ")
    cantidad = int(input("[*] Cuántas veces deseas enviar el mensaje?: "))

    # Crea una sesión de cliente HTTP
    async with aiohttp.ClientSession() as session:
        # Obtiene el servidor
        guild = bot.get_guild(server_id)
        if guild is None:
            print("[?] No se pudo encontrar el servidor. Asegúrate de que el ID sea correcto y que el bot esté en el servidor.")
            return

        # Lista para almacenar las tareas
        tasks = []

        # Recorre todos los canales y busca webhooks
        for channel in guild.text_channels:
            try:
                webhooks = await channel.webhooks()
                for webhook in webhooks:
                    # Crea una tarea para enviar el mensaje
                    for _ in range(cantidad):
                        tasks.append(send_message(webhook, message_content))

            except Exception as e:
                print(f"[!] No se pudo enviar el mensaje a {channel.name}: {e}")

        # Espera a que todas las tareas se completen
        await asyncio.gather(*tasks)

async def send_message(webhook, message_content):
    try:
        await webhook.send(message_content)
        print(f"[+] Mensaje enviado a {webhook.name}.")
    except Exception as e:
        print(f"[!] No se pudo enviar el mensaje a {webhook.name}: {e}")

# Ejecuta el bot
if __name__ == "__main__":
    # Utiliza asyncio.run para ejecutar el bot
    asyncio.run(bot.start('MTI5OTQxNjA0ODk0NDE1Njc1Mg.GB0AAL.iK5ndimNjqkJnHw979el9hLy0tO_tvCKuDAEiw'))  # Tu token de bot
