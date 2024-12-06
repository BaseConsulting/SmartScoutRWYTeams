# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
import aiohttp
from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import Activity

class TeamsBot(ActivityHandler):
    def __init__(self):
        self.base_url = os.getenv("BACKEND_BASE_URL")
        self.chat_stream_endpoint = os.getenv("BACKEND_CHAT_STREAM_ENDPOINT")
        self.auth_token = os.getenv("AUTH_TOKEN")

    async def on_message_activity(self, turn_context: TurnContext):
        user_query = turn_context.activity.text
        headers = {"Content-Type": "application/json"}
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"

        payload = {
            "messages": [{"role": "user", "content": user_query}],
            "context": {},  # Include any additional context if necessary
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}{self.chat_stream_endpoint}",
                    json=payload,
                    headers=headers,
                ) as response:
                    if response.status == 200:
                        async for line in response.content:
                            if line.strip():
                                bot_response = line.decode("utf-8")
                                await turn_context.send_activity(bot_response)
                    else:
                        await turn_context.send_activity("An error occurred while processing your request.")
        except Exception as e:
            await turn_context.send_activity(f"An exception occurred: {str(e)}")
