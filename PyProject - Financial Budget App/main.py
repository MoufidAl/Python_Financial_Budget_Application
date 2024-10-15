import pandas as pd
import csv
from datetime import datetime
from PyProject.data_entry import get_user_amount,get_user_cat,get_user_date,get_user_desc
import matplotlib.pyplot as plt

class CSV:
    CSV_FILE = "Personal_Budgeting_Data.csv" # Class Variable
    cols = ['date','amount','category','description']
    date_format = "%m-%d-%Y"
    
    # Initializing the file, this will create it if it does not exist.
    @classmethod # The classmethod will allow the below function to access class variables.
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.cols)
            df.to_csv(cls.CSV_FILE, index=False)
    
    @classmethod
    def add_entry(cls,date,amount,category,description):
        new_entry = {
            "date":date,
            "amount":amount,
            "category":category,
            "description":description
        }
        with open(cls.CSV_FILE, "a",newline="") as csvfile:
            writer = csv.DictWriter(cls.CSV_FILE,fieldnames=cls.cols) #writing into csv file in a dict format.
            writer.writerow(new_entry)
        print('Entry Added!')

    @classmethod
    def view_transactions(cls,start_date,end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df['date'] = pd.to_datetime(df['date'], format = CSV.date_format)
        start_date = datetime.strptime(start_date,CSV.date_format)
        end_date = datetime.strptime(end_date,CSV.date_format)

        # Create a mask for the filtering of the datetime objects in the date column
        mask = (df['date'] >= start_date) & (df['date'] <= end_date)
        filtered_df = df.loc[mask]

        # Showing Results
        if filtered_df.empty:
            print('No Data found in the specified date range')
        else:
            print(f"Transaction between {start_date.strftime(CSV.date_format)} to {end_date.strftime(CSV.date_format)} are below:")
            print(filtered_df.to_string(index=False, formatters={'date': lambda row: row.strftime(CSV.date_format)}))
        # Showing Total Income and Total Expenses
        total_income = filtered_df[filtered_df['category'] == 'Income']['amount'].sum()
        total_expenses = filtered_df[filtered_df['category'] == 'Expense']['amount'].sum()

        print("\nSummary:")
        print(f"Total Income: ${total_income:.2f}") # :.2f formats the results into a decimal rounded to 2 decimal places.
        print(f"Total Expenses: ${total_expenses:.2f}")
        print(f"Net Amount: ${(total_income - total_expenses):.2f}")


def add_data():
    CSV.initialize_csv()
    date = get_user_date("Enter Date of Transaction: ", allow_default=True)
    amount = get_user_amount()
    category = get_user_cat()
    description = get_user_desc()
    CSV.add_entry(date,amount,category,description)

def plot_it(df):
    df.set_index('date', inplace=True) # For plotting purposes we need to have the date be the index in the frame to base the graph on.
    # In order to plot it correctly, we need to make sure that the values in each of the dfs is continuous...
    # This means that we need to fill in days where no transactions took place with a value (0) so that we get a line graph correctly
    income_df = df[df['category']=='Income'].resample("D").sum().reindex(df.index, fill_value=0)
    expense_df = df[df['category'] == 'Expense'].resample("D").sum().reindex(df.index, fill_value=0)

    plt.figure(figsize=(10,5))
    plt.plot(income_df.index,income_df['amount'],label='Income',color='g')
    plt.plot(expense_df.index,expense_df['amount'], label='Expenses', color='r')
    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.title('Income and Expenses over Time')
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    while True:
        print("\n1. Add a new transaction")
        print("2.View transactions & a summary withina  date range")
        print("3. Exit Application")

        user_choice = input("Please enter would you like to do (1-3): ")
        if user_choice == '1':
            add_data()
        elif user_choice == '2':
            start_date = get_user_date("Enter Start date (mm-dd-yyyy): ")
            end_date = get_user_date("Enter End date (mm-dd-yyyy): ")
            df = CSV.view_transactions(start_date,end_date)
            if input("Do you want to see this data plotted? y/n: ").lower() == 'y':
                plot_it(df)
        elif user_choice == '3':
            print('Exiting Application...')
            break
        else:
            print('Invalid Choice, please enter 1, 2, or 3')

if __name__ == "__main__":
    main()