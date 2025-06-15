import basic
import asyncio

class Channel:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name

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

async def get_channels(discord):
    channels = await discord.evaluate('''() => {
  const channels = [];
  document.querySelectorAll('[data-list-item-id^="channels___"]').forEach(el => {
    const id = el.getAttribute('data-list-item-id').split('___')[1];
    const nameEl = el.querySelector('.name__2ea32');
    const name = nameEl ? nameEl.textContent.trim() : 'unknown';
    channels.push({ id, name });
  });
  return channels;
}''')
    print("[nav] Parsing channels...")
    print(f"{'Channel ID':^19}\t{'Channel Name':^20}")
    print(f"1257780211525877821     unknown")
    parsed_channels = []
    for ch in channels:
        parsed_channel = Channel(ch["id"], ch["name"])
        parsed_channels.append(parsed_channel)
        print(f"{parsed_channel}")