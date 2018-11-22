""" Customer Relationship Management (CRM) module

Data table structure:
    * id (string): Unique and random generated identifier
        at least 2 special characters (except: ';'), 2 number, 2 lower and 2 upper case letters)
    * name (string)
    * email (string)
    * subscribed (int): Is she/he subscribed to the newsletter? 1/0 = yes/no
"""

# everything you'll need is imported:
# User interface module
import ui
# data manager module
import data_manager
# common module
import common


def start_module():
    """
    Starts this module and displays its menu.
     * User can access default special features from here.
     * User can go back to main menu from here.

    Returns:
        None
    """

    table = data_manager.get_table_from_file("crm/customers.csv")
    table_title = ["id", "name", "email", "subscribed"]

    list_options = ["Show table",
                    "Add person",
                    "Remove person",
                    "Update table",
                    "Get ID of the person with the longest name",
                    "Get list of subscribers email addresses"]

    ui.print_menu("CRM module menu:", list_options, "Exit program")
    while True:
        option = ui.get_inputs(["Please enter a number"], "")
        if option[0] == "1":
            show_table(table)
        elif option[0] == "2":
            table = add(table)
        elif option[0] == "3":
            id_ = ui.get_inputs(["ID: "], "Please type ID to remove: ")[0]
            table = remove(table, id_)
        elif option[0] == "4":
            id_ = ui.get_inputs(["ID: "], "Please type ID to update: ")[0]
            table = update(table, id_)
        elif option[0] == "5":
            result = get_longest_name_id(table)
            ui.print_result(result, "Printing the ID of the person with the longest name")
        elif option[0] == "6":
            result = get_subscribed_emails(table)
            ui.print_result(result, "Printing a list with the name and email addresses of the subscribers")
        elif option[0] == "0":
            exit()
        else:
            ui.print_error_message("No such an option!")


def show_table(table):
    """
    Display a table

    Args:
        table (list): list of lists to be displayed.

    Returns:
        None
    """
    title_list = ["id", "name", "email", "subscribed"]
    table = data_manager.get_table_from_file("crm/customers.csv")
    ui.print_table(table, title_list)


def add(table):
    """
    Asks user for input and adds it into the table.

    Args:
        table (list): table to add new record to

    Returns:
        list: Table with a new record
    """

    list_labels = ["name: ", "email: ", "subscribed: "]
    wanna_stay = True
    while wanna_stay:
        new_product = ui.get_inputs(list_labels, "Please provide new information")
        new_product.insert(0, common.generate_random(table))
        table.append(new_product)
        next_step = ui.get_inputs([""], "Press 0 to save & exit or 1 to add another person.")[0]
        if next_step == "0":
            data_manager.write_table_to_file("crm/customers.csv", table)
            wanna_stay = False
    return table


def remove(table, id_):
    """
    Remove a record with a given id from the table.

    Args:
        table (list): table to remove a record from
        id_ (str): id of a record to be removed

    Returns:
        list: Table without specified record.
    """

    wanna_stay = True
    current_iterates = 0
    max_iterates = len(table)
    while wanna_stay:
        for i, v in enumerate(table):
            if v[0] == id_:
                table.remove(table[i])
            elif v[0] != id_ and current_iterates < max_iterates:
                current_iterates += 1
            else:
                ui.print_error_message("There is nothing with the given ID!")
        next_step = ui.get_inputs([""], "Press 0 to exit or 1 to remove another person.")[0]
        if next_step == '0':
            data_manager.write_table_to_file("crm/customers.csv", table)
            wanna_stay = False
        else:
            id_ = ui.get_inputs(["Please type ID to remove: "], "\n")[0]
            continue
    return table


def update(table, id_):
    """
    Updates specified record in the table. Ask users for new data.

    Args:
        table (list): list in which record should be updated
        id_ (str): id of a record to update

    Returns:
        list: table with updated record
    """

    wanna_stay = True
    current_iterates = 0
    max_iterates = len(table)
    while wanna_stay:
        for i, v in enumerate(table):
            if v[0] == id_:
                first_step = ui.get_inputs([""], "Please specify, what would you like to change at the given index? (name, email, subscription)")[0]
                if first_step == "name":
                    new_name = ui.get_inputs([""], "Please give a new name!")
                    v[1] = new_name[0]
                elif first_step == "email":
                    new_email = ui.get_inputs([""], "Please give a new email address!")
                    v[2] = new_email[0]
                elif first_step == "subscription":
                    new_subscription = ui.get_inputs([""], "Please give a new subscription option! (0 for NOT subscribed and 1 for subscribed")
                    v[3] = new_subscription[0]
                else:
                    ui.print_error_message("There's no such an option!")
            elif v[0] != id_ and current_iterates < max_iterates:
                current_iterates += 1
            else:
                ui.print_error_message("You can't add an item because of some reasons!")
        last_step = ui.get_inputs([""], "Press 0 to exit or 1 to update another item.")[0]
        if last_step == '0':
            data_manager.write_table_to_file("crm/customers.csv", table)
            wanna_stay = False
        else:
            id_ = ui.get_inputs(["Please type an ID to update the item at the given ID: "], "\n")[0]
            continue

    return table


# special functions:
# ------------------


def get_longest_name_id(table):
    nList = []
    lList = []
    name = []
    possible_results = []
    a = []
    for inList in table:
        nList.append(inList[1])
    for i in range(0, len(nList)):
        lList.append(len(nList[i]))
    maxLen = 0
    for num in lList:
        if maxLen < num:
            maxLen = num
    for inList in table:
        if maxLen == len(inList[1]):
            possible_results.append(inList[0])
            name.append(inList[1])
            a.append((inList[1], inList[0]))
    n = len(a)
    for i in range(n):
        for j in range(n-1-i):
            if a[j] < a[j+1]:
                a[j], a[j+1] = a[j+1], a[j]
    result = a[0][1]
    return result


# the question: Which customers has subscribed to the newsletter?
# return type: list of strings (where string is like email+separator+name, separator=";")


def get_subscribed_emails(table):
    result = []
    separator = ";"
    for inList in table:
        if inList[3] == "1":
            a = ''.join([inList[2], separator, inList[1]])
            result.append(a)
    return result
