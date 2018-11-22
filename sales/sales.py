""" Sales module

Data table structure:
    * id (string): Unique and random generated identifier
        at least 2 special characters (except: ';'), 2 number, 2 lower and 2 upper case letters)
    * title (string): Title of the game sold
    * price (number): The actual sale price in USD
    * month (number): Month of the sale
    * day (number): Day of the sale
    * year (number): Year of the sale
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

    table = data_manager.get_table_from_file("sales/sales.csv")
    table_title = ["id", "title", "price", "month", "day", "year"]

    list_options = ["Show table",
                    "Add product",
                    "Remove product",
                    "Update table",
                    "Get the item's ID with the lowest price",
                    "Get th number of items sold in a given range of years"]

    ui.print_menu("Sales module menu:", list_options, "Exit program")
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
            result = get_lowest_price_item_id(table)
            ui.print_result(result, "Printing the number of games by manufacturers")
        elif option[0] == "6":
            pass
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

    title_list = ["id", "title", "price", "month", "day", "year"]
    table = data_manager.get_table_from_file("sales/sales.csv")
    ui.print_table(table, title_list)


def add(table):
    """
    Asks user for input and adds it into the table.

    Args:
        table (list): table to add new record to

    Returns:
        list: Table with a new record
    """

    list_labels = ["title: ", "price: ", "month: ", "day: ", "year: "]
    wanna_stay = True
    while wanna_stay:
        new_product = ui.get_inputs(list_labels, "Please provide product information")
        new_product.insert(0, common.generate_random(table))
        table.append(new_product)
        next_step = ui.get_inputs([""], "Press 0 to save & exit or 1 to add another product.")[0]
        if next_step == "0":
            data_manager.write_table_to_file("sales/sales.csv", table)
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
            data_manager.write_table_to_file("sales/sales.csv", table)
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
                first_step = ui.get_inputs([""], "Please specify, what would you like to change at the given index? (title, price, month, day, year)")[0]
                if first_step == "title":
                    new_title = ui.get_inputs([""], "Please give a new title!")
                    v[1] = new_title[0]
                elif first_step == "price":
                    new_price = ui.get_inputs([""], "Please give a new price!")
                    v[2] = new_price[0]
                elif first_step == "month":
                    new_month = ui.get_inputs([""], "Please give a new month!")
                    v[3] = new_month[0]
                elif first_step == "day":
                    new_day = ui.get_inputs([""], "Please give a new day!")
                    v[4] = new_day[0]
                elif first_step == "year":
                    new_day = ui.get_inputs([""], "Please give a new year!")
                    v[5] = new_year[0]
                else:
                    ui.print_error_message("There's no such an option!")
            elif v[0] != id_ and current_iterates < max_iterates:
                current_iterates += 1
            else:
                ui.print_error_message("You can't add an item because of some reasons!")
        last_step = ui.get_inputs([""], "Press 0 to exit or 1 to update another item.")[0]
        if last_step == '0':
            data_manager.write_table_to_file("sales/sales.csv", table)
            wanna_stay = False
        else:
            id_ = ui.get_inputs(["Please type an ID to update the item at the given ID: "], "\n")[0]
            continue

    return table


# special functions:
# ------------------

def get_lowest_price_item_id(table):
    """
    Question: What is the id of the item that was sold for the lowest price?
    if there are more than one item at the lowest price, return the last item by alphabetical order of the title

    Args:
        table (list): data table to work on

    Returns:
         string: id
    """

    pList = []
    for inList in table:
        pList.append(int(inList[2]))
    maxPrice = 110
    for num in pList:
        if num < maxPrice:
            maxPrice = num
    strPrice = str(maxPrice)
    for inList in table:
        if strPrice in inList[2]:
            result = inList[0]
    return result


def get_items_sold_between(table, month_from, day_from, year_from, month_to, day_to, year_to):
    """
    Question: Which items are sold between two given dates? (from_date < sale_date < to_date)

    Args:
        table (list): data table to work on
        month_from (int)
        day_from (int)
        year_from (int)
        month_to (int)
        day_to (int)
        year_to (int)

    Returns:
        list: list of lists (the filtered table)
    """

    # your code
