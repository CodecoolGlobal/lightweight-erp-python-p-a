"""
This module creates reports for the marketing department.
This module can run independently from other modules.
Has no own data structure but uses other modules.
Avoud using the database (ie. .csv files) of other modules directly.
Use the functions of the modules instead.
"""

# importing everything you need
import ui
import common
from sales import sales
from crm import crm


def start_module():
    """
    Starts this module and displays its menu.
     * User can access default special features from here.
     * User can go back to main menu from here.

    Returns:
        None
    """
    list_options = ["Get last buyers name",
                    "Get last buyers ID",
                    "Get the name of the person, who spent the most and the amount he/she spent",
                    "Get the ID of the person, who spent the most and the amount he/she spent",
                    "Get the most frequent buyers name",
                    "Get the most frequent buyers ID"]

    ui.print_menu("Data Analyser Module menu:", list_options, "Exit program")
    while True:
        option = ui.get_inputs(["Please enter a number"], "")
        if option[0] == "1":
            result = get_the_last_buyer_name()
            ui.print_result(result, "The last buyers name")
        elif option[0] == "2":
            result = get_the_last_buyer_id()
            ui.print_result(result, "The last buyers ID")
        elif option[0] == "3":
            result = get_the_buyer_name_spent_most_and_the_money_spent()
            ui.print_result(result, "The buyers name, who spent the most money and the amount he/she spent")
        elif option[0] == "4":
            result = get_the_buyer_id_spent_most_and_the_money_spent()
            ui.print_result(result, "The buyers ID, who spent the most money and the amount he/she spent")
        elif option[0] == "5":
            result = get_the_most_frequent_buyers_names()
            ui.print_result(result, "The most frequent buyers name")
        elif option[0] == "6":
            result = get_the_most_frequent_buyers_ids()
            ui.print_result(result, "The most frequent buyers ID")
        elif option[0] == "0":
            exit()
        else:
            ui.print_error_message("No such an option!")


def get_the_last_buyer_name():
    """
    Returns the customer _name_ of the customer made sale last.

    Returns:
        str: Customer name of the last buyer
    """
    last_sale_id = sales.get_item_id_sold_last()
    last_buyer_id = sales.get_customer_id_by_sale_id(last_sale_id)
    last_buyer_name = crm.get_name_by_id(last_buyer_id)
    return last_buyer_name


def get_the_last_buyer_id():
    """
    Returns the customer _id_ of the customer made sale last.

    Returns:
        str: Customer id of the last buyer
    """
    last_sale_id = sales.get_item_id_sold_last()
    last_buyer_id = sales.get_customer_id_by_sale_id(last_sale_id)
    return last_buyer_id


def get_the_buyer_name_spent_most_and_the_money_spent():
    """
    Returns the customer's _name_ who spent the most in sum and the money (s)he spent.

    Returns:
        tuple: Tuple of customer name and the sum the customer spent eg.: ('Daniele Coach', 42)
    """
    names = sales.get_all_sales_ids_for_customer_ids()
    new_dict = {}
    for key, values in names.items():
        new_dict.update({crm.get_name_by_id(key): sales.get_the_sum_of_prices(values)})
    valami = []
    for key, values in new_dict.items():
        valami.append((key, values))
    result = valami[0]
    return result


def get_the_buyer_id_spent_most_and_the_money_spent():
    """
    Returns the customer's _id_ who spent more in sum and the money (s)he spent.

    Returns:
        tuple: Tuple of customer id and the sum the customer spent eg.: (aH34Jq#&, 42)
    """

    names = sales.get_all_sales_ids_for_customer_ids()
    new_dict = {}
    for key, values in names.items():
        new_dict.update({key: sales.get_the_sum_of_prices(values)})
    valami = []
    for key, values in new_dict.items():
        valami.append((key, values))
    result = valami[0]
    return result


def get_the_most_frequent_buyers_names(num=1):
    """
    Returns 'num' number of buyers (more precisely: the customer's name) who bought most frequently in an
    ordered list of tuples of customer names and the number of their sales.

    Args:
        num: the number of the customers to return.

    Returns:
        list of tuples: Ordered list of tuples of customer names and num of sales
            The first one bought the most frequent. eg.: [('Genoveva Dingess', 8), ('Missy Stoney', 3)]
    """

    names = sales.get_num_of_sales_per_customer_ids()
    new_dict = {}
    for key, values in names.items():
        new_dict.update({crm.get_name_by_id(key): values})
    new_list = list(new_dict.items())
    return new_list[:num]


def get_the_most_frequent_buyers_ids(num=1):
    """
    Returns 'num' number of buyers (more precisely: the customer ids of them) who bought more frequent in an
    ordered list of tuples of customer id and the number their sales.

    Args:
        num: the number of the customers to return.

    Returns:
        list of tuples: Ordered list of tuples of customer ids and num of sales
            The first one bought the most frequent. eg.: [(aH34Jq#&, 8), (bH34Jq#&, 3)]
    """

    names = sales.get_num_of_sales_per_customer_ids()
    new_dict = {}
    for key, values in names.items():
        new_dict.update({key: values})
    new_list = list(new_dict.items())
    return new_list[:num]
