import basic
import asyncio
from dataclasses import dataclass
@dataclass
class Channel:
    id:str
    name:str
    typ:str

    def __repr__(self):
        return f"{self.typ}\t{self.id: <20}\t{self.name}"

@dataclass
class Server:
    name: str
    id: str

    def __repr__(self):
        return f"{self.id: <20}\t{self.name}"

GUILD_ANIMATION_TIME = 0.2

async def go_to_guild_by_name(name, discord):
    await discord.click(f".blobContainer_e5445c[data-dnd-name=\"{name}\"]")
    print(f"[nav] Navigated to guild \"{name}\", waiting {GUILD_ANIMATION_TIME}sec for animation... ")
    await asyncio.sleep(GUILD_ANIMATION_TIME)

async def go_to_guild(id, discord):
    await basic.click_data_list_item_by_id("guildsnav", id, discord)
    print(f"[nav] Navigated to guild \"{id}\", waiting {GUILD_ANIMATION_TIME}sec for animation... ")
    await asyncio.sleep(GUILD_ANIMATION_TIME)

async def list_guilds(id, discord):
    await basic.click_data_list_item_by_id("guildsnav", id, discord)
    print(f"[nav] Navigated to guild \"{id}\", waiting {GUILD_ANIMATION_TIME}sec for animation... ")
    await asyncio.sleep(GUILD_ANIMATION_TIME)

async def go_to_channel(id, discord, dm=False):
    if dm:
        await discord.click(f"[href*=\"/channels/@me/{id}\"]")
        print(f"[nav] Opened channel (PRIVATE DM) {id}.")
        return

    print(f"[nav] Opened channel (TEXT CHANNEL) {id}.")
    await basic.click_data_list_item_by_id("channels", id, discord)

async def go_to_channel_by_name(name, discord):
    await discord.click(f'.containerDefault_c69b6d[data-dnd-name="{name}"]')
    print(f"[nav] Opened channel (TEXT CHANNEL) \"{name}\".")

async def get_servers(discord):
    servers = await discord.evaluate(GET_GUILDS)
    parsed_servers = []
    for server in servers:
        parsed = Server(server["name"], server["id"])
        parsed_servers.append(parsed)
        print(parsed)
    
    return parsed_servers
GET_GUILDS = """
() =>
{
	const scroller = document.querySelector('.scroller_ef3116');
	scroller.scrollTo(0, scroller.scrollHeight);
	const channels = [];
	document.querySelectorAll('[data-list-item-id^="guildsnav___"]').forEach(el =>
	{
		const id = el.getAttribute('data-list-item-id').split('___')[1];
		const nameEl = el.querySelector('.hiddenVisually__27f77');
		const name = nameEl ? nameEl.textContent.trim() : 'unknown';
		console.log(id, nameEl, name)
		console.log(id, name)

		channels.push(
		{
			id,
			name,
		});
	});
	return channels;
}
"""

GET_CH_JS = """
() =>
{
	const scroller = document.querySelector('.content__99f8c');
	scroller.scrollTo(0, scroller.scrollHeight);
	const channels = [];
	document.querySelectorAll('[data-list-item-id^="channels___"]').forEach(el =>
	{
		const id = el.getAttribute('data-list-item-id').split('___')[1];
		const nameEl = el.querySelector('.name__2ea32');
		const name = nameEl ? nameEl.textContent.trim() : 'unknown';
		console.log(id, nameEl, name)
		const type = el.getAttribute('aria-label').includes('(text channel)') ? "tc" :
			el.getAttribute('aria-label').includes('(voice channel)') ? "vc" :
			"unknown";
		console.log(id, type)

		channels.push(
		{
			id,
			name,
			type
		});
	});
	return channels;
}
"""
async def get_channels(discord, json=False):
    channels = await discord.evaluate(GET_CH_JS)
    if json:
        return channels  # Don't parse just give raw JSON

    # Otherwise
    print("[nav] Parsing channels...")
    parsed_channels = []
    for ch in channels:
        parsed_channel = Channel(ch["id"], ch["name"], ch["type"])
        parsed_channels.append(parsed_channel)

    return parsed_channels