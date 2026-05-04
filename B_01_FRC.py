import pandas
from tabulate import tabulate
from datetime import date
import math

# functions
def statement_generator(statement, decoration, amount=3):
    """Emphasises headings by adding decoration at the start and end"""
    return f"{decoration * amount} {statement} {decoration * amount}\n"

def yes_no_check(question):
    """Checks that users enter yes / no / y / n"""

    while True:

        response = input(question).lower()

        if response == "y" or response == "yes":
            return "yes"
        elif response == "n" or response == "no":
            return "no"

        print(f"Please answer yes / no (y / n)")

def instructions():
    """Displays instructions"""
    print(statement_generator("Instructions", "ℹ️"))

    print('''This program will ask you for... 
    - The name of the product you are selling 
    - How many items you plan on selling 
    - The costs for each component of the product 
      (variable expenses)
    - Whether or not you have fixed expenses (if you have 
      fixed expenses, it will ask you what they are).
    - How much money you want to make (ie: your profit goal)

It will also ask you how much the recommended sales price should 
be rounded to.

The program outputs an itemised list of the variable and fixed 
expenses (which includes the subtotals for these expenses). 

Finally it will tell you how much you should sell each item for 
to reach your profit goal. 

The data will also be written to a text file which has the 
same name as your product and today's date.

    ''')

def not_blank(question):
    """Checks user response is not blank"""
    while True:
        response = input(question)

        if response != "":
            return response
        else:
            print("Please enter a response.")

def num_check(question, num_type="float", exit_code=None):
    """Checks that response is a float / integer more than zero"""

    if num_type == "float":
        error = "Please enter a number greater than 0."
    else:
        error = "Please enter an integer greater than 0."

    while True:
        response = input(question)

        if response == exit_code:
            return response
        try:

            if num_type == "float":
                response = float(response)
            else:
                response = int(response)

            if response > 0:
                return response
            else:
                print(error)

        except ValueError:
            print(error)

def get_expenses(exp_type, how_many=1):
    """Gets variable / fixed expenses and outputs
    panda (as a string) and a subtotal of the expenses"""

    all_items = []
    all_amounts = []
    all_dollar_per_item = []

    expenses_dict = {
        "Item": all_items,
        "Amount": all_amounts,
        "$ / Item": all_dollar_per_item
    }
    amount = how_many
    how_much_question = "How much? $"

    while True:
        item_name = not_blank("Item Name: ")

        if exp_type == "variable" and item_name == "xxx" and len(all_items) == 0:
            print("Please enter at least one item.")
            continue

        elif item_name == "xxx":
            break

        if exp_type == "variable":

            amount = num_check(f"How many <enter for {how_many}>: ",
                               "integer", "")

            if amount == "":
                amount = how_many

            how_much_question = "Price for one? $"

        price_for_one = num_check(how_much_question, "float")
        print()

        all_items.append(item_name)
        all_amounts.append(amount)
        all_dollar_per_item.append(price_for_one)

    expense_frame = pandas.DataFrame(expenses_dict)

    expense_frame['Cost'] = expense_frame['Amount'] * expense_frame['$ / Item']

    subtotal = expense_frame['Cost'].sum()


    add_dollars = ['Amount', '$ / Item', 'Cost']
    for var_item in add_dollars:
        expense_frame[var_item] = expense_frame[var_item].apply(currency)

    if exp_type == "variable":
        expense_string = tabulate(expense_frame, headers='keys',
                                  tablefmt='psql', showindex=False)
    else:
        expense_string = tabulate(expense_frame[['Item', 'Cost']], headers='keys',
                                  tablefmt='psql', showindex=False)
    return expense_string, subtotal

def currency(x):
    """Formats numbers as currency ($#.##)"""
    return "${:.2f}".format(x)

def profit_goal(total_costs):
    """Calculates profit goal  work out profit goal and total sales required"""
    error = "Please enter a valid profit goal\n"

    valid = False
    while not valid:
        response = input("What is your profit goal (eg $500 or 50%): ")

        if response[0] == "$":
            profit_type = "$"
            amount = response[1:]
        elif response[-1] == "%":
            profit_type = "%"
            amount = response[:-1]
        else:
            profit_type = "unknown"
            amount = response
        try:
            amount = float(amount)
            if amount <= 0:
                print(error)
                continue
        except ValueError:
            print(error)
            continue

        if profit_type == "unknown" and amount >= 100:
            dollar_type = yes_no_check(f"Do you mean ${amount:.2f}.  ie {amount:.2f} dollars? , y / n: ")

            if dollar_type == "yes":
                profit_type = "$"
            else:
                profit_type = "%"
        elif profit_type == "unknown" and amount < 100:
            percent_type = yes_no_check(f"Do you mean {amount:.0f}%? , y / n: ")
            if percent_type == "yes":
                profit_type = "%"
            else:
                profit_type = "$"

        if profit_type == "$":
            return amount
        else:
            goal = (amount / 100) * total_costs
            return goal

def round_up(amount, round_val):
    """Rounds amount to desired hole number"""
    return int(math.ceil(amount / round_val)) * round_val

# main routine

fixed_subtotal = 0
fixed_panda_string = ""

print(statement_generator("Fundraising Calculator", "💰"))
want_instructions = yes_no_check("\nShow instructions? ")
print()

if want_instructions == "yes":
    instructions()


product_name = not_blank("\nProduct Name: ")
quantity_made = num_check("Quantity being made: ", "integer")

print("Getting variable expenses....")
variable_expenses = get_expenses("variable", quantity_made)

variable_panda_string = variable_expenses[0]
variable_subtotal = variable_expenses[1]

has_fixed = yes_no_check("\nDo you have fixed expenses? ")

if has_fixed == "yes":
    fixed_expenses = get_expenses("fixed")

    fixed_panda_string = fixed_expenses[0]
    fixed_subtotal = fixed_expenses[1]

    if fixed_subtotal == 0:
        has_fixed = "no"
        fixed_panda_string = ""

total_expenses = variable_subtotal + fixed_subtotal
total_expenses_string = f"Total Expenses: ${total_expenses:.2f}"

target = profit_goal(total_expenses)
sales_target = total_expenses + target

selling_price = (total_expenses + target) / quantity_made
round_to = num_check("Round To: ", 'integer')
suggested_price = round_up(selling_price, round_to)

today = date.today()
day = today.strftime("%d")
month = today.strftime("%m")
year = today.strftime("%Y")
hour = today.strftime("%H")
minute = today.strftime("%M")
second = today.strftime("%S")

main_heading_string = statement_generator(f"Fundraising Calculator "
                                     f"({product_name}, {day}/{month}/{year})", "=")
quantity_string = f"Quantity being made: {quantity_made}"
variable_heading_string = statement_generator("Variable Expenses", "-")
variable_subtotal_string = f"Variable Expenses Subtotal: ${variable_subtotal:.2f}"

if has_fixed == "yes":
    fixed_heading_string = statement_generator("Fixed Expenses", "-")
    fixed_subtotal_string = f"Fixed Expenses Subtotal: {fixed_subtotal:.2f}"
else:
    fixed_heading_string = statement_generator("You have no Fixed Expenses", "-")
    fixed_subtotal_string = "Fixed Expenses Subtotal: $0.00"

selling_price_heading = statement_generator("Selling Price Calculations", "-")
profit_goal_string = f"Profit Goal: ${target:.2f}"
sales_target_string = f"\nTotal Sales Needed: ${sales_target:.2f}"

minimum_price_string = f"Minimum Selling Price: ${selling_price:.2f}"
suggested_price_string = statement_generator(f"Suggested Selling Price: "
                                        f"${suggested_price:.2f}", "*")

to_write = [main_heading_string, quantity_string,
            "\n", variable_heading_string, variable_panda_string,
            variable_subtotal_string,
            "\n", fixed_heading_string, fixed_panda_string,
            fixed_subtotal_string, "\n",
            selling_price_heading, total_expenses_string,
            profit_goal_string, sales_target_string,
            minimum_price_string, "\n", suggested_price_string]
print()
for item in to_write:
    print(item)

file_name = f"F_{input('Enter file name: ')}_{day}-{month}-{year}_{hour}-{minute}-{second}"
write_to = "{}.txt".format(file_name)

text_file = open(write_to, "w+")
for item in to_write:
    text_file.write(item)
    text_file.write("\n")