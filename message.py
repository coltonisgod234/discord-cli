import basic
from dataclasses import dataclass
import textwrap

TEXT_CONTENT_FORMAT_CUTOFF = 14
USERNAME_FORMAT_CUTOFF = 7
REPLY_BADGE_TEXT = "REPLY"
REPLY_BADGE_WIDTH_FSTRING = 32
USERNAME_WIDTH_FSTRING = 20

@dataclass
class DiscordMessage:
    user_displayname: str
    timestamp: any
    text_content: str
    reply_to: str | None
    reply_text_content: str | None

    def __repr__(self):
        reply = ""
        if None not in [self.reply_text_content, self.reply_to]:
            reply = f"({REPLY_BADGE_TEXT} {self.reply_to[:USERNAME_FORMAT_CUTOFF]}… {self.reply_text_content[:TEXT_CONTENT_FORMAT_CUTOFF]}…)"

        user = self.user_displayname if self.user_displayname is not None else "(SYSTEM)"
        return f"{reply:<{REPLY_BADGE_WIDTH_FSTRING}} \t {user: <{USERNAME_WIDTH_FSTRING}}: \t {self.text_content}"

async def click_message_bar(discord):
    await basic.click_discord_element_by_class("74017", "textArea", discord)

async def type_to_message_bar(text, discord):
    await basic.type_chars_to_message_bar(text, discord)  # Type in
    await basic.send_message_via_return(discord)  # Send

async def get_all_messages_in_current_ch(discord):
    message_scroller = await discord.querySelector(".scrollerInner__36d07")
    parsed_messages = []

    msg_wrappers = await message_scroller.querySelectorAll(".messageListItem__5126c")
    for wrapper in msg_wrappers:
        parsed_messages.append(DiscordMessage(
            await basic.find_last_inner_html(".username_c19a55", wrapper),
            await basic.find_last_inner_html(".timestamp_c19a55", wrapper),
            await basic.find_last_inner_html(".messageContent_c19a55", wrapper),
            await basic.is_message_reply(wrapper),
            await basic.get_message_reply_text(wrapper)
        ))

    return parsed_messages