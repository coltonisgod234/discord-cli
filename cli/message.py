from . import basic
from dataclasses import dataclass
import textwrap
import asyncio

TEXT_CONTENT_FORMAT_CUTOFF = 14
USERNAME_FORMAT_CUTOFF = 7
REPLY_BADGE_TEXT = "REPLY"
REPLY_BADGE_WIDTH_FSTRING = 32
USERNAME_WIDTH_FSTRING = 20

@dataclass
class DiscordMessage:
    id: int
    user_displayname: str
    timestamp: any
    text_content: str
    reply_to: str | None
    reply_text_content: str | None

    def __repr__(self):
        reply = ""
        if None not in [self.reply_text_content, self.reply_to]:
            reply = f"({REPLY_BADGE_TEXT} {self.reply_to[:USERNAME_FORMAT_CUTOFF]}… {self.reply_text_content[:TEXT_CONTENT_FORMAT_CUTOFF]}…)"

        user = self.user_displayname if self.user_displayname is not None else ""
        return f"{self.id} \t{reply:<{REPLY_BADGE_WIDTH_FSTRING}}\t {user: <{USERNAME_WIDTH_FSTRING}}\t\t\t\t{self.text_content}"

async def click_message_bar(discord):
    await basic.click_discord_element_by_class("74017", "textArea", discord)

async def type_to_message_bar(text, discord):
    await basic.type_chars_to_message_bar(text, discord)  # Type in
    await basic.send_message_via_return(discord)  # Send

def get_message_id(data_id: str):
    # [0] (for some reason...) = channel ID of message
    # [1] = message ID
    data_id = data_id.replace("chat-messages-", "")
    split_id = data_id.split("-")
    return split_id[1]

async def get_all_messages_in_current_ch(discord):
    message_scroller = await discord.querySelector("[data-list-id='chat-messages']")
    parsed_messages = []

    msg_wrappers = await message_scroller.querySelectorAll("[id^='chat-messages-']")
    for wrapper in msg_wrappers:
        msg_id = get_message_id(await wrapper.executionContext.evaluate('(el) => el.getAttribute("id")', wrapper)),  # For some reason this is still a tuple with length 1
        msg_id = msg_id[0]
        msg_selector_id = f"{msg_id}"
        username_selector = f"[id='message-username-{msg_selector_id}']"
        parsed_messages.append(DiscordMessage(
            # stupid hack around pyppeteer bullshit
            msg_id,
            await basic.find_last_inner_html(username_selector, wrapper),
            await basic.find_last_inner_html(f"[id='message-timestamp-{msg_selector_id}']", wrapper),
            await basic.find_last_inner_html(f"[id='message-content-{msg_selector_id}']", wrapper),
            await basic.is_message_reply(wrapper),
            await basic.get_message_reply_text(wrapper)
        ))

    return parsed_messages

async def stream_all_messages_in_current_ch(discord, parse=True):
    # Get the container & all message wrappers (ElementHandles)
    message_scroller = await discord.querySelector("[data-list-id='chat-messages']")
    msg_wrappers = await message_scroller.querySelectorAll("[id^='chat-messages-']")

    # Bulk-extract id, username, timestamp, content in one evaluate call
    js_extract = """
    () => {
    const messages = [];
    const wrappers = document.querySelectorAll("[id^='chat-messages-']");
    wrappers.forEach(wrapper => {
        const id = wrapper.getAttribute("id");
        const actual_fucking_id = id.split("-")[3];
        console.log(id, actual_fucking_id)
        const usernameEl = wrapper.querySelector(`[id='message-username-${actual_fucking_id}']`);
        const timestampEl = wrapper.querySelector(`[id='message-timestamp-${actual_fucking_id}']`);
        const contentEl = wrapper.querySelector(`[id='message-content-${actual_fucking_id}']`);
        console.log(usernameEl, timestampEl, contentEl)

        // Port of is_message_reply:
        const replyContainer = wrapper.querySelector("[aria-label*='replying to']");
        const replyTo = replyContainer ? replyContainer.textContent : null;

        // Port of get_message_reply_text:
        let replyText = "";
        const replyTextContainer = wrapper.querySelector(".repliedTextPreview_c19a55");
        if (replyTextContainer) {
        const replyContentEl = replyTextContainer.querySelector(".repliedTextContent_c19a55");
        replyText = replyContentEl ? replyContentEl.textContent : null;
        }

        messages.push({
            id: actual_fucking_id,
            username: usernameEl ? usernameEl.textContent : "(SHIT)",
            timestamp: timestampEl ? timestampEl.textContent : "(SHIT)",
            content: contentEl ? contentEl.textContent : "(SHIT)",
            replyTo,
            replyText
        });
    });
    return messages;
    }
    """
    raw_messages = await discord.evaluate(js_extract)

    # Zip ElementHandles and raw data, then run python reply checks per wrapper
    for wrapper, raw_msg in zip(msg_wrappers, raw_messages):
        is_reply = await basic.is_message_reply(wrapper)
        reply_text = await basic.get_message_reply_text(wrapper)

        if parse:
            yield DiscordMessage(
                raw_msg["id"],
                raw_msg["username"],
                raw_msg["timestamp"],
                raw_msg["content"],
                raw_msg["replyTo"],
                raw_msg["replyText"]
            )
            await asyncio.sleep(0)  # let event loop run
        else:
            yield raw_msg
            await asyncio.sleep(0)  # let event loop run