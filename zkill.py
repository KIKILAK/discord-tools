import discord
import os
import asyncio
import datetime
title = r"""

   .-') _ .-. .-')                               
  (  OO) )\  ( OO )                              
,(_)----. ,--. ,--.  ,-.-')  ,--.      ,--.      
|       | |  .'   /  |  |OO) |  |.-')  |  |.-')  
'--.   /  |      /,  |  |  \ |  | OO ) |  | OO ) 
(_/   /   |     ' _) |  |(_/ |  |`-' | |  |`-' | 
 /   /___ |  .   \  ,|  |_.'(|  '---.'(|  '---.' 
|        ||  |\   \(_|  |    |      |  |      |  
`--------'`--' '--'  `--'    `------'  `------'  

"""
print(title)
print("-" * 50)
print("#ospygang #nuker #ospy")
print("-" * 50)
# Verificar si el archivo tokens.txt existe en el directorio
if not os.path.isfile('tokens.txt'):
    print("El archivo 'tokens.txt' no se encontró en el directorio actual.")
    exit()

# Leer los tokens del archivo tokens.txt
with open('tokens.txt', 'r') as file:
    tokens = [line.strip() for line in file if line.strip()]

if not tokens:
    print("No se encontraron tokens válidos en el archivo 'tokens.txt'.")
    exit()

# Solicitar el enlace de invitación, el mensaje a enviar, el ID del canal y la cantidad de veces a enviar el mensaje
invite_link = input("Ingresa el enlace de invitación del servidor: ")
message_to_send = input("Ingresa el mensaje que el bot enviará al unirse: ")
channel_id = int(input("Ingresa el ID del canal donde se enviará el mensaje: "))
repeat_count = int(input("Ingresa la cantidad de veces que se enviará el mensaje: "))

# Definir una función para conectar cada bot y enviar el mensaje
async def connect_and_send_messages(token):
    intents = discord.Intents.default()
    intents.guilds = True
    intents.guild_messages = True

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print("\n")
        print(f'[+] Bot conectado como {client.user}')
        print(f'[+] Puedes unirte al servidor utilizando el enlace: {invite_link}')
        print("\n")

        # Obtener el canal por su ID y enviar el mensaje la cantidad de veces especificada
        channel = client.get_channel(channel_id)
        if channel is not None:
            try:
                for i in range(1, repeat_count + 1):
                    await channel.send(message_to_send)
                    print(f'[+] Mensaje {i} enviado en el canal: {channel.name}')
                    os.system("color 0a")
                print(f'[+] Se enviaron un total de {repeat_count} mensajes en el canal: {channel.name}')
            except discord.Forbidden:
                print(f'[x] No se pudo enviar el mensaje en el canal: {channel.name}. Permisos insuficientes.')
            except Exception as e:
                print(f'[!] Error al enviar el mensaje: {e}')
                os.system("color 0c")
        else:
            print("[?] El canal con el ID especificado no se encontró. Verifica el ID.")
        
        # Cerrar el cliente después de enviar los mensajes
        await client.close()

    # Ejecutar el cliente de Discord con el token proporcionado
    await client.start(token)

# Función principal para ejecutar cada bot
async def main():
    tasks = []
    for token in tokens:
        tasks.append(connect_and_send_messages(token))
    await asyncio.gather(*tasks)

# Ejecutar la función principal
asyncio.run(main())
