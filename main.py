import asyncio
from pyppeteer import connect
import nav
import message
import vc
import argparse

parser = argparse.ArgumentParser("dterm")
parser.add_argument("command")
parser.add_argument("--text")
parser.add_argument("--private", action="store_true")

# By name
parser.add_argument("-cn")
parser.add_argument("-gn")
parser.add_argument("-un")

# By ID
parser.add_argument("-ci")
parser.add_argument("-gi")
parser.add_argument("-ui")

# Stuff
parser.add_argument("--json", action="store_true")
parsed_args = parser.parse_args()

async def command_text(args, discord):
    await message.type_to_message_bar(args.text, discord)

async def command_texts(args, discord):
    out = await message.get_all_messages_in_current_ch(discord)
    for m in out:
        print(m)

async def command_channels(args, discord):
    channels = await nav.get_channels(discord, json=args.json)
    for channel in channels:
        print(channel)

async def command_leavevc(args, discord):
    await vc.leave_vc(discord)

async def switch_guild(args, discord):
    if args.gn:
        await nav.go_to_guild_by_name(args.gn, discord)
    elif args.gi:
        await nav.go_to_guild(args.gi, discord)
    elif args.private:
        await nav.go_to_guild("home", discord)

async def switch_ch(args, discord):
    if args.cn:
        await nav.go_to_channel_by_name(args.cn, discord)
    elif args.ci:
        await nav.go_to_channel(args.ci, discord, args.private)

async def switch(args, discord):
    await switch_guild(args, discord)
    await switch_ch(args, discord)

async def connect_to_discord():
    browser = await connect(browserURL="http://localhost:9222")
    pages = await browser.pages()
    discord = next(p for p in pages if "discord.com" in p.url)
    print(f"[ connected to discord: {discord}\n\n")
    return discord

async def main(args, discord):
    print("[ Get command...")
    if args.command == "text":
        await switch(args, discord)
        await command_text(args, discord)
    elif args.command == "texts":
        await switch(args, discord)
        await command_texts(args, discord)
    elif args.command == "channels":
        await switch(args, discord)
        await command_channels(args, discord)
    elif args.command == "servers":
        await nav.go_to_guild("home", discord)
        await nav.get_servers(discord)
    elif args.command == "switch":
        await switch(args, discord)
    elif args.command == "disconnect":
        await command_leavevc(args, discord)
    elif args.command == "mute":
        await vc.mute(discord)
    elif args.command == "unmute":
        await vc.unmute(discord)
    elif args.command == "deafen":
        await vc.deaf(discord)
    elif args.command == "undeafen":
        await vc.undeaf(discord)
    else:
        print("Unregognized command.")
        quit(1)
    
    print("Ok.")

print("[ Connect to discord...")
discord = asyncio.get_event_loop().run_until_complete(connect_to_discord())
print("[ Start main")
asyncio.get_event_loop().run_until_complete(main(parsed_args, discord))
