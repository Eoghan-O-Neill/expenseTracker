## Expense Tracker CLI APP  

This basic CLI app was created as a part of the [roadmap.sh backend developer roadmap](https://roadmap.sh/projects/expense-tracker) it allows users to create and store expenses and track them over time. The app uses all default python modules and therefore doesn't need a venv or requirements to be installed. Just run the python file in the command line using its name ``python expense-tracker.py``.  

To create an expense use the ``add`` argument followed by the expenses description. Adding an expense has the following flags.
- ``--date`` or ``-d`` to specify a date in the format YYYY-MM-DD. This defualts to the current date if no argument is provided.
- ``--amount`` or ``-a`` to add the expense amount as an integer.
- ``--category`` or ``-c``` to specify the expenses category. Possible categories are "Groceries", "Rent/Mortgage", "Utilities", "Transportation", "Fuel", "Public Transit", "Insurance", "Phone & Internet", "Dining Out", "Entertainment", "Subscriptions", "Healthcare", "Medical Bills", "Fitness", "Clothing", "Personal Care", "Household Supplies", "Childcare", "Education", "Gifts & Donations", "Travel", "Pets", "Savings", "Investments", "Debt Payments", "Miscellaneous".  

To update an expense use the ``update`` argument followed by the ID of the expense you want to update as an integer. Updating an expense has the following flags. 
- ``--newdate`` or ``-nd`` to specify an updated expense date in the format YYYY-MM-DD.
- ``--newamount`` or ``-na`` to specify an updated amount as an integer.
- ``--newdecription`` or ``-nd`` to specify an updated description.
- ``--newcategory`` or ``-nc`` to specify a new category. Possible categories are the same as when adding an expense.  

To delete an expense use the ``delete`` argument followed by the expenses ID.    

To list all expenses use the ``list`` argument. Lists can be filtered using the following flags.
- ``--monthfilter`` or ``-mf`` to list only expenses from a specific month to look at. This flag takes the number of the month from 1 to 12 as an int.
- ``--categoryfilter`` or ``-cf`` to list only expenses in a specific category to look at. This flag takes the name of the category as a string. Possible categories are the same as when adding an expense.  

To summarise (return a total) use the ``summary`` argumnent. Totals for a specific month can by attained by following with the ``--summarymonth`` flag which takes the relevant month as a number.  

To se a budget use the ``setbudget`` argument followed by a budget amount. You can set a budget for a specific month using the ``--month`` or ``-m`` flags followed by the month as an integer from 1 to 12. When adding expenses after setting a budget the CLI will display how much under or over budget the user is for the current month.  

To print expenses a csv can be generated using the ``print`` argument. To return only expenses for a specific month include the ``--printmonth`` flag followed by the number of the month between 1 and 12 as an integer.  
