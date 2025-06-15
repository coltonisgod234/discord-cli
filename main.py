import asyncio
from pyppeteer import connect
import nav
import message
import argparse

parser = argparse.ArgumentParser("dterm")
parser.add_argument("command")
parser.add_argument("-text")
parser.add_argument("--private", action="store_true")

# By name
parser.add_argument("-cn")
parser.add_argument("-gn")
parser.add_argument("-un")

# By ID
parser.add_argument("-ci")
parser.add_argument("-gi")
parser.add_argument("-ui")
args = parser.parse_args()

async def command_text(args, discord):
    if args.gn:
        await nav.go_to_guild_by_name(args.gn, discord)
    elif args.gi:
        await nav.go_to_guild(args.gi, discord)
    elif args.private:
        await nav.go_to_guild("home", discord)

    if args.cn:
        await nav.go_to_channel_by_name(args.cn, discord)
    elif args.ci:
        await nav.go_to_channel(args.ci, discord, args.private)

    await message.type_to_message_bar(args.text, discord)

async def command_texts(args, discord):
    if args.gn:
        await nav.go_to_guild_by_name(args.gn, discord)
    elif args.gi:
        await nav.go_to_guild(args.gi, discord)
    elif args.private:
        await nav.go_to_guild("home", discord)

    if args.cn:
        await nav.go_to_channel_by_name(args.cn, discord)
    elif args.ci:
        await nav.go_to_channel(args.ci, discord, args.private)

    out = await message.get_all_messages_in_current_ch(discord)
    for m in out:
        print(m)

async def command_channels(args, discord):
    if args.gn:
        await nav.go_to_guild_by_name(args.gn, discord)
    elif args.gi:
        await nav.go_to_guild(args.gi, discord)
    elif args.private:
        await nav.go_to_guild("home", discord)

    await nav.get_channels(discord)

async def main():
    browser = await connect(browserURL="http://localhost:9222")
    pages = await browser.pages()
    discord = next(p for p in pages if "discord.com" in p.url)
    print(f"connected to discord: {discord}\n\n")

    if args.command == "text":
        await command_text(args, discord)
    elif args.command == "texts":
        await command_texts(args, discord)
    elif args.command == "channels":
        await command_channels(args, discord)

    print("Done.")

asyncio.get_event_loop().run_until_complete(main())
