# Created by Pu043431Void
# Version 1.7.1
# 2.20.25

from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
from tkinter import ttk

# Create main application window
root = Tk()
root.resizable(False, False)  # Sets both horizontal and vertical resizing to False
root.title("Advanced Budget Calculator")
tabControl = ttk.Notebook(root)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl) 

# Set the window size
root.geometry("600x700")

# Lists to store incomes and expenses
incomes = []
expenses = []

# Expense Categories (can also be left blank)
expense_categories = [
    "", "Housing & Utilities", "Bills", "Transportation", "Loan Payment", "Other Debt",
    "Living Expenses", "Healthcare", "Family", "Education", "Savings",
    "Investments", "Miscellaneous Expense", "Other"
]

# Function to add income
def add_income():
    desc = income_desc_entry.get()
    amount = income_amount_entry.get()
    if desc and amount:
        try:
            amount = float(amount)
            incomes.append((desc, amount))
            income_listbox.insert(END, f"{desc}: ${amount:.2f}")
            income_desc_entry.delete(0, END)
            income_amount_entry.delete(0, END)
        except ValueError:
            tkinter.messagebox.showerror("Input Error", "Please enter a valid income amount.")

# Function to add expense
def add_expense():
    desc = expense_desc_entry.get()
    amount = expense_amount_entry.get()
    category = expense_category_combobox.get().strip()

    if desc and amount:
        try:
            amount = float(amount)
            expenses.append((category, desc, amount))  # Store category, desc, amount
            expense_listbox.insert(END, f"{desc} ({category if category else 'Uncategorized'}): ${amount:.2f}")
            expense_desc_entry.delete(0, END)
            expense_amount_entry.delete(0, END)
            expense_category_combobox.set("")  # Reset category field (empty)
        except ValueError:
            tkinter.messagebox.showerror("Input Error", "Please enter a valid expense amount.")

# Function to remove selected income
def remove_income():
    selected_idx = income_listbox.curselection()
    if selected_idx:
        incomes.pop(selected_idx[0])  # Remove from list
        income_listbox.delete(selected_idx)  # Remove from UI

# Function to remove selected expense
def remove_expense():
    selected_idx = expense_listbox.curselection()
    if selected_idx:
        expenses.pop(selected_idx[0])  # Remove from list
        expense_listbox.delete(selected_idx)  # Remove from UI

# Function to calculate budget and show breakdown
def calculate_budget():
    total_income = sum(amount for _, amount in incomes)
    total_expenses = sum(amount for _, _, amount in expenses)
    savings = total_income - total_expenses

    # Group expenses by category
    categorized_expenses = {}
    for category, desc, amount in expenses:
        category = category if category else "Uncategorized"  # Default if empty
        if category not in categorized_expenses:
            categorized_expenses[category] = []
        categorized_expenses[category].append((desc, amount))

    # Create breakdown text
    breakdown = "Income Breakdown:\n"
    for desc, amount in incomes:
        breakdown += f"  {desc}: ${amount:.2f}\n"

    breakdown += "\nExpense Breakdown:\n"
    for category, items in categorized_expenses.items():
        breakdown += f"  {category}:\n"
        for desc, amount in items:
            breakdown += f"    {desc}: ${amount:.2f}\n"

    breakdown += f"\nTotal Income: ${total_income:.2f}\nTotal Expenses: ${total_expenses:.2f}\nSavings: ${savings:.2f}"

    # Display results
    result_text.set(f"Total Income: ${total_income:.2f}\n"
                    f"Total Expenses: ${total_expenses:.2f}\n"
                    f"Savings: ${savings:.2f}")

    # Show detailed breakdown in text box
    breakdown_text.delete(1.0, END)
    breakdown_text.insert(END, breakdown)

    # Show the "Summary" button
    summary_button.grid(row=0, column=1, padx=10)

# Function to export breakdown to a text file
def export_to_txt():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(breakdown_text.get(1.0, END))  # Get text from text widget
        tkinter.messagebox.showinfo("Success", f"Budget breakdown saved to:\n{file_path}")

# Function to import a budget from a TXT file
def import_from_txt():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "r") as file:
            data = file.readlines()

        # Clear existing data
        incomes.clear()
        expenses.clear()
        income_listbox.delete(0, END)
        expense_listbox.delete(0, END)

        # Parse the imported data
        section = None
        for line in data:
            line = line.strip()
            if "Income Breakdown:" in line:
                section = "income"
            elif "Expense Breakdown:" in line:
                section = "expense"
            elif "Total Income:" in line:
                break  # Stop parsing after totals
            elif section and line:
                try:
                    desc, amount = line.split(": $")
                    amount = float(amount)
                    if section == "income":
                        incomes.append((desc.strip(), amount))
                        income_listbox.insert(END, f"{desc.strip()}: ${amount:.2f}")
                    elif section == "expense":
                        expenses.append(("", desc.strip(), amount))  # Default category empty
                        expense_listbox.insert(END, f"{desc.strip()} (Uncategorized): ${amount:.2f}")
                except ValueError:
                    continue  # Skip invalid lines

        # Recalculate budget after import
        calculate_budget()
        tkinter.messagebox.showinfo("Success", "Budget imported successfully!")

# Function to switch to Summary tab
def go_to_summary():
    tabControl.select(tab2)  # Switch to Summary tab

# Tab Control
tabControl.add(tab1, text ='Info') 
tabControl.add(tab2, text ='Summary') 
tabControl.pack(expand=1, fill="both")

# Labels and Entry Fields for Income
Label(tab1, text="Add Income").pack(pady=5)
frame_income = Frame(tab1)
frame_income.pack()

Label(frame_income, text="Description:").grid(row=0, column=0)
income_desc_entry = Entry(frame_income, width=20)
income_desc_entry.grid(row=0, column=1)

Label(frame_income, text="Amount:").grid(row=0, column=2)
income_amount_entry = Entry(frame_income, width=20)
income_amount_entry.grid(row=0, column=3)

# Listbox to display added incomes
income_listbox = Listbox(tab1, height=9, width=55)
income_listbox.pack(pady=5)

# Income Buttons
Button(frame_income, text="Add Income", command=add_income).grid(row=0, column=4, padx=5)
Button(tab1, text="Remove Selected Income", command=remove_income).pack(pady=5)

# Labels and Entry Fields for Expenses
Label(tab1, text="Add Expense").pack(pady=5)
frame_expense = Frame(tab1)
frame_expense.pack()

Label(frame_expense, text="Description:").grid(row=0, column=0)
expense_desc_entry = Entry(frame_expense, width=20)
expense_desc_entry.grid(row=0, column=1)

Label(frame_expense, text="Amount:").grid(row=0, column=2)
expense_amount_entry = Entry(frame_expense, width=20)
expense_amount_entry.grid(row=0, column=3)

Label(frame_expense, text="Category:").grid(row=1, column=0)
expense_category_combobox = ttk.Combobox(frame_expense, values=expense_categories, state="readonly", width=17)
expense_category_combobox.grid(row=1, column=1)
expense_category_combobox.set("")  # Default is blank

# Listbox to display added expenses
expense_listbox = Listbox(tab1, height=10, width=55)
expense_listbox.pack(pady=5)

# Expense Buttons
Button(frame_expense, text="Add Expense", command=add_expense).grid(row=0, column=4, padx=5)
Button(tab1, text="Remove Selected Expense", command=remove_expense).pack(pady=5)

# Create Frame for Buttons (Ensures Proper Alignment)
button_frame = Frame(tab1)
button_frame.pack(pady=10)

# Calculate Button
calculate_button = Button(button_frame, text="Calculate Budget", command=calculate_budget)
calculate_button.grid(row=0, column=0, padx=10)

# Summary Button (Initially Hidden)
summary_button = Button(button_frame, text="Summary", command=go_to_summary)
summary_button.grid(row=0, column=1, padx=10)
summary_button.grid_remove()  # Hide initially

# Result Display
result_text = StringVar()
result_label = Label(tab1, textvariable=result_text, font=("Arial", 11), justify="left")
result_label.pack(pady=10)

# Budget Breakdown Display
Label(tab2, text="Budget Breakdown").pack()
breakdown_text = Text(tab2, height=35, width=55)
breakdown_text.pack(pady=5)

# Frame for Export & Import Buttons
button_frame = Frame(tab2)
button_frame.pack(pady=10)

# Export & Import Buttons
Button(button_frame, text="Export to TXT", command=export_to_txt).grid(row=0, column=0, padx=10)
Button(button_frame, text="Import from TXT", command=import_from_txt).grid(row=0, column=1, padx=10)

# Run Tkinter event loop
root.mainloop()