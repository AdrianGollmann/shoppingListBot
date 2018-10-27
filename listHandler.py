def clear():
    myfile = open("shoppingList.txt", "w+")
    myfile.close()


# capitalize first character of string
def format_list(item_list):
    list = []
    for item in item_list:
        list.append(str(item).title())
    return list


# remove multiple items on list
def remove_doublings(item_list):
    list = []
    for item in format_list(item_list):
        if item not in list:
            list.append(item)
    return list


# save list in textfile
def to_file(item_list):
    myfile = open("shoppingList.txt", "a")
    myList = to_list()
    for item in remove_doublings(item_list):
        if item not in myList:
            myfile.write(item + "\n")

    myfile.close()


# TODO: pretty output in messenger
# not working correct
def format_item(item1, item2, length_max):
    l1 = length_max - len(item1)
    l2 = length_max - len(item2)
    t = ""
    for i in range(l1):
        t = t + " "
    t = t + "\t"
    item = "{}" + t + "{}\n"
    return item


# prepare list as message for telegram
def send_list(bot, id, list):
    lines = int(len(list) / 2)
    items = "{:20}{:20}\n"
    list1 = []
    list2 = []
    for i in range(lines):
        list1.append(list[i])
        list2.append(list[i + lines])
    if len(list) % 2 != 0:
        list1.append(list[len(list) - 1])

    length = 0
    for i in list1:
        if len(i) > length:
            length = len(i)

    t = ""
    for i in range(len(list1) - 1):
        t = t + format_item(list1[i], list2[i], length).format(list1[i], list2[i])
    if len(list) % 2 != 0:
        t = t + str(list1[len(list1) - 1])
    else:
        t = t + items.format(list1[len(list1) - 1], list2[len(list2) - 1])

    bot.sendMessage(id, "\U0001F6D2" + "*Einkaufsliste*" + "\U0001F6D2\n" + t, 'Markdown')
    print(list1)
    print(list2)
    print(t)


# convert textfile to list
def to_list():
    list = []
    myfile = open("shoppingList.txt", "r")

    for line in myfile:
        line = line.strip()
        list.append(line)

    myfile.close()
    return list


# delete items from list
def remove_from_list(item, bot, id):
    newList = to_list()

    if item in newList:
        newList.remove(item)

        myfile = open("shoppingList.txt", "w")
        for item in newList:
            myfile.write(item + "\n")

        myfile.close()
    else:
        bot.sendMessage(id, "Item not in list.")
