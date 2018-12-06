""" Inventory module

Data table structure:
    * id (string): Unique and random generated identifier
        at least 2 special characters (except: ';'), 2 number, 2 lower and 2 upper case letters)
    * name (string): Name of item
    * manufacturer (string)
    * purchase_year (number): Year of purchase
    * durability (number): Years it can be used
"""

# everything you'll need is imported:
# User interface module
import ui
# data manager module
import data_manager
# common module
import common
import datetime

def start_module():
    """
    Starts this module and displays its menu.
     * User can access default special features from here.
     * User can go back to main menu from here.

    Returns:
        None
    """

    table = data_manager.get_table_from_file("inventory/inventory.csv")
    table_title = ["id", "name", "manufacturer", "purchase_year", "durability"]

    list_options = ["Show table",
                    "Add item",
                    "Remove item",
                    "Update table",
                    "Get every not expired product",
                    "Get th average durability time for each manufacturer"]

    ui.print_menu("Inventory module menu:", list_options, "Exit program")
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
            pass
        elif option[0] == "6":
            result = get_average_durability_by_manufacturers(table)
            ui.print_result(result, "Printing the average durability by manufacturers")
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

    title_list = ["id", "name", "manufacturer", "purchase_year", "durability"]
    table = data_manager.get_table_from_file("inventory/inventory.csv")
    ui.print_table(table, title_list)


def add(table):
    """
    Asks user for input and adds it into the table.

    Args:
        table (list): table to add new record to

    Returns:
        list: Table with a new record
    """

    list_labels = ["name: ", "manufacturer: ", "purchase_year: ", "durability: "]
    wanna_stay = True
    while wanna_stay:
        new_product = ui.get_inputs(list_labels, "Please provide new information")
        new_product.insert(0, common.generate_random(table))
        table.append(new_product)
        next_step = ui.get_inputs([""], "Press 0 to save & exit or 1 to add another information.")[0]
        if next_step == "0":
            data_manager.write_table_to_file("inventory/inventory.csv", table)
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
        next_step = ui.get_inputs([""], "Press 0 to exit or 1 to remove another item.")[0]
        if next_step == '0':
            data_manager.write_table_to_file("inventory/inventory.csv", table)
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
                first_step = ui.get_inputs([""], "Please specify, what would you like to change at the given index? (name, manufacturer, purchase_year, durability)")[0]
                if first_step == "name":
                    new_name = ui.get_inputs([""], "Please give a new name!")
                    v[1] = new_name[0]
                elif first_step == "manufacturer":
                    new_manufacturer = ui.get_inputs([""], "Please give a new manufacturer!")
                    v[2] = new_manufacturer[0]
                elif first_step == "purchase_year":
                    new_purchase_year = ui.get_inputs([""], "Please give a new purchase year!")
                    v[3] = new_purchase_year[0]
                elif first_step == "durability":
                    new_durability = ui.get_inputs([""], "Please give a new durability year!")
                    v[4] = new_durability[0]
                else:
                    ui.print_error_message("There's no such an option!")
            elif v[0] != id_ and current_iterates < max_iterates:
                current_iterates += 1
            else:
                ui.print_error_message("You can't add an item because of some reasons!")
        last_step = ui.get_inputs([""], "Press 0 to exit or 1 to update another item.")[0]
        if last_step == '0':
            data_manager.write_table_to_file("inventory/inventory.csv", table)
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
        my_dict.setdefault(t[2], []).append(t[4:5])
    return my_dict


def get_available_items(table):
    """
    Question: Which items have not exceeded their durability yet?

    Args:
        table (list): data table to work on

    Returns:
        list: list of lists (the inner list contains the whole row with their actual data types)
    """

    avList = []
    everything = []
    result = []
    now = datetime.datetime.now()
    for inList in table:
        if int(inList[3]) + int(inList[4]) > now.year:
            avList.extend(inList)
            everything.extend(inList)
    result.append(avList)
    result.append(everything)
    return result


def get_add(list):
    sum = 0 
    for items in list:
        sum += items
    return sum


def get_average_durability_by_manufacturers(table):
    """
    Question: What are the average durability times for each manufacturer?

    Args:
        table (list): data table to work on

    Returns:
        dict: a dictionary with this structure: { [manufacturer] : [avg] }
    """
    new_dict = {}
    for line in table:
        new_dict.setdefault(line[2], []).append(int(line[4]))
    result = {key: get_add(values)/len(values) for key, values in new_dict.items()}
    return result
