async def click_data_list_item_by_id(item, id, discord):
    await discord.click(f"[data-list-item-id=\"{item}___{id}\"]")

def get_data_list_item_by_id(item, id):
    return f"[data-list-item-id=\"{item}___{id}\"]"

async def selector_for_element_by_class(item, c):
    selector = f".{c}__{item}"
    #print(f"Selecting... {selector}")
    return selector

async def focus_discord_element_by_class(item, c, discord):
    await discord.focus(
        await selector_for_element_by_class(item, c)
    )

async def type_chars_to_message_bar(text, discord):
    await focus_discord_element_by_class("75297", "markup", discord)  # Hack because its a div and not an input
    await discord.keyboard.type(text)

async def send_message_via_return(discord):
    await focus_discord_element_by_class("75297", "markup", discord)
    await discord.keyboard.press("Enter")

async def find_inner_htmls(selector, discord):
    try:
        evals = await discord.querySelectorAllEval(
            selector,
            '(nodes) => nodes.map(n => n.textContent)'
        )
    except:
        return None

    return evals

async def find_last_inner_html(selector, discord, index=-1):
    try:
        evals = await discord.querySelectorAllEval(
            selector,
            '(nodes) => nodes.map(n => n.textContent)'
        )
        #print(f"evals for {selector} index={index} are: {evals}")
        html = evals[index]
    except Exception as e:
        #print(f"evals for {selector} index={index} are: None (exception {e})")
        return None  # indication to stop (there are no more messages)

    return html

async def is_message_reply(discord):
    result = False

    reply_container = await discord.querySelector(".repliedMessage_c19a55")
    result = await find_last_inner_html(".username_c19a55", reply_container, 0)
    #print(f"is_reply: {result}")
    return result

async def get_message_reply_text(discord):
    result = False

    reply_container = await discord.querySelector(".repliedTextPreview_c19a55")
    result = await find_last_inner_html(".repliedTextContent_c19a55", reply_container, 0)
    #print(f"is_reply: {result}")
    return result