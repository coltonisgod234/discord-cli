import asyncio
from pyppeteer import connect
from . import nav
from . import message
from . import vc
import argparse

def apply_safe_defaults(args):
    if not hasattr(args, "private"): args.private = False  # Safe default
    return args

async def command_text(args, discord):
    args = apply_safe_defaults(args)
    return await message.type_to_message_bar(args.text, discord)

async def command_texts(args, discord, enable_print=False):
    args = apply_safe_defaults(args)
    out = await message.get_all_messages_in_current_ch(discord)
    if enable_print:
        for m in out:
            print(m)
    
    return out

async def command_channels(args, discord, enable_print=False):
    args = apply_safe_defaults(args)
    channels = []  # Default value
    if args.private:
        channels = await nav.get_dms(discord, json=args.json)
    else:
        channels = await nav.get_channels(discord, json=args.json)

    if enable_print:
        for channel in channels:
            print(channel)
    
    return 

async def command_leavevc(args, discord):
    args = apply_safe_defaults(args)
    await vc.leave_vc(discord)

async def command_vc(args, discord):
    args = apply_safe_defaults(args)
    if args.private:
        await vc.join_vc_private(discord)
    else:
        print("Command not supported")

async def switch_guild(args, discord):
    args = apply_safe_defaults(args)
    if hasattr(args, "gn"):
        await nav.go_to_guild_by_name(args.gn, discord)
    elif hasattr(args, "gi"):
        await nav.go_to_guild(args.gi, discord)
    elif args.private:
        await nav.go_to_guild("home", discord)

async def switch_ch(args, discord):
    args = apply_safe_defaults(args)
    if hasattr(args, "cn"):
        await nav.go_to_channel_by_name(args.cn, discord)
    elif hasattr(args, "gi"):
        await nav.go_to_channel(args.ci, discord, args.private)

async def switch(args, discord):
    args = apply_safe_defaults(args)
    await switch_guild(args, discord)
    await switch_ch(args, discord)

async def connect_to_discord():
    browser = await connect(browserURL="http://localhost:9222")
    pages = await browser.pages()
    discord = next(p for p in pages if "discord.com" in p.url)
    print(f"[ connected to discord: {discord}\n\n")
    return discord

async def command(args, discord):
    args = apply_safe_defaults(args)
    match args.command:
        case "text":
            await switch(args, discord)
            return await command_text(args, discord)
        case "texts":
            await switch(args, discord)
            return await command_texts(args, discord, enable_print=True)
        case "channels":
            await switch(args, discord)
            return await command_channels(args, discord, enable_print=True)
        case "servers":
            await nav.go_to_guild("home", discord)
            return await nav.get_servers(discord)
        case "switch":
            return await switch(args, discord)
        case "disconnect":
            return await command_leavevc(args, discord)
        case "mute":
            return await vc.mute(discord)
        case "unmute":
            return await vc.unmute(discord)
        case "deafen":
            return await vc.deaf(discord)
        case "undeafen":
            return await vc.undeaf(discord)
        case _:
            print("Unregognized command.")
            quit(2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser("dterm")
    parser.add_argument("command")
    parser.add_argument("-text")
    parser.add_argument("--private", "-pr", action="store_true")

    # By name
    parser.add_argument("-cn")
    parser.add_argument("-gn")
    parser.add_argument("-un")

    # By ID
    parser.add_argument("-ci")
    parser.add_argument("-gi")
    parser.add_argument("-ui")

    # Stuff
    parser.add_argument("--json", "-js", action="store_true")
    parsed_args = parser.parse_args()

    print("[ Connect to discord...")
    discord = asyncio.get_event_loop().run_until_complete(connect_to_discord())
    print("[ Start main")
    asyncio.get_event_loop().run_until_complete(command(parsed_args, discord))
