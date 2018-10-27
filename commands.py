def send_commands(bot, id):
    output_mesh = "{} - {}\n"
    t = ""
    list = [["!add", "add list"], ["!remove", "remove from list"], ["!clear", "clear a shopping list"],
            ["!remove [item, list]", "removes item from list or a list"], ["!lists", "show all lists"]]
    for i in range(len(list)):
        t = t + output_mesh.format(list[i][0], list[i][1])

    bot.sendMessage(id, "\U00002757" + "*Befehlsliste*" + "\U00002757"
                                                          "\n" + t, 'Markdown')

    print(t)
