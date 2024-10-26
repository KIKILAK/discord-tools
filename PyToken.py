import base64
import os

os.system("color 0c")

title = r"""

___________     __                   _________      .__                     
\__    ___/___ |  | __ ____   ____  /   _____/ ____ |__|_____   ___________ 
  |    | /  _ \|  |/ // __ \ /    \ \_____  \ /    \|  \____ \_/ __ \_  __ \
  |    |(  <_> )    <\  ___/|   |  \/        \   |  \  |  |_> >  ___/|  | \/
  |____| \____/|__|_ \\___  >___|  /_______  /___|  /__|   __/ \___  >__|   
                    \/    \/     \/        \/     \/   |__|        \/       

"""
print(title)
print("\n")
UserID = input("--------(-💀-)[BlackCord]/[#Enter the user ID] $ ")
b = base64.b64encode(bytes(UserID, 'utf-8')) # bytes
base64_str = b.decode('utf-8') # convert bytes to string

print("User Token First Part:" + base64_str)