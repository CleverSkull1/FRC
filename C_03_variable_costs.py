import pandas

def not_blank(question):
    """Checks that a user response is not blank"""

    while True:
        response = input(question)

        if response != "":
            return response

        print("Please enter an answer.\n")

def int_check(question, low=None, high=None, allow_enter=False):
    """Checks users enter an integer between two values"""
    error = f"Please enter a valid number"
    while True:
        try:
            response = input(question)

            if low <= int(response) <= high:
                return int(response)
            elif allow_enter == True and response == "":
                response = 10
                return int(response)
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

    amount = 1

    while True:
        item_name = not_blank("Item Name: ")

        if ((exp_type == "variable" and item_name == "xxx") and len(all_items) == 0) and len(all_items) == 0:
            print("Enter at least one item ")
            continue
        elif item_name == "xxx":
            break

        amount = int_check(f"Quantity <enter for {quantity}>: ", 1, 9999, True)

        if amount == "":
            amount = quantity

        cost = int_check("Price for one? ")

        all_items.append(item_name)
        all_amounts.append(amount)
        all_dollar_per_item.append(cost)

    expense_frame = pandas.DataFrame(expenses_dict)
    expense_frame['Cost'] = expense_frame['Amount'] * expense_frame['$ / Item']

    subtotal = expense_frame['Cost'].sum()

    return expense_frame, subtotal

quantity_made = int_check(f"Quantity made: ", 1, 9999)

print(f"\nGetting variable costs..")
variable_expenses = get_expenses("variable", quantity_made)
print()
variable_panda = variable_expenses[0]
variable_subtotal = variable_expenses[1]
print(variable_panda)
print(variable_subtotal)