async def click_button_js(selector, discord):
    '''
    Use this if discord.click is being a little bitch
    '''
    print(f"selector {selector}")
    await discord.evaluate(f'''() => {{
    const btn = document.querySelector(\"{selector}\");
    if (btn) {{ btn.click(); }}
    }}''')


async def click_data_list_item_by_id(item, id, discord):
    await discord.click(f"[data-list-item-id=\"{item}___{id}\"]")

def get_data_list_item_by_id(item, id):
    return f"[data-list-item-id=\"{item}___{id}\"]"

async def type_chars_to_message_bar(text, discord):
    await discord.type("[aria-label*='Message #']", text)

async def send_message_via_return(discord):
    await discord.click("[aria-label*='Message #']")
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
        print(f"evals for {selector} index={index} are: {evals}")
        html = evals[index]
    except Exception as e:
        print(f"evals for {selector} index={index} are: None (exception {e})")
        return None  # indication to stop (there are no more messages)

    return html

async def is_message_reply(discord):
    result = False

    reply_container = await discord.querySelector("[aria-label*='replying to']")
    result = await find_last_inner_html(".username_c19a55", reply_container, 0)
    #print(f"is_reply: {result}")
    return result

async def get_message_reply_text(discord):
    result = False

    reply_container = await discord.querySelector(".repliedTextPreview_c19a55")
    result = await find_last_inner_html(".repliedTextContent_c19a55", reply_container, 0)
    #print(f"is_reply: {result}")
    return result