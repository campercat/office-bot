import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

import logging
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
logger = logging.getLogger(__name__)

payload = {
	"blocks": [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Where are you working from today?"
			}
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "mrkdwn",
					"text": "*When:*\nJun 25"
				}
			]
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Office"
					},
					"style": "primary",
					"value": "click_me_123",
                    "action_id": "check_button"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Home"
					},
					"style": "primary",
					"value": "click_me_123",
                    "action_id": "check_button_2"
				}
			]
		}
	]
}

channel_name = "getting-people-connected"
conversation_id = None
try:
    # Call the conversations.list method using the WebClient
    for result in client.conversations_list():
        if conversation_id is not None:
            break
        for channel in result["channels"]:
            if channel["name"] == channel_name:
                conversation_id = channel["id"]
                #Print result
                print(f"Found conversation ID: {conversation_id}")
                break

except SlackApiError as e:
    print(f"Error: {e}")


# ID of the channel you want to send the message to
channel_id = conversation_id

try:
    # Call the chat.postMessage method using the WebClient
    result = client.chat_postMessage(
        channel=channel_id,
        text="notification to user",
        blocks=payload["blocks"]
    )
    logger.info(result)

except SlackApiError as e:
    logger.error(f"Error posting message: {e}")


# This listener will be called every time an interactive component with the `action_id` "approve_button" is triggered
# `block_id` is disregarded in this case
@app.action("check_button")
def some_action_response(ack,say):
    ack()
    # Do something in response
    say("Thank you! I have updated your working location!")


# Listens to incoming messages that contain "hello"
@app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Hey there <@{message['user']}>!"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Click Me"},
                    "action_id": "button_click"
                }
            }
        ],
        text=f"Hey there <@{message['user']}>!"
    )

@app.action("button_click")
def action_button_click(body, ack, say):
    # Acknowledge the action
    ack()
    say(f"<@{body['user']['id']}> clicked the button")

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
