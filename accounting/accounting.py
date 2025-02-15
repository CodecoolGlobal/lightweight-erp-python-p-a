""" Accounting module

Data table structure:
    * id (string): Unique and random generated identifier
        at least 2 special characters (except: ';'), 2 number, 2 lower and 2 upper case letters)
    * month (number): Month of the transaction
    * day (number): Day of the transaction
    * year (number): Year of the transaction
    * type (string): in = income, out = outflow
    * amount (int): amount of transaction in USD
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

    table = data_manager.get_table_from_file("accounting/items.csv")
    table_title = ["id", "month", "day", "year", "type", "amount"]

    list_options = ["Show table",
                    "Add product",
                    "Remove product",
                    "Update table",
                    "Get the most profitable year",
                    "Get th average profit of a year (per item)"]

    ui.print_menu("Accounting module menu:", list_options, "Exit program")
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
            result = which_year_max(table)
            ui.print_result(result, "Which year had the highest profit?")
        elif option[0] == "6":
            year = ui.get_inputs(["Year: "], "Please give a year to search for! ")[0]
            result = avg_amount(table, year)
            ui.print_result(result, "Printing the average profit for each item in a given year")
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

    title_list = ["id", "month", "day", "year", "type", "amount"]
    table = data_manager.get_table_from_file("accounting/items.csv")
    ui.print_table(table, title_list)


def add(table):
    """
    Asks user for input and adds it into the table.

    Args:
        table (list): table to add new record to

    Returns:
        list: Table with a new record
    """

    list_labels = ["month: ", "day: ", "year: ", "type: ", "amount: "]
    wanna_stay = True
    while wanna_stay:
        new_product = ui.get_inputs(list_labels, "Please provide item information")
        new_product.insert(0, common.generate_random(table))
        table.append(new_product)
        next_step = ui.get_inputs([""], "Press 0 to save & exit or 1 to add another item.")[0]
        if next_step == "0":
            data_manager.write_table_to_file("accounting/items.csv", table)
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
        next_step = ui.get_inputs([""], "Press 0 to exit or 1 to remove another product.")[0]
        if next_step == '0':
            data_manager.write_table_to_file("accounting/items.csv", table)
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
                first_step = ui.get_inputs([""], "Please specify, what would you like to change at the given index? (month, day, year, type, amount)")[0]
                if first_step == "month":
                    new_month = ui.get_inputs([""], "Please give a new month!")
                    v[1] = new_month[0]
                elif first_step == "day":
                    new_day = ui.get_inputs([""], "Please give a new day!")
                    v[2] = new_day[0]
                elif first_step == "year":
                    new_year = ui.get_inputs([""], "Please give a new year!")
                    v[3] = new_year[0]
                elif first_step == "type":
                    new_type = ui.get_inputs([""], "Please give a new type!")
                    v[4] = new_type[0]
                elif first_step == "amount":
                    new_amount = ui.get_inputs([""], "Please give a new amount!")
                    v[5] = new_amount[0]
                else:
                    ui.print_error_message("There's no such an option!")
            elif v[0] != id_ and current_iterates < max_iterates:
                current_iterates += 1
            else:
                ui.print_error_message("You can't add an item because of some reasons!")
        last_step = ui.get_inputs([""], "Press 0 to exit or 1 to update another item.")[0]
        if last_step == '0':
            data_manager.write_table_to_file("accounting/items.csv", table)
            wanna_stay = False
        else:
            id_ = ui.get_inputs(["Please type an ID to update the item at the given ID: "], "\n")[0]
            continue

    return table


# special functions:
# ------------------

def which_year_max(table):
    pList = []
    for inList in table:
        if inList[4] == "in":
            pList.append(inList[5])
    maxProfit = pList[0]
    for num in pList:
        if num > maxProfit:
            maxProfit = num
    for inList in table:
        if inList[5] == maxProfit:
            result = int(inList[3])
            return result


def avg_amount(table, year):
    stringYear = str(year)
    yList = []
    iList = []
    oList = []
    for inList in table:
        if stringYear in inList[3]:
            yList.append(inList)
    for inList in yList:
        if inList[4] == "in":
            inList[5] = int(inList[5])
            iList.append(inList[5])
        else:
            inList[5] = int(inList[5])
            oList.append(inList[5])
    sumIncome = 0
    for i in range(0, len(iList)):
        sumIncome += iList[i]
    sumOutcome = 0
    for i in range(0, len(oList)):
        sumOutcome += oList[i]
    result = (sumIncome-sumOutcome)/len(yList)
    return result
