import discord
import asyncio
import aiohttp
from discord.ext import commands
import public_ip as ip

title = r"""

__________                     .___         __   .__.__  .__                
\____    /____  ___________  __| _/        |  | _|__|  | |  |   ___________ 
  /     // ___\/  _ \_  __ \/ __ |  ______ |  |/ /  |  | |  | _/ __ \_  __ \
 /     /\  \__(  <_> )  | \/ /_/ | /_____/ |    <|  |  |_|  |_\  ___/|  | \/
/_______ \___  >____/|__|  \____ |         |__|_ \__|____/____/\___  >__|   
        \/   \/                 \/              \/                 \/       

"""
print(title)
print("-" * 50)
print("IP: " + ip.get() + " " +  "Welcome. AJ")
print("-" * 50)
print("\n")

# Función para solicitar el token y el ID del servidor al usuario
def get_credentials():
    token = input("Please enter your bot token: ")
    guild_id = input("Please enter the server (guild) ID :")
    print("\n")
    return token, int(guild_id)

# Obtener token y ID del servidor
bot_token, server_id = get_credentials()

# Configuración del bot con el prefijo de comando '!'
intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.members = True  # Permite acceder a la información de los miembros
intents.emojis = True  # Permite acceder a la gestión de emojis
bot = commands.Bot(command_prefix='!', intents=intents)

# Evento cuando el bot esté listo
@bot.event
async def on_ready():
    print(f'\n[+] Logged in as {bot.user.name}')
    guild = bot.get_guild(server_id)
    if guild:
        print(f'[+] Connected to server: {guild.name} (ID: {guild.id})\n')
        show_menu(guild)
    else:
        print(f'[?] Could not find a server with ID: {server_id}')

# Función para mostrar el menú
def show_menu(guild):
    while True:
        print("\n--- Discord Bot Menu ---")
        print("1. Change Server Name")
        print("2. Check Bot Permissions")
        print("3. Create Channels")
        print("4. Send Custom Message in Existing Channels")
        print("5. Delete All Channels")
        print("6. Change Server Picture")
        print("7. Create Roles")
        print("8. Change Nicknames of All Members")
        print("9. Change Names of All Roles and Channels")
        print("10. Kick All Bots from the Server")
        print("11. Create Emojis from Image URL")
        print("12. Delete All Emojis")
        print("13. Create Webhooks")
        print("14. Exit")
        choice = input("Please choose an option (1-14): ")

        if choice == '1':
            new_name = input("Enter the new server name: ")
            bot.loop.create_task(change_server_name(guild, new_name))
        elif choice == '2':
            bot.loop.create_task(check_permissions(guild))
        elif choice == '3':
            channel_name_base = input("Enter the base name for the channels or leave blank if using custom names: ")
            channel_count = int(input("How many channels do you want to create? "))
            custom_names = input("Do you want to use custom names for the channels? (yes/no): ").lower() == 'yes'
            channel_names = []
            
            if custom_names:
                print(f"Please enter {channel_count} names separated by commas:")
                channel_names = input("Names: ").split(',')
                if len(channel_names) != channel_count:
                    print("[!] The number of names provided does not match the number of channels to create.")
                    continue

            delay_seconds = float(input("Enter delay in seconds between each channel creation: "))
            send_message = input("Do you want to send a message in the new channels? (yes/no): ").lower() == 'yes'
            message_content = ""
            if send_message:
                message_content = input("Enter the message to send: ")
            
            bot.loop.create_task(create_channels(guild, channel_name_base, channel_count, channel_names, delay_seconds, send_message, message_content))
        elif choice == '4':
            message_content = input("Enter the custom message to send: ")
            times_to_send = int(input("How many times to send the message in each channel? "))
            bot.loop.create_task(send_message_in_existing_channels(guild, message_content, times_to_send))
        elif choice == '5':
            confirmation = input("Are you sure you want to delete all channels? Type 'yes' to confirm: ")
            if confirmation.lower() == 'yes':
                bot.loop.create_task(delete_all_channels(guild))
            else:
                print("[x] Deletion canceled.")
        elif choice == '6':
            image_url = input("Enter the URL of the new server picture: ")
            bot.loop.create_task(change_server_picture(guild, image_url))
        elif choice == '7':
            role_count = int(input("How many roles do you want to create? "))
            custom_names = input("Do you want to provide custom names for each role? (yes/no): ").lower() == 'yes'
            role_names = []
            
            if custom_names:
                print(f"Please enter {role_count} names separated by commas:")
                role_names = input("Names: ").split(',')
                if len(role_names) != role_count:
                    print("[!] The number of names provided does not match the number of roles to create.")
                    continue
            
            bot.loop.create_task(create_roles(guild, role_count, role_names))
        elif choice == '8':
            new_nickname = input("Enter the new nickname for all members: ")
            bot.loop.create_task(change_all_nicknames(guild, new_nickname))
        elif choice == '9':
            new_name = input("Enter the new name for all roles and channels: ")
            bot.loop.create_task(change_all_roles_and_channels(guild, new_name))
        elif choice == '10':
            confirmation = input("Are you sure you want to kick all bots from the server? Type 'yes' to confirm: ")
            if confirmation.lower() == 'yes':
                bot.loop.create_task(kick_all_bots(guild))
            else:
                print("[x] Kicking bots canceled.")
        elif choice == '11':
            image_url = input("Enter the URL of the image to create emojis: ")
            bot.loop.create_task(create_emojis_from_image(guild, image_url))
        elif choice == '12':
            confirmation = input("Are you sure you want to delete all emojis? Type 'yes' to confirm: ")
            if confirmation.lower() == 'yes':
                bot.loop.create_task(delete_all_emojis(guild))
            else:
                print("[x] Deletion of emojis canceled.")
        elif choice == '13':
            webhook_name = input("Enter the name for the webhooks: ")
            webhook_count = int(input("How many webhooks do you want to create? "))
            message_content = input("Enter the message to send with each webhook: ")
            times_to_send = int(input("How many times to send the message with each webhook? "))
            bot.loop.create_task(create_webhooks(guild, webhook_name, webhook_count, message_content, times_to_send))
        elif choice == '14':
            print("[completed] Exiting the menu.")
            break
        else:
            print("[!] Invalid option, please try again.")

# Función para crear múltiples webhooks
async def create_webhooks(guild, webhook_name, webhook_count, message_content, times_to_send):
    try:
        for channel in guild.text_channels:
            for _ in range(webhook_count):
                webhook = await channel.create_webhook(name=webhook_name)
                print(f'[+] Webhook \'{webhook.name}\' created in channel \'{channel.name}\'.')

                for _ in range(times_to_send):
                    await webhook.send(message_content)
                    print(f'[+] Message sent through webhook \'{webhook.name}\' in channel \'{channel.name}\'.')
                    await asyncio.sleep(1)  # Pausa de 1 segundo entre mensajes

    except discord.Forbidden:
        print("[x] Bot lacks permission to create webhooks or send messages through them.")
    except Exception as e:
        print(f"[x] An error occurred: {e}")

# Función para cambiar el nombre del servidor
async def change_server_name(guild, new_name):
    try:
        await guild.edit(name=new_name)
        print(f'[+] Server name changed to: {new_name}')
    except discord.Forbidden:
        print("[x] Bot lacks permission to change the server name.")
    except Exception as e:
        print(f"[x] An error occurred: {e}")

# Función para chequear los permisos del bot
async def check_permissions(guild):
    bot_member = guild.me
    permissions = bot_member.guild_permissions
    permission_list = [
        ("Administrator", permissions.administrator),
        ("Manage Server", permissions.manage_guild),
        ("Manage Channels", permissions.manage_channels),
        ("Send Messages", permissions.send_messages),
        ("Read Message History", permissions.read_message_history),
        ("Manage Roles", permissions.manage_roles),
        ("Manage Emojis", permissions.manage_emojis)
    ]

    print("\n--- Bot Permissions ---")
    for perm, has_permission in permission_list:
        print(f"{perm}: {'[+] Yes' if has_permission else '[x] No'}")

# Función para crear múltiples canales en el servidor y enviar un mensaje si es necesario
async def create_channels(guild, channel_name_base, channel_count, channel_names, delay_seconds, send_message, message_content):
    try:
        for i in range(channel_count):
            channel_name = channel_names[i] if channel_names else f"{channel_name_base}-{i + 1}"
            new_channel = await guild.create_text_channel(name=channel_name)
            print(f'[+] Channel \'{channel_name}\' created successfully.')
            
            if send_message and message_content:
                await new_channel.send(message_content)
                print(f'[+] Message sent in channel \'{channel_name}\'.')
            await asyncio.sleep(delay_seconds)
        
        print('[completed] Channel creation process finished.')
    except discord.Forbidden:
        print("[x] Bot lacks permission to create channels or send messages in them.")
    except Exception as e:
        print(f"[x] An error occurred: {e}")

# Función para enviar un mensaje en canales existentes
async def send_message_in_existing_channels(guild, message_content, times_to_send):
    for channel in guild.text_channels:
        for _ in range(times_to_send):
            await channel.send(message_content)
            print(f'[+] Message sent in channel \'{channel.name}\'.')
            await asyncio.sleep(1)  # Pause of 1 second between messages

# Función para eliminar todos los canales en el servidor
async def delete_all_channels(guild):
    try:
        for channel in guild.text_channels:
            await channel.delete()
            print(f'[+] Channel \'{channel.name}\' deleted successfully.')
        
        print('[completed] All channels have been deleted.')
    except discord.Forbidden:
        print("[x] Bot lacks permission to delete channels.")
    except Exception as e:
        print(f"[x] An error occurred: {e}")

# Función para cambiar la imagen del servidor
async def change_server_picture(guild, image_url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as response:
                if response.status == 200:
                    image_data = await response.read()
                    await guild.edit(icon=image_data)
                    print('[+] Server picture changed successfully.')
                else:
                    print(f'[x] Failed to download image: {response.status}')
    except discord.Forbidden:
        print("[x] Bot lacks permission to change the server picture.")
    except Exception as e:
        print(f"[x] An error occurred: {e}")

# Función para crear múltiples roles en el servidor
async def create_roles(guild, role_count, role_names):
    try:
        for i in range(role_count):
            role_name = role_names[i] if role_names else f"Role-{i + 1}"
            role = await guild.create_role(name=role_name)
            print(f'[+] Role \'{role.name}\' created successfully.')
        
        print('[completed] Role creation process finished.')
    except discord.Forbidden:
        print("[x] Bot lacks permission to create roles.")
    except Exception as e:
        print(f"[x] An error occurred: {e}")

# Función para cambiar el apodo de todos los miembros en el servidor
async def change_all_nicknames(guild, new_nickname):
    try:
        for member in guild.members:
            await member.edit(nick=new_nickname)
            print(f'[+] Nickname of member \'{member.name}\' changed successfully.')
        
        print('[completed] All nicknames have been changed.')
    except discord.Forbidden:
        print("[x] Bot lacks permission to change nicknames.")
    except Exception as e:
        print(f"[x] An error occurred: {e}")

# Función para cambiar los nombres de todos los roles y canales en el servidor
async def change_all_roles_and_channels(guild, new_name):
    try:
        # Cambiar los nombres de los roles
        for role in guild.roles:
            await role.edit(name=new_name)
            print(f'[+] Role \'{role.name}\' changed successfully.')
        
        # Cambiar los nombres de los canales
        for channel in guild.text_channels:
            await channel.edit(name=new_name)
            print(f'[+] Channel \'{channel.name}\' changed successfully.')
        
        print('[completed] All roles and channels have been renamed.')
    except discord.Forbidden:
        print("[x] Bot lacks permission to change names of roles or channels.")
    except Exception as e:
        print(f"[x] An error occurred: {e}")

# Función para expulsar todos los bots del servidor
async def kick_all_bots(guild):
    try:
        for member in guild.members:
            if member.bot:
                await member.kick()
                print(f'[+] Bot \'{member.name}\' has been kicked from the server.')
        
        print('[completed] All bots have been kicked from the server.')
    except discord.Forbidden:
        print("[x] Bot lacks permission to kick members.")
    except Exception as e:
        print(f"[x] An error occurred: {e}")

# Función para crear emojis desde una URL de imagen
async def create_emojis_from_image(guild, image_url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as response:
                if response.status == 200:
                    image_data = await response.read()
                    emoji = await guild.create_custom_emoji(name="NewEmoji", image=image_data)
                    print(f'[+] Emoji \'{emoji.name}\' created successfully.')
                else:
                    print(f'[x] Failed to download image for emoji: {response.status}')
    except discord.Forbidden:
        print("[x] Bot lacks permission to create emojis.")
    except Exception as e:
        print(f"[x] An error occurred: {e}")

# Función para eliminar todos los emojis del servidor
async def delete_all_emojis(guild):
    try:
        for emoji in guild.emojis:
            await emoji.delete()
            print(f'[+] Emoji \'{emoji.name}\' deleted successfully.')
        
        print('[completed] All emojis have been deleted.')
    except discord.Forbidden:
        print("[x] Bot lacks permission to delete emojis.")
    except Exception as e:
        print(f"[x] An error occurred: {e}")

# Iniciar el bot
bot.run(bot_token)
