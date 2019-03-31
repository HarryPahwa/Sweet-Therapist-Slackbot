import os
import time
import re
from slackclient import SlackClient
import json
import csv
import sys
import os

client_id=sys.argv[1]
# instantiate Slack client
slack_client = SlackClient(client_id)
#os.environ.get('SLACK_BOT_TOKEN'))
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None
users = None
channels = None
user_names=[]
top_names=[]
# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event and event["type"] != "desktop_notification" and event["type"] != "user_typing":
            print(slack_events)
    for event in slack_events:
        if event["type"] == "message" and "subtype" in event and event["subtype"] == "message_changed":
            message = "Dont you dare go changing them messages on me BOI"
            print(message)
            return message, event["channel"]
        if event["type"] == "message" and not "subtype" in event:
            # user_id, message = parse_direct_mention(event["text"])
            print(event["user"])
            # print(users["members"])
            for imember in  users["members"]:
                if imember["id"] == event["user"]:
                    print(imember["real_name"])
                    print(event["text"])
                    print("NAMES FOUND:")
                    name_found = "none"
                    for word in event["text"].split():
                        if(user_names.count(word)>0):
                            print("user name", end="")
                            name_found = word
                            print(name_found)
                        elif(top_names[0].count(word)>0):
                            print("list name", end="")
                            name_found = word
                            print(name_found)
                    print(name_found)
                    print()
                    # print(user_names[0])
                    message_channel = "private message"
                    for ichannel in channels["channels"]:

                        # print(ichannel["name_normalized"])
                        # print(ichannel["id"])
                        # print()
                        # print(event["channel"])
                        # print()
                        if (ichannel["id"] == event["channel"]):
                            message_channel = ichannel["name_normalized"]
                    print(message_channel)
            # if user_id == starterbot_id:
            #     return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "Not sure what you mean. Try *{}*.".format(EXAMPLE_COMMAND)

    # Finds and executes the given command, filling in response
    response = None
    # This is where you start to implement more commands!
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...write some more code then I can do that!"
    elif command.startswith("Dont you dare"):
        response = command
    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):




        with open('topNames.csv', 'r') as f:
            reader = csv.reader(f)
            your_list = list(reader)

        top_names=your_list


        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        channels=slack_client.api_call("conversations.list")
        users=slack_client.api_call("users.list")
        # print(json.dumps(channels, sort_keys=True, indent=4))

        # print(json.dumps(users, sort_keys=True, indent=4))

        for member in  users["members"]:
            try:
                user_names.append(member["real_name"])
                user_names.append(member["profile"]["first_name"])
                user_names.append(member["profile"]["last_name"])
            except:
                print("missing info")
        print(user_names)
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")
