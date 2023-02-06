from nonebot.plugin.on import on_command
from nonebot.adapters.onebot.v11 import (
    GROUP,
    Bot,
    Message,
    MessageEvent,
    GroupMessageEvent,
    )

def msg_split(event:MessageEvent) -> list:
    '''
    拆分文字段落
    '''
    msg = str(event.message).strip().split(" ")
    msg_list = []
    for seg in msg:
        msg_list.append(Message(seg))
    return msg_list

# 伪造聊天记录

fabricate_chat = on_command("伪转发聊天记录 ", permission=GROUP, priority = 90, block = True)

@fabricate_chat.handle()
async def _(bot:Bot, event: GroupMessageEvent):
    group_id = event.group_id
    msg_list = msg_split(event)
    output =[]
    for msg in msg_list:
        at = None
        data = Message()
        for seg in msg:
            if seg.type == "at":
                at = int(seg.data["qq"])
            else:
                data += seg
        if data and at:
            info = await bot.get_group_member_info(group_id = group_id,user_id = at)
            nickname = info["card"] if info["card"] else info["nickname"]
            output.append(
                {
                    "type": "node",
                    "data": {
                        "name": nickname,
                        "uin": at,
                        "content": data
                        }
                    }
                )
    if output:
        await bot.send_group_forward_msg(group_id = group_id, messages = output)
    else:
        await fabricate_chat.finish()
