import argparse
import os
import csv
from datetime import datetime

expenses_database = "expenses_database.csv"
if not os.path.exists(expenses_database):
    headers = ["id", "date", "description", "amount", "category"]
    with open(expenses_database, "w", newline='') as db:
        writer = csv.writer(db)
        writer.writerow(headers)

def add_expense(args):
    with open(expenses_database, "r") as db:
        reader = csv.reader(db)
        next(reader, None) # Skip first row
        expenses_data = [row for row in reader]
    expense_ids = [row[0] for row in expenses_data]
    current_month_expenses = [row[3] for row in expenses_data if row[1].split("-")[1][-1] == str(datetime.now().month)[-1]]
    current_month_spend = sum([int(expense) for expense in current_month_expenses])

    with open("budget.txt", "r", newline="") as b:
        reader = csv.reader(b)
        next(reader, None) # Skip first row
        expenses_data = [row for row in reader]
    current_budget = [row[1] for row in expenses_data if row[0] == str(datetime.now().month)[-1]]
    current_budget = int(current_budget[0])

    expense_id = 1
    while str(expense_id) in expense_ids:
        expense_id += 1
    expense_row = [expense_id, args.date, args.description, args.amount, args.category]
    with open(expenses_database, "a", newline='') as db:
        writer = csv.writer(db)
        writer.writerow(expense_row)
    print(f"Expense added successfully (ID: {expense_id})")

    if current_budget < current_month_spend:
        print(f"You have spent ${current_month_spend + args.amount} this month. You are ${current_month_spend - current_budget} over this month's budget.")
    elif current_month_spend < current_budget:
        print(f"You have spent ${current_month_spend + args.amount} this month. ${current_budget - current_month_spend} left in this month's budget.")
    elif current_month_spend == current_budget:
        print(f"You have spent ${current_month_spend + args.amount} this month. You have reached your budget.")

def update_expense(args):
    expenses_db_content = csv.reader(open(expenses_database))
    lines = list(expenses_db_content)
    with open("budget.txt", "r", newline="") as b:
        reader = csv.reader(b)
        next(reader, None) # Skip first row
        expenses_data = [row for row in reader]
    current_budget = [row[1] for row in expenses_data if row[0] == str(datetime.now().month)[-1]]
    current_budget = int(current_budget[0])

    for line in lines:
        if line[0] == args.id:
            old_amount = line[3]
            old_description = line[2]
            old_date = line[1]
            old_category = line[4]

    if args.newamount:
        for line in lines:
            if line[0] == args.id:
                line[3] = args.newamount
        print(f"'{old_description}' (ID: {args.id}) amount update from ${old_amount} to ${args.newamount}")
    if args.newdescription:
        for line in lines:
            if line[0] == args.id:
                line[2] = args.newdescription
        print(f"'{old_description}' (ID: {args.id}) description updated to '{args.newdescription}'")
    if args.newdate:
        for line in lines:
            if line[0] == args.id:
                line[1] = args.newdate
        print(f"'{old_description}' (ID: {args.id}) date updated from {old_date} to {args.newdate}")
    if args.newcategory:
        for line in lines:
            if line[0] == args.id:
                if line[4] == "":
                    line[4] = args.newcategory
                    print(f"'{old_description}' (ID: {args.id}) category update to {args.newcategory}")
                else:
                    line[4] = args.newcategory
                    print(f"'{old_description}' (ID: {args.id}) category updated from {old_category} to {args.newcategory}")

    current_month_expenses = [row[3] for row in lines[1:] if row[1].split("-")[1][-1] == str(datetime.now().month)[-1]] 
    current_month_spend = sum([int(expense) for expense in current_month_expenses])

    if current_budget < current_month_spend:
        print(f"You have spent ${current_month_spend} this month. You are ${current_month_spend - current_budget} over this month's budget.")
    elif current_month_spend < current_budget:
        print(f"You have spent ${current_month_spend} this month. ${current_budget - current_month_spend} left in this month's budget.")
    elif current_month_spend == current_budget:
        print(f"You have spent ${current_month_spend} this month. You have reached your budget.")

    with open(expenses_database, "w", newline="") as db:
        writer = csv.writer(db)
        writer.writerows(lines)
    

def delete_expense(args):
    expenses_db_content = csv.reader(open(expenses_database))
    lines = list(expenses_db_content)
    for location, line in enumerate(lines):
        if line[0] == str(args.id):
            print(f"You deleted '{lines[location][2]}' (ID: {lines[location][0]})")
            del lines[location]
    with open(expenses_database, "w", newline="") as db:
        writer = csv.writer(db)
        writer.writerows(lines)

    current_month_expenses = [row[3] for row in lines[1:] if row[1].split("-")[1][-1] == str(datetime.now().month)[-1]] 
    current_month_spend = sum([int(expense) for expense in current_month_expenses])
    with open("budget.txt", "r", newline="") as b:
        reader = csv.reader(b)
        next(reader, None) # Skip first row
        expenses_data = [row for row in reader]

    current_budget = [row[1] for row in expenses_data if row[0] == str(datetime.now().month)[-1]]
    current_budget = int(current_budget[0])
    if current_budget < current_month_spend:
        print(f"You have spent ${current_month_spend} this month. You are ${current_month_spend - current_budget} over this month's budget.")
    elif current_month_spend < current_budget:
        print(f"You have spent ${current_month_spend} this month. ${current_budget - current_month_spend} left in this month's budget.")
    elif current_month_spend == current_budget:
        print(f"You have spent ${current_month_spend} this month. You have reached your budget.")

def list_expenses(args):
    if args.monthfilter != None and args.monthfilter > 12:
        print("This is not a valid month.")
    else:
        expenses_db_content = csv.reader(open(expenses_database))
        lines = [line for line in expenses_db_content]
        if len(lines) == 1:
            print("There are no expenses.")
        if args.monthfilter != None:
            header = lines[0]
            lines = [line for line in lines[1:] if int(str(line[1]).split("-")[1]) == args.monthfilter]
            lines.insert(0, header)
        if args.categoryfilter != None:
            header = lines[0]
            lines = [line for line in lines[1:] if line[4] == args.categoryfilter]
            lines.insert(0, header)
        if len(lines) == 1:
            print("There are no expenses matching these filters.")
        else:
            max_length = [max(len(item[i]) for item in lines) for i in range(4)]
            item_lengths = [[len(item) for item in line] for line in lines]
            spaces_to_add = [[a - b for a, b in zip(max_length, item_length)] for item_length in item_lengths]
            for line, spaces in zip(lines, spaces_to_add):
                if line[3] != "amount":
                    line[3] = f"${line[3]}"
                for location, (item, space_size) in enumerate(zip(line, spaces)):
                    item += (" " * space_size)
                    line[location] = item
            lines = ["  ".join(line) for line in lines]
            for line in lines:
                print(line)

month_dict = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
}

def summary_expenses(args):
    if args.summarymonth == None:
        expenses_db_content = csv.reader(open(expenses_database))
        next(expenses_db_content, None)
        amounts = [int(line[3]) for line in expenses_db_content]
        print(f"Total expenses: ${sum(amounts)}")
    else:
        expenses_db_content = csv.reader(open(expenses_database))
        next(expenses_db_content, None)
        amounts = [int(line[3]) for line in expenses_db_content if int(line[1].split("-")[1].strip("0")) == int(args.summarymonth)]
        print(f"{month_dict[int(args.summarymonth)]} expenses: ${sum(amounts)}")

def set_budget(args):
    if int(args.month) > 12:
        print("That is not a valid month.")
    else:
        if not os.path.exists("budget.txt"):
            budget_data = [['month', 'budget']]
            budget_data.append([args.month, args.budgetamount])
            with open("budget.txt", "w", newline="") as b:
                writer = csv.writer(b)
                writer.writerows(budget_data)
        else:
            budget_data = [line for line in csv.reader(open("budget.txt"))]
            budget_months = [budget[0] for budget in budget_data]
            if str(args.month) not in budget_months:
                with open("budget.txt", "a", newline="") as b:
                    writer = csv.writer(b)
                    writer.writerow([args.month, args.budgetamount])
            else:
                for budget in budget_data:
                    if budget[0] == str(args.month):
                        budget[1] = args.budgetamount
                with open("budget.txt", "w", newline="") as b:
                    writer = csv.writer(b)
                    writer.writerows(budget_data)
        print(f"The budget for {month_dict[args.month]} is set to ${args.budgetamount}")

def print_expenses(args):
    if args.printmonth == None:
        expenses_db_content = csv.reader(open(expenses_database))
        with open("ExpensesFull.csv", "w", newline="") as db:
            writer = csv.writer(db)
            writer.writerows(expenses_db_content)
        print(f"Expenses CSV Generated.")
    elif args.printmonth > 12:
        print("That is not a valid month")
    else:
        expenses_db_content = csv.reader(open(expenses_database))
        lines = [row for row in expenses_db_content]
        header = lines[0]
        lines = [row for row in lines[1:] if int(row[1].split("-")[1][-1]) == args.printmonth]
        lines.insert(0, header)
        with open(f"Expenses{month_dict[args.printmonth]}.csv", "w", newline="") as db:
            writer = csv.writer(db)
            writer.writerows(lines)
        print(f"{month_dict[args.printmonth]} Expenses CSV Generated.")
        
def date_validator(date_string: str) -> datetime:
    try:
        return str(datetime.strptime(date_string, "%Y-%m-%d").date())
    except ValueError:
        raise argparse.ArgumentTypeError(f"not a valid date: {date_string}")

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(required=True)

parser_add = subparsers.add_parser("add")
parser_add.add_argument("description", type=str)
parser_add.add_argument("--date", "-d", type=date_validator, default=str(datetime.today().strftime('%Y-%m-%d')))
parser_add.add_argument("--amount", "-a", type=int)
parser_add.add_argument("--category", "-c", default=None, choices= ["Groceries", "Rent/Mortgage", "Utilities",
                                                                    "Transportation", "Fuel", "Public Transit",
                                                                    "Insurance", "Phone & Internet", "Dining Out",
                                                                    "Entertainment", "Subscriptions", "Healthcare",
                                                                    "Medical Bills", "Fitness", "Clothing", "Personal Care",
                                                                    "Household Supplies", "Childcare", "Education",
                                                                    "Gifts & Donations", "Travel", "Pets", "Savings",
                                                                    "Investments", "Debt Payments", "Miscellaneous"])
parser_add.set_defaults(func=add_expense)

parser_update = subparsers.add_parser("update")
parser_update.add_argument("id", type=str)
parser_update.add_argument("--newdate", "-nd", type=date_validator)
parser_update.add_argument("--newamount", "-na", type=int)
parser_update.add_argument("--newdescription", "-nde", type=str)
parser_update.add_argument("--newcategory", "-nc", default=None, choices= ["Groceries", "Rent/Mortgage", "Utilities",
                                                                    "Transportation", "Fuel", "Public Transit",
                                                                    "Insurance", "Phone & Internet", "Dining Out",
                                                                    "Entertainment", "Subscriptions", "Healthcare",
                                                                    "Medical Bills", "Fitness", "Clothing", "Personal Care",
                                                                    "Household Supplies", "Childcare", "Education",
                                                                    "Gifts & Donations", "Travel", "Pets", "Savings",
                                                                    "Investments", "Debt Payments", "Miscellaneous"])
parser_update.set_defaults(func=update_expense)

parser_delete = subparsers.add_parser("delete")
parser_delete.add_argument("id", type=str)
parser_delete.set_defaults(func=delete_expense)

parser_list = subparsers.add_parser("list")
parser_list.add_argument("--monthfilter", "-mf", type=int, default=None)
parser_list.add_argument("--categoryfilter", "-cf", type=str, default=None, choices= ["Groceries", "Rent/Mortgage", "Utilities",
                                                                    "Transportation", "Fuel", "Public Transit",
                                                                    "Insurance", "Phone & Internet", "Dining Out",
                                                                    "Entertainment", "Subscriptions", "Healthcare",
                                                                    "Medical Bills", "Fitness", "Clothing", "Personal Care",
                                                                    "Household Supplies", "Childcare", "Education",
                                                                    "Gifts & Donations", "Travel", "Pets", "Savings",
                                                                    "Investments", "Debt Payments", "Miscellaneous"])
parser_list.set_defaults(func=list_expenses)

parser_summary = subparsers.add_parser("summary")
parser_summary.add_argument("--summarymonth", type=str, default=None)
parser_summary.set_defaults(func=summary_expenses)

parser_budget = subparsers.add_parser("setbudget")
parser_budget.add_argument("budgetamount")
parser_budget.add_argument("--month", "-m", type=int, default=datetime.now().month)
parser_budget.set_defaults(func=set_budget)

parser_print = subparsers.add_parser("print")
parser_print.add_argument("--printmonth", type=int, default=None)
parser_print.set_defaults(func=print_expenses)

args = parser.parse_args()
args.func(args)