import os

os.environ['TORCH_USE_RTLD_GLOBAL'] = "true"

import logging
from fastapi import FastAPI, WebSocket

from bot.constants import SOURCE_PROMPT, REPHRASE_PROMPT
from bot.init_chat import init_chat
from bot.retrieve_related_docs import retrieve_related_docs

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        data = await websocket.receive_json()
        query = data["query"]
        history = data["history"]

        if len(history) > 0:
            system_msg = REPHRASE_PROMPT.format(
                user_msg=history[0]["msg"] if len(history) != 0 else "",
                bot_msg=history[1]["msg"] if len(history) != 0 else ""
            )

            chat_response = init_chat([{"role": "system", "content": system_msg}, {"role": "user", "content": query}])

            bot_msg = ""
            for delta in chat_response:
                if "content" in delta:
                    bot_msg += delta.content
            query = bot_msg

        related_docs = retrieve_related_docs(query)

        await websocket.send_json({
            "type": "sources",
            "data": list(set(map(lambda related_doc: f"[{related_doc[1].title}]({related_doc[1].url})", related_docs)))
        })

        system_msg = SOURCE_PROMPT.format(
            sources=map(lambda related_doc: f"Source: {related_doc[0]}\nContent: ```\n{related_doc[1]}\n```",
                        related_docs))

        messages = [{"role": "system", "content": system_msg}]
        if len(history) > 0:
            messages.append({"role": "user", "content": history[0]["msg"]})
            messages.append({"role": "assistant", "content": history[1]["msg"]})
        messages.append({"role": "user", "content": data["query"]})

        chat_response = init_chat(data["api_key"], messages)

        bot_msg = ""
        for delta in chat_response:
            if "content" in delta:
                bot_msg += delta.content
                await websocket.send_json({
                    "type": "response",
                    "data": bot_msg
                })

    except Exception as e:
        logger.error(e)
        return


port = int(os.environ.get("PORT", 8080))  # Retrieve the PORT environment variable, defaulting to 8000

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=port)
