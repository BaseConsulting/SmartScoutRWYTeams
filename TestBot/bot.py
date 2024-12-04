# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount
from botbuilder.core import CardFactory, MessageFactory
from botbuilder.schema import SigninCard, ActionTypes


class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

    async def on_message_activity(self, turn_context: TurnContext):
        card = SigninCard(
        text="Please sign in to continue",
        buttons=[
            {
                "type": ActionTypes.signin,
                "title": "Sign in",
                "value": "https://login.microsoftonline.com/"
            }
        ]
        )
        await turn_context.send_activity(MessageFactory.attachment(CardFactory.signin_card(card)))
        await turn_context.send_activity(f"You said '{ turn_context.activity.text }'")

    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")
