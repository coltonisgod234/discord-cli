import cli.main
import asyncio
from argparse import Namespace  # Nothing else

current_guild = 1257780211525877820 # test ID
current_channel = 1257780211525877823  # test ID

print("[ Establish connection to discord [.....]")
discord = asyncio.get_event_loop().run_until_complete(cli.main.connect_to_discord())

async def loop():
    #framebuffer = []
    async for msg in cli.main.message.stream_all_messages_in_current_ch(discord, True):
        #framebuffer += str(msg)
        print(msg)
    
    #print("".join(framebuffer))
    await asyncio.sleep(0.1)
    print("\x1b[H")  # clear screen and move cursor home
    #print("\x1b[2J")

async def main():
    await cli.main.switch(Namespace(
        gi=current_guild,
        ci=current_channel,
    ), discord)
    while True:
        await loop()


asyncio.get_event_loop().run_until_complete(main())