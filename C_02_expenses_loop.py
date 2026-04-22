def not_blank(question):
    """Checks that a user response is not blank"""

    while True:
        response = input(question)

        if response != "":
            return response

        print("Please enter an answer.\n")

def int_check(question, low=1, high=255):
    """Checks users enter an integer between two values"""
    error = f"Please enter a valid number"
    while True:
        try:
            response = int(input(question))

            if low <= response <= high:
                return response
            else:
                print(error)
        except ValueError:
            print(error)

def get_expenses(exp_type):
    """Gets fixed expenses and outputs
    panda as a string and a subtotal of the expenses"""

    all_items = []

    while True:
        item_name = not_blank("Item Name: ")

        if (exp_type == "variable" and item_name == "xxx") and len (all_items) == 0:
            print("Enter at least one item ")
            continue
        elif item_name == "xxx":
            break

        all_items.append(item_name)

    return all_items

# print("Getting variable costs..")
# variable_expenses = get_expenses("variable")
# num_variable = len(variable_expenses)
# print(f"You entered {num_variable} items\n")

print("Getting fixed costs..")
fixed_expenses = get_expenses("fixed")
num_fixed = len(fixed_expenses)
print(f"You entered {num_fixed} items")


