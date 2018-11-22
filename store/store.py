""" Store module

Data table structure:
    * id (string): Unique and random generated identifier
        at least 2 special characters (except: ';'), 2 number, 2 lower and 2 upper case letters)
    * title (string): Title of the game
    * manufacturer (string)
    * price (number): Price in dollars
    * in_stock (number)
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
    table = data_manager.get_table_from_file("store/games.csv")
    table_title = ["id", "title", "manufacturer", "price", "in_stock"]

    list_options = ["Show table",
                    "Add product",
                    "Remove product",
                    "Update table",
                    "Get counts by manufacturers",
                    "Get average by manufacturer"]

    ui.print_menu("Store module menu:", list_options, "Exit program")
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
            result = get_counts_by_manufacturers(table)
            ui.print_result(result, "Printing the number of games by manufacturers")
        elif option[0] == "6":
            result = get_average_by_manufacturer(table, "Ensemble Studios")
            ui.print_result(result, "Printing the number of games by manufacturers")
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
    title_list = ["id", "title", "manufacturer", "price", "in_stock"]
    table = data_manager.get_table_from_file("store/games.csv")
    ui.print_table(table, title_list)


def add(table):
    """
    Asks user for input and adds it into the table.

    Args:
        table (list): table to add new record to

    Returns:
        list: Table with a new record
    """
    list_labels = ["title: ", "manufacturer: ", "price: ", "in_stock: "]
    wanna_stay = True
    while wanna_stay:
        new_product = ui.get_inputs(list_labels, "Please provide product information")
        new_product.insert(0, common.generate_random(table))
        table.append(new_product)
        next_step = ui.get_inputs([""], "Press 0 to save & exit or 1 to add another product.")[0]
        if next_step == "0":
            data_manager.write_table_to_file("store/games.csv", table)
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

    # your code
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
            data_manager.write_table_to_file("store/games.csv", table)
            wanna_stay = False
        else:
            id_ = ui.get_inputs(["Please type ID to remove: "], "\n")[0]
            continue
    return table


def update(table, id_):
    """
    Updates specified record in the table. Ask users for new data.

    Args:
        table: list in which record should be updated
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
                first_step = ui.get_inputs([""], "Please specify, what would you like to change at the given index? (title, manufacturer, price, stock)")[0]
                if first_step == "title":
                    new_title = ui.get_inputs([""], "Please give a new title!")
                    v[1] = new_title[0]
                elif first_step == "manufacturer":
                    new_manufacturer = ui.get_inputs([""], "Please give a new manufacturer!")
                    v[2] = new_manufacturer[0]
                elif first_step == "price":
                    new_price = ui.get_inputs([""], "Please give a new price!")
                    v[3] = new_price[0]
                elif first_step == "stock":
                    new_stock = ui.get_inputs([""], "Please give a new stock!")
                    v[4] = new_stock[0]
                else:
                    ui.print_error_message("There's no such an option!")
            elif v[0] != id_ and current_iterates < max_iterates:
                current_iterates += 1
            else:
                ui.print_error_message("You can't add an item because of some reasons!")
        last_step = ui.get_inputs([""], "Press 0 to exit or 1 to update another item.")[0]
        if last_step == '0':
            data_manager.write_table_to_file("store/games.csv", table)
            wanna_stay = False
        else:
            id_ = ui.get_inputs(["Please type an ID to update the item at the given ID: "], "\n")[0]
            continue

    return table


# special functions:
# ------------------


def create_dict(table):
    my_dict = {}
    for t in table:
        my_dict.setdefault(t[2], []).append(t[1:3])
    return my_dict


def get_counts_by_manufacturers(table):
    """
    Question: How many different kinds of game are available of each manufacturer?

    Args:
        table (list): data table to work on

    Returns:
         dict: A dictionary with this structure: { [manufacturer] : [count] }
    """
    table_dict = create_dict(table)
    new_dict = {}
    for k in table_dict:
        new_dict[k] = len(table_dict[k])
    return new_dict


def get_average_by_manufacturer(table, manufacturer):
    """
    Question: What is the average amount of games in stock of a given manufacturer?

    Args:
        table (list): data table to work on
        manufacturer (str): Name of manufacturer

    Returns:
         number
    """
    sList = []
    for inList in table:
        if inList[2] == manufacturer:
            sList.append(inList[4])
    sumStore = 0
    for i in range(0, len(sList)):
        sumStore += int(sList[i])
    return sumStore/len(sList)
