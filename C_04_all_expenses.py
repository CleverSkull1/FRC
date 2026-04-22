import pandas
from tabulate import tabulate

def not_blank(question):
    """Checks that a user response is not blank"""

    while True:
        response = input(question)

        if response != "":
            return response

        print("Please enter an answer.\n")

def int_check(question, low=0, high=9999, allow_enter=False):
    """Checks users enter an integer between two values"""
    error = f"Please enter a valid number"
    while True:
        try:
            response = input(question)

            if low <= int(response) <= high:
                return int(response)
            elif allow_enter == True and response == "":
                response = 10
                return response
            elif response == "xxx":
                break
            else:
                print(error)
        except ValueError:
            print(error)

def get_expenses(exp_type, quantity=10):
    """Gets fixed expenses and outputs
    panda as a string and a subtotal of the expenses"""

    all_items = []
    all_amounts = []
    all_dollar_per_item = []

    expenses_dict = {
        "Item": all_items,
        "Amount": all_amounts,
        "Cost": all_dollar_per_item
    }

    amount = quantity
    how_much_question = "How much? $"

    while True:
        item_name = not_blank("Item Name: ")

        if ((exp_type == "variable" and item_name == "xxx") and len(all_items) == 0) and len(all_items) == 0:
            print("Enter at least one item ")
            continue
        elif item_name == "xxx":
            break

        if exp_type == "variable":
            amount = int_check(f"Quantity <enter for 10>: ", 1, 9999, True)

            if amount == "":
                amount = quantity

            how_much_question = int_check("Price for one? ")

        cost = how_much_question

        all_items.append(item_name)
        all_amounts.append(amount)
        all_dollar_per_item.append(cost)

    expense_frame = pandas.DataFrame(expenses_dict)
    expense_frame['Cost'] = expense_frame['Amount'] * expense_frame['$ / Item']
    subtotal = expense_frame['Cost'].sum()

    add_dollars = ['Amount', "$ / Item", "Cost"]
    for var_item in add_dollars:
        expense_frame[var_item] = expense_frame[var_item].apply(currency)

    if exp_type == "variable":
        expense_string = tabulate(expense_frame, headers='keys',
                                  tablefmt='psql', showindex=False)
    else:
        expense_string = tabulate(expense_frame[['Item', 'Cost']], headers='keys',
                                  tablefmt='psql', showindex=False)

    return expense_string, subtotal

def currency(a):
    return "${:.2f}".format(a)

quantity_made = int_check(f"Quantity made: ", 1)

print(f"\nGetting variable costs..")
variable_expenses = get_expenses("variable", quantity_made)
variable_panda = variable_expenses[0]
variable_subtotal = variable_expenses[1]

print("\nGetting fixed costs..")
fixed_expenses = get_expenses("fixed")
fixed_panda = fixed_expenses[0]
fixed_subtotal = fixed_expenses[1]

print(f"\n=== Variable Expenses ===\n{variable_panda}")
print(f"Variable Subtotal: ${variable_subtotal:.2f}\n")

print(f"=== Fixed Expenses ===\n{fixed_panda}")
print(f"Fixed Subtotal: ${fixed_subtotal:.2f}\n")

total_expenses = variable_subtotal + fixed_subtotal
print(f"Total Expenses: ${total_expenses:.2f}")
