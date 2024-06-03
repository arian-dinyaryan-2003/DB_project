import tkinter as tk
from tkinter import ttk

def open_bank_info():
    bank_info_window = tk.Toplevel(root)
    bank_info_window.title("Bank Information")
    bank_info_window.configure(bg="lightblue")
    
    columns = ("bank_name", "withdrawal", "deposit", "balance")
    
    tree = ttk.Treeview(bank_info_window, columns=columns, show='headings')
    tree.heading("bank_name", text="Bank Name")
    tree.heading("withdrawal", text="Withdraw")
    tree.heading("deposit", text="Deposit")
    tree.heading("balance", text="Balance")
    
    tree.column("bank_name", width=150, anchor='center')
    tree.column("withdrawal", width=100, anchor='center')
    tree.column("deposit", width=100, anchor='center')
    tree.column("balance", width=100, anchor='center')
    
    # Sample data
    data = [
        ("Bank 1", 100, 200, 300),
        ("Bank 2", 150, 250, 400),
        ("Bank 3", 200, 300, 500)
    ]
    
    for item in data:
        tree.insert('', 'end', values=item)
    
    tree.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
    
    scrollbar = ttk.Scrollbar(bank_info_window, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

def open_window1():
    window1 = tk.Toplevel(root)
    window1.title("Show Information")
    window1.configure(bg="lightblue")
    
    columns = ("amount", "title", "bank", "date")
    
    tree = ttk.Treeview(window1, columns=columns, show='headings')
    tree.heading("amount", text="Amount")
    tree.heading("title", text="Title")
    tree.heading("bank", text="Bank")
    tree.heading("date", text="Date")

    tree.column("amount", width=100, anchor='center')
    tree.column("title", width=100, anchor='center')
    tree.column("bank", width=100, anchor='center')
    tree.column("date", width=100, anchor='center')
    
    # Sample data
    data = [
        (1000, "Groceries", "Bank 1", "2024-01-01"),
        (500, "Rent", "Bank 2", "2024-02-01"),
        (200, "Utilities", "Bank 3", "2024-03-01")
    ]
    
    for item in data:
        tree.insert('', 'end', values=item)
    
    tree.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
    
    scrollbar = ttk.Scrollbar(window1, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Add Bank Info button
    bank_info_button = tk.Button(window1, text="Bank Info", command=open_bank_info, width=15, height=2, bg="lightblue", fg="black", activebackground="blue", activeforeground="white", font=("Helvetica", 12))
    bank_info_button.pack(pady=10)

def open_window2():
    window2 = tk.Toplevel(root)
    window2.title("Add record")
    window2.configure(bg="lightgreen")
    label2 = ttk.Label(window2, text="Add record", background="lightgreen", font=("Helvetica", 16))
    label2.pack(padx=20, pady=20)

    button_bank_card = tk.Button(window2, text="Add bank card", command=open_add_bank_card, width=30, height=3, bg="palegreen", fg="black", activebackground="green", activeforeground="white", font=("Helvetica", 14))
    button_bank_card.pack(padx=20, pady=10)

    button_transaction = tk.Button(window2, text="Add transaction", command=open_add_transaction, width=30, height=3, bg="lightseagreen", fg="black", activebackground="green", activeforeground="white", font=("Helvetica", 14))
    button_transaction.pack(padx=20, pady=10)

    button_category = tk.Button(window2, text="Add category", command=open_add_category, width=30, height=3, bg="mediumseagreen", fg="black", activebackground="green", activeforeground="white", font=("Helvetica", 14))
    button_category.pack(padx=20, pady=10)

def open_window3():
    window3 = tk.Toplevel(root)
    window3.title("Search")
    window3.configure(bg="lightyellow")

    label3 = ttk.Label(window3, text="Search", background="lightyellow", font=("Helvetica", 16))
    label3.pack(padx=20, pady=20)

    category_label = ttk.Label(window3, text="Select Category:", background="lightyellow", font=("Helvetica", 12))
    category_label.pack(padx=20, pady=(10, 0))

    categories = ["Category 1", "Category 2", "Category 3"]  # مثال از دسته‌بندی‌ها
    category_combobox = ttk.Combobox(window3, values=categories, font=("Helvetica", 12))
    category_combobox.pack(padx=20, pady=5)

    start_date_label = ttk.Label(window3, text="Start Date:", background="lightyellow", font=("Helvetica", 12))
    start_date_label.pack(padx=20, pady=(10, 0))

    start_date_entry = ttk.Entry(window3, font=("Helvetica", 12))
    start_date_entry.pack(padx=20, pady=5)

    end_date_label = ttk.Label(window3, text="End Date:", background="lightyellow", font=("Helvetica", 12))
    end_date_label.pack(padx=20, pady=(10, 0))

    end_date_entry = ttk.Entry(window3, font=("Helvetica", 12))
    end_date_entry.pack(padx=20, pady=5)

    search_button = tk.Button(window3, text="Search Now", width=15, height=2, bg="lightblue", fg="black", activebackground="blue", activeforeground="white", font=("Helvetica", 12))
    search_button.pack(padx=20, pady=20)

def open_add_bank_card():
    add_bank_card_window = tk.Toplevel(root)
    add_bank_card_window.title("Add Bank Card")
    add_bank_card_window.configure(bg="palegreen")
    
    label = ttk.Label(add_bank_card_window, text="Add Bank Card", background="palegreen", font=("Helvetica", 16))
    label.pack(padx=20, pady=20)

    bank_name_label = ttk.Label(add_bank_card_window, text="Bank Name:", background="palegreen", font=("Helvetica", 12))
    bank_name_label.pack(padx=20, pady=(10, 0))

    bank_name_entry = ttk.Entry(add_bank_card_window, font=("Helvetica", 12))
    bank_name_entry.pack(padx=20, pady=5)

    balance_label = ttk.Label(add_bank_card_window, text="Bank Balance:", background="palegreen", font=("Helvetica", 12))
    balance_label.pack(padx=20, pady=(10, 0))

    balance_entry = ttk.Entry(add_bank_card_window, font=("Helvetica", 12))
    balance_entry.pack(padx=20, pady=5)

    add_button = tk.Button(add_bank_card_window, text="Add", width=15, height=2, bg="lightblue", fg="black", activebackground="blue", activeforeground="white", font=("Helvetica", 12))
    add_button.pack(padx=20, pady=20)

def open_add_transaction():
    add_transaction_window = tk.Toplevel(root)
    add_transaction_window.title("Add Transaction")
    add_transaction_window.configure(bg="lightseagreen")
    
    label = ttk.Label(add_transaction_window, text="Add Transaction", background="lightseagreen", font=("Helvetica", 16))
    label.pack(padx=20, pady=20)

    amount_label = ttk.Label(add_transaction_window, text="Transaction Amount:", background="lightseagreen", font=("Helvetica", 12))
    amount_label.pack(padx=20, pady=(10, 0))

    amount_entry = ttk.Entry(add_transaction_window, font=("Helvetica", 12))
    amount_entry.pack(padx=20, pady=5)

    bank_name_label = ttk.Label(add_transaction_window, text="Select Bank:", background="lightseagreen", font=("Helvetica", 12))
    bank_name_label.pack(padx=20, pady=(10, 0))

    bank_names = ["Bank 1", "Bank 2", "Bank 3"]  # مثال از نام بانک‌ها
    bank_name_combobox = ttk.Combobox(add_transaction_window, values=bank_names, font=("Helvetica", 12))
    bank_name_combobox.pack(padx=20, pady=5)

    category_label = ttk.Label(add_transaction_window, text="Select Category:", background="lightseagreen", font=("Helvetica", 12))
    category_label.pack(padx=20, pady=(10, 0))

    categories = ["Category 1", "Category 2", "Category 3"]  # مثال از دسته‌بندی‌ها
    category_combobox = ttk.Combobox(add_transaction_window, values=categories, font=("Helvetica", 12))
    category_combobox.pack(padx=20, pady=5)

    date_label = ttk.Label(add_transaction_window, text="Transaction Date:", background="lightseagreen", font=("Helvetica", 12))
    date_label.pack(padx=20, pady=(10, 0))

    date_entry = ttk.Entry(add_transaction_window, font=("Helvetica", 12))
    date_entry.pack(padx=20, pady=5)

    add_button = tk.Button(add_transaction_window, text="Add", width=15, height=2, bg="lightblue", fg="black", activebackground="blue", activeforeground="white", font=("Helvetica", 12))
    add_button.pack(padx=20, pady=20)

def open_add_category():
    add_category_window = tk.Toplevel(root)
    add_category_window.title("Add Category")
    add_category_window.configure(bg="mediumseagreen")

    label = ttk.Label(add_category_window, text="Add Category", background="mediumseagreen", font=("Helvetica", 16))
    label.pack(padx=20, pady=20)

    category_name_label = ttk.Label(add_category_window, text="Category Name:", background="mediumseagreen", font=("Helvetica", 12))
    category_name_label.pack(padx=20, pady=(10, 0))

    category_name_entry = ttk.Entry(add_category_window, font=("Helvetica", 12))
    category_name_entry.pack(padx=20, pady=5)

    type_label = ttk.Label(add_category_window, text="Category Type:", background="mediumseagreen", font=("Helvetica", 12))
    type_label.pack(padx=20, pady=(10, 0))

    category_types = ["Income", "Expense"]
    type_combobox = ttk.Combobox(add_category_window, values=category_types, font=("Helvetica", 12))
    type_combobox.pack(padx=20, pady=5)

    priority_label = ttk.Label(add_category_window, text="Priority:", background="mediumseagreen", font=("Helvetica", 12))
    priority_label.pack(padx=20, pady=(10, 0))

    priorities = ["1", "2", "3"]
    priority_combobox = ttk.Combobox(add_category_window, values=priorities, font=("Helvetica", 12))
    priority_combobox.pack(padx=20, pady=5)

    add_button = tk.Button(add_category_window, text="Add", width=15, height=2, bg="lightblue", fg="black", activebackground="blue", activeforeground="white", font=("Helvetica", 12))
    add_button.pack(padx=20, pady=20)

root = tk.Tk()
root.title("My Database Project")

title_label = tk.Label(root, text="My Database Project", font=("Helvetica", 20, "bold"))
title_label.pack(padx=40, pady=20)

button1 = tk.Button(root, text="Show information", command=open_window1, width=40, height=4, bg="lightblue", fg="black", activebackground="blue", activeforeground="white", font=("Helvetica", 16))
button1.pack(padx=40, pady=10)

button2 = tk.Button(root, text="Add record", command=open_window2, width=40, height=4, bg="lightgreen", fg="black", activebackground="green", activeforeground="white", font=("Helvetica", 16))
button2.pack(padx=40, pady=10)

button3 = tk.Button(root, text="Search", command=open_window3, width=40, height=4, bg="lightyellow", fg="black", activebackground="yellow", activeforeground="white", font=("Helvetica", 16))
button3.pack(padx=40, pady=10)

root.mainloop()
