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

while True:
    product_name = not_blank("Name?")
    quality_made = int_check("Quality being made: ")
    print(f"You are making {quality_made} {product_name}\n")

