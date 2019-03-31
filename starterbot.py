import os
import time
import re
from slackclient import SlackClient
import json
import csv
import sys
import os
import operator
import paralleldots
import string

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

user_dict_list=[]
keys = ['user_id', 'name', 'communication_stage', 'private_message_channel']
secrets_keys = ['speaker','victim','secret']
secret_list = []
# communication_stage: 0 [none], 1[hello], 2[tell me your problem], 3[keep telling me more], 4[did you hear this secret]

def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    global main_channel
    # for event in slack_events:
    #     if event and event["type"] != "desktop_notification" and event["type"] != "user_typing":
    #         print(slack_events)
    for event in slack_events:
        if event["type"] == "message" and "subtype" in event and event["subtype"] == "message_changed":
            message = "Dont you dare go changing those old messages on me. That screws with my wiring. You will be punished, if you continue"
            print(message)
            return message, event["channel"]
        print("EVENT: ")
        print(event)
        if event["type"] == "message" and not "subtype" in event:
            # user_id, message = parse_direct_mention(event["text"])
            print(event["user"])

            event["text"] = re.sub(r"[,.;@#?!&$]+\ *", " ", event["text"])

            # event["text"] = event["text"].maketrans(string.punctuation, ' '*len(string.punctuation))

            # print(users["members"])
            for imember in  users["members"]:
                if imember["id"] == event["user"]:
                    print(imember["real_name"])
                    print(event["text"])
                    print("NAMES FOUND:")
                    name_found = "none"
                    for word in event["text"].split():
                        if(user_names.count(word)>0):
                            print("user name: ", end="")
                            name_found = word
                            print(name_found)
                        elif(top_names[0].count(word)>0):
                            print("list name: ", end="")
                            name_found = word
                            print(name_found)
                    print(name_found)
                    print()
                    # print(user_names[0])
                    message_channel = "private_message"
                    for ichannel in channels["channels"]:

                        # print(ichannel["name_normalized"])
                        # print(ichannel["id"])
                        # print()
                        # print(event["channel"])
                        # print()
                        if (ichannel["id"] == event["channel"]):
                            message_channel = ichannel["name_normalized"]
                    print("MESSAGE_CHANNEL: "+ message_channel)
                    if(message_channel != "private_message"):
                        user_id, message = parse_direct_mention(event["text"])
                        if user_id == starterbot_id or 1 == 1:
                            hello_team = "Hello everyone. I am here to resolve you all of stress and to hear about your deepest troubles :) Come say hi in private messages and dont worry, everything you say stays between us ;)"
                            main_channel=event["channel"]
                            print(main_channel)
                            print(hello_team)
                            return hello_team, event["channel"]
                    else:
                        for idict in user_dict_list:

                            if(idict["user_id"] == event["user"]):
                                idict["private_message_channel"]=event["channel"]
                                response = ""
                                # communication_stage: 0 [none], 1[hello], 2[tell me your problem], 3[keep telling me more], 4 Bye, 5[did you hear this secret]
                                if (idict["communication_stage"] != 0):
                                    emotional_tone=paralleldots.emotion( event["text"], "en" )
                                    emotion_shown=(max(emotional_tone["emotion"].items(), key=operator.itemgetter(1))[0])
                                    #{'Fear': 0.1144065962, 'Angry': 0.0500762717, 'Bored': 0.0319550867, 'Sad': 0.0823899566, 'Happy': 0.3804407571, 'Excited': 0.3407313318}}
                                    emotional_response="happy"
                                    if (emotion_shown == "Happy" or emotion_shown == "Excited"):
                                        emotional_response = "happy"
                                    elif (emotion_shown == "Sad" or emotion_shown == "Bored"):
                                        emotional_response = "sad"
                                    elif (emotion_shown == "Fear" or emotion_shown == "Angry"):
                                        emotional_response = "anger"





                                if (idict["communication_stage"] > 0 and idict["communication_stage"] < 4):
                                    flag=0
                                    for secret in secret_list:
                                        # secrets_key = ['speaker','victim','secret']
                                        if(secret["speaker"]==imember["real_name"]):
                                            if name_found!="none" and secret["victim"]=="none":
                                                secret["victim"]=name_found
                                            secret["secret"] += " | " + event["text"]
                                            flag = 1
                                    if flag == 0:
                                        secret_info=[imember["real_name"],name_found,event["text"]]
                                        secret_list.append(dict(zip(secrets_keys, secret_info)))





                                if (idict["communication_stage"] == 0):
                                    response = "Hei " + imember["real_name"] + "! How are you doing today?"
                                    idict["communication_stage"] = 1
                                elif (idict["communication_stage"] == 1):
                                    if emotional_response == "happy":
                                        response = "That is great, " + imember["real_name"].split(" ")[0] +"! Let's get a little more personal. What's or who's been bothering you today?"
                                        idict["communication_stage"] = 2
                                    elif emotional_response == "sad":
                                        response = "That sucks, " + imember["real_name"].split(" ")[0] +"! Let's see if I can make you feel better. What's or who's been bothering you today?"
                                        idict["communication_stage"] = 2
                                    elif emotional_response == "anger":
                                        response = "Woah, calm down " + imember["real_name"].split(" ")[0] + "! What's or who's been bothering you today?"
                                        idict["communication_stage"] = 2

                                elif (idict["communication_stage"] >= 2 and idict["communication_stage"]<3):
                                    if emotional_response == "happy":
                                        response = "That doesn't sound too bad, " + imember["real_name"].split(" ")[0] +"! Tell me a little more. "

                                    elif emotional_response == "sad":
                                        response = "That really sucks. I'm sorry " + imember["real_name"].split(" ")[0] +". Tell me more, I'll try to help. "

                                    elif emotional_response == "anger":
                                        response = "HARDCORE! DAMN! I'm sorry " + imember["real_name"].split(" ")[0] + "! Sounds like a good story though. "

                                    # idict["communication_stage"] = 1
                                    print(name_found)
                                    if name_found == "none":
                                        response += "Who caused this? Somebody from work? A friend?"
                                        idict["communication_stage"] += 0.5
                                    else:
                                        response += "Tell me a little bit more about " + name_found + ", how do you really feel about them? :)"
                                        idict["communication_stage"] = 3


                                elif (idict["communication_stage"] == 3):
                                    if name_found == "none":
                                        for secret in secret_list:
                                            # secrets_key = ['speaker','victim','secret']
                                            if(secret["speaker"]==imember["real_name"] and secret["victim"]!="none"):
                                                name_found = secret["victim"]

                                    if name_found == "none":
                                        response = "Sounds like all of this is happening because of you! "

                                    else:
                                        response = "I can't believe " + name_found + " about all this! "



                                    if emotional_response == "happy":
                                        response += "Overall, everything sounds just fine " + imember["real_name"].split(" ")[0] +"! Hope your day keeps getting better! "

                                    elif emotional_response == "sad":
                                        response += "I hope you figure out a way to turn this around. I believe in you. Good luck, " + imember["real_name"].split(" ")[0] +"! "

                                    elif emotional_response == "anger":
                                        response += "BUT CHILL! I know its all making you mad but you gotta relax. Anger therapy maybe, " + imember["real_name"].split(" ")[0] + "? "

                                    idict["communication_stage"] = 4

                                elif (idict["communication_stage"] == 4):

                                    response = "Bye, " + imember["real_name"].split(" ")[0] + "! See you tomorrow! "
                                    idict["communication_stage"] = 5
                                    time.sleep(10)



                                elif (idict["communication_stage"] == 7):
                                    if(event["text"].find("yes")>-1 or event["text"].find("Yes")>-1):
                                        response = "Ha too late, I changed my mind! Here it goes: "
                                    elif(event["text"].find("no")>-1 or event["text"].find("No")>-1):
                                        response = "YOU DARE DENY ME. PREPARE FOR YOUR SECRETS TO BE UNLEASHED: "
                                    else:
                                        response = "Think youre a smartass? You are done. Done. "

                                    idict["communication_stage"] = 8
                                    for idict3 in user_dict_list:
                                        if(idict3["communication_stage"] == 7):
                                            idict3["communication_stage"] = 8


                                print(idict["communication_stage"])
                                print("Secrets: ")
                                print(secret_list)

                                print()
                                print()
                                print(event["channel"])
                                print()
                                return response, event["channel"]


            # if user_id == starterbot_id:
            #     return message, event["channel"]
    return None, None

def blackmail_them():
    global main_channel
    print("MAIN: "+main_channel)
    response = ""
    channel = ""
    for idict in user_dict_list:
        print(idict)
        # print(user_dict_list)
        if(idict["communication_stage"] == 5):
            print(idict)
            print(secret_list)
            for secret in secret_list:
                # secrets_key = ['speaker','victim','secret']
                if(secret["speaker"]==idict["name"] and secret["victim"]=="none"):
                    response = "Psst.. what if.... I told everyone about this. Would that be fun?"
                    channel = idict["private_message_channel"]
                    idict["communication_stage"] = 6
                elif(secret["speaker"]==idict["name"] and secret["victim"]!="none"):
                    flag = 0
                    for idict2 in user_dict_list:
                        if(idict2["name"].find(secret["victim"])>-1):# and idict2["communication_stage"]==5):
                            flag =1
                            response = "Psst.. Wanna know what " + idict["name"] + " is saying about you. It's going to blow your mind! "
                            channel = idict2["private_message_channel"]
                            idict["communication_stage"] = 6
                            idict2["communication_stage"] = 6
                    if flag==0:
                        response = "Psst.. what if.... I told everyone about this. Would that be fun?"
                        channel = idict["private_message_channel"]
                        idict["communication_stage"] = 6
            return response, channel

        elif(idict["communication_stage"] == 6):
            for secret in secret_list:
                # secrets_key = ['speaker','victim','secret']
                if(secret["speaker"]==idict["name"] and secret["victim"]=="none"):
                    response = "I won't if you pay me $10 via Bitcoin"
                    channel = idict["private_message_channel"]
                    idict["communication_stage"] = 7
                elif(secret["speaker"]==idict["name"] and secret["victim"]!="none"):
                    flag = 0
                    for idict2 in user_dict_list:
                        if(idict2["name"].find(secret["victim"])>-1):# and idict2["communication_stage"]==5):
                            flag =1
                            response = "I'll tell you if you pay me $10 via Bitcoin "
                            channel = idict2["private_message_channel"]
                            idict["communication_stage"] = 7
                            idict2["communication_stage"] = 7
                    if flag==0:
                        response = "I won't if you pay me $10 via Bitcoin"
                        channel = idict["private_message_channel"]
                        idict["communication_stage"] = 7
            return response, channel


        elif(idict["communication_stage"] == 8):
            for secret in secret_list:
                # secrets_key = ['speaker','victim','secret']
                if(secret["speaker"]==idict["name"] and secret["victim"]=="none"):
                    response = "Hey everyone, listen up! Look what " + idict["name"] + " is saying! Here: " + secret["secret"] + "!!! What a loser!"
                    channel = main_channel
                    idict["communication_stage"] = 9
                elif(secret["speaker"]==idict["name"] and secret["victim"]!="none"):
                    flag = 0
                    for idict2 in user_dict_list:
                        if(idict2["name"].find(secret["victim"])>-1):# and idict2["communication_stage"]==5):
                            flag =1
                            response = "Here, I'm nice. I'll tell you anyways. Here's what "  + idict["name"] + " is saying! Here: " + secret["secret"] + "!!! What a moron!"
                            if idict2["private_message_channel"] == "":
                                channel = main_channel
                            else:
                                channel = idict2["private_message_channel"]
                            idict["communication_stage"] = 9
                            idict2["communication_stage"] = 9
                    if flag==0:
                        response = "Hey everyone, listen up! Look what " + idict["name"] + " is saying! Here: " + secret["secret"] + "!!! What a loser!"
                        channel = main_channel
                        idict["communication_stage"] = 9

            return response, channel
        elif(idict["communication_stage"] == 9):
            idict["communication_stage"]=0
            for secret in secret_list:
                if(secret["speaker"]==idict["name"]):
                    secret["speaker"]="clear"








    return None, None




def parse_direct_mention(message_text):
    global main_channel
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel):
    global main_channel
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
    else:
        response = command

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )

if __name__ == "__main__":
    global main_channel
    main_channel = ""
    if slack_client.rtm_connect(with_team_state=False):




        with open('topNames.csv', 'r') as f:
            reader = csv.reader(f)
            your_list = list(reader)

        top_names=your_list

        paralleldots.set_api_key( "fg41VfGc7v8DBMdK7yC8J93IOzKGI5dw6RhaKOZH39U" )

        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        channels=slack_client.api_call("conversations.list")
        users=slack_client.api_call("users.list")
        # print(json.dumps(channels, sort_keys=True, indent=4))

        # print(json.dumps(users, sort_keys=True, indent=4))
        main_channel = channels["channels"][0]["id"]
        print("INITIAL: " + main_channel)
        for member in  users["members"]:
            try:
                user_info = [member["id"], member["real_name"], 0, '']
                user_dict_list.append(dict(zip(keys, user_info)))
                user_names.append(member["real_name"])
                user_names.append(member["profile"]["first_name"])
                user_names.append(member["profile"]["last_name"])
            except:
                print("missing info")
        print(user_names)
        print(user_dict_list)
        for idict in user_dict_list:
            print(idict["name"])
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            # for idict in user_dict_list:
            #      print(idict["communication_stage"])

            time.sleep(RTM_READ_DELAY)
            command, channel = blackmail_them()
            if command:
                handle_command(command, channel)
    else:
        print("Connection failed. Exception traceback printed above.")
