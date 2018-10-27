from enum import IntEnum
import telepot
import time
import datetime
import commands
import listHandler


# add user id's here
class Members(IntEnum):
    HOST = 0
    USER1 = 0
    # User 2 to n ....
    CHAT_ID = 0


class Status:
    state_react = 1
    state_add = 0
    item_list = []


def handle(msg):
    # split receive3d message
    id = msg['from']['id']
    chat_id = msg['chat']['id']
    command = msg['text']
    if id != Members.HOST:
        user = msg['from']['first_name'], msg['from']['username']
    else:
        user = msg['from']['first_name']

    # show payload in terminal
    print(msg)

    # log unauthorized user
    if id != Members.HOST and \
            id != Members.USER1:

        bot.sendMessage(chat_id, "You are not registered!")

        payload = "Unauthorized user has used your bot. \nUser: " + str(user[0]) + " " + str(user[1]) + " \nID: " + str(
            id)

        bot.sendMessage(int(Members.CHAT), payload)

        log = open("Log_unauthorized.txt", "a")
        log.write(str(datetime.datetime.now()) + ": " + str(user[0]) + " " + str(user[1]) + " ID: " + str(id) + "\n")
        log.close()

    # following code works only for registered user id's (class Members)
    else:
        # loop adding items
        if Status.state_add == 1:
            if command == "!cancel":
                Status.state_add = 0
                listHandler.to_file(Status.item_list)
                Status.item_list.clear()
            else:
                items = command.split(",")
                for i in range(len(items)):
                    Status.item_list.append(str(items[i]).strip())
        else:
            # bot will not answer
            if str(command).startswith("/pi_stop"):
                Status.state_react = 0
                bot.sendMessage(chat_id, "I'm now in silent-mode")

            # will answer
            elif str(command).startswith("/pi_start"):
                Status.state_react = 1
                bot.sendMessage(chat_id, "I'm is now listening")

            # when activated
            if Status.state_react != 0:

                # show commands
                if command == "!commands":
                    commands.send_commands(bot, chat_id)

                # print shoppinglist
                elif command == "!shop":
                    shopping_list = listHandler.to_list()
                    if not shopping_list:
                        bot.sendMessage(chat_id, "Your list is empty.")
                    else:
                        listHandler.send_list(bot, chat_id, shopping_list)

                # clear shoppinglist
                elif command == "!clear":
                    listHandler.clear()
                    bot.sendMessage(chat_id, "You have cleared the list!")

                # remove products
                elif str(command).startswith("!remove"):
                    item = str(command).split(" ")[1]
                    items = item.split(",")
                    for i in range(len(items)):
                        listHandler.remove_from_list(items[i].strip(), bot, chat_id)

                # calling queue for
                elif str(command).startswith("!add"):
                        Status.state_add = 1

                        bot.sendMessage(chat_id, "Enter some products. E.g.: Cheese or more like milk, sausage, cookies. "
                                                 "Type *!cancel* to end listener", 'Markdown')


bot = telepot.Bot('ENTER YOUR TELEGRAM BOT TOKEN HERE') # see readme for manual
bot.message_loop(handle)

while 1:
    time.sleep(10)
