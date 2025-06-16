import basic

async def leave_vc(discord):
    await basic.click_button_js(".button__67645[aria-label*='Disconnect']", discord)

async def unmute(discord):
    await discord.click("button[aria-label='Unmute']")

async def mute(discord):
    await discord.click("button[aria-label='Mute']")

async def undeaf(discord):
    await discord.click("button[aria-label='Undeafen']")

async def deaf(discord):
    await discord.click("button[aria-label='Deafen']")
