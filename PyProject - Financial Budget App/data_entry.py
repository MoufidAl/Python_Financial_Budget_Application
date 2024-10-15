from datetime import datetime

date_format = "%m-%d-%Y"
categories = {'I':'Income', 'E':'Expense'}

def get_user_date(prompt, allow_default=False):
    date_str = input(prompt)
    if allow_default and not date_str:
        return datetime.today().strftime(date_format)
    try:
        valid_date = datetime.strptime(date_str,date_format)
        return valid_date.strftime(date_format)
    except ValueError:
        print("Invalid date, enter in 'mm-dd-yyyy' format")
        return get_user_date(prompt, allow_default) # Recursive function - can't proceed without entering a valid date.

def get_user_amount():
    try:
        amount = float(input("Enter Amount: "))
        if amount <= 0:
            raise ValueError("Amount must be above zero")
        return amount
    except ValueError as e:
        print(e)
        return get_user_amount()

def get_user_cat():
    try:
        cat = str(input("Please specify whether this is an Income or Expense using 'I' or 'E': "))
        if cat in categories:
            return categories[cat]
    except ValueError as e:
        print(e)
        return get_user_cat()

def get_user_desc():
    return input("Enter a description (optional): ")