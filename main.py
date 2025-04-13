import tkinter as tk
from tkinter import messagebox, ttk

# Logic functions
def add_expense(expenses, amount, category):
    expenses.append({'amount': amount, 'category': category})

def total_expenses(expenses):
    return sum(expense['amount'] for expense in expenses)

def filter_expenses_by_category(expenses, category):
    return [expense for expense in expenses if expense['category'].lower() == category.lower()]

def print_expenses(expenses):
    return '\n'.join([f"• Amount: ₹{expense['amount']}, Category: {expense['category']}" for expense in expenses])

def get_unique_categories(expenses):
    # Return a sorted list of unique categories
    return sorted(list(set(expense['category'] for expense in expenses)))

# GUI App
class ExpenseTrackerApp:
    def __init__(self, root):
        self.expenses = []
        
        # Define color scheme
        self.primary_color = "#1a53ff"     # Medium blue
        self.secondary_color = "#e6ecff"   # Light blue
        self.bg_color = "#f0f5ff"          # Very light blue for background
        self.text_color = "#003366"        # Dark blue text
        self.highlight_color = "#4d79ff"   # Lighter blue for highlights
        
        root.title("💸 Expense Tracker")
        root.geometry("600x550")
        root.resizable(False, False)
        root.configure(bg=self.bg_color)

        # Apply theme to root window first
        self.configure_styles()

        # Title
        title_label = tk.Label(root, text="Expense Tracker", font=('Segoe UI', 18, 'bold'), 
                              bg=self.bg_color, fg=self.primary_color)
        title_label.pack(pady=10)

        # Input Frame - using tk.Frame instead of ttk.Frame for consistent background
        input_frame = tk.Frame(root, bg=self.bg_color, bd=1, relief=tk.GROOVE, padx=15, pady=15)
        input_frame.pack(pady=5, padx=20, fill="x")

        # Amount label and entry
        amount_label = tk.Label(input_frame, text="Amount (₹):", font=('Segoe UI', 11), 
                               bg=self.bg_color, fg=self.text_color)
        amount_label.grid(row=0, column=0, padx=5, pady=8, sticky="e")
        
        self.amount_entry = tk.Entry(input_frame, width=20, font=('Segoe UI', 10), 
                                    bd=1, relief=tk.SOLID)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=8)

        # Category label and entry
        category_label = tk.Label(input_frame, text="Category:", font=('Segoe UI', 11), 
                                 bg=self.bg_color, fg=self.text_color)
        category_label.grid(row=1, column=0, padx=5, pady=8, sticky="e")
        
        # Use combobox for category (allow both selection and new entry)
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(input_frame, width=18, textvariable=self.category_var, 
                                          font=('Segoe UI', 10))
        self.category_combo['values'] = ['Food', 'Transport', 'Entertainment', 'Utilities', 'Shopping', 'Other']
        self.category_combo.grid(row=1, column=1, padx=5, pady=8)

        # Add expense button
        self.add_button = tk.Button(input_frame, text="Add Expense", font=('Segoe UI', 11, 'bold'),
                                   bg=self.primary_color, fg="white", padx=10, pady=5,
                                   activebackground=self.highlight_color, activeforeground="white",
                                   command=self.add_expense_gui)
        self.add_button.grid(row=2, column=0, columnspan=2, pady=12)

        # Button Frame
        button_frame = tk.Frame(root, bg=self.bg_color, bd=1, relief=tk.GROOVE, padx=15, pady=15)
        button_frame.pack(pady=10, padx=20, fill="x")

        # Action buttons
        show_all_btn = tk.Button(button_frame, text="Show All Expenses", width=20, 
                                bg=self.highlight_color, fg="white", font=('Segoe UI', 10),
                                activebackground=self.primary_color, activeforeground="white",
                                command=self.show_expenses)
        show_all_btn.grid(row=0, column=0, padx=8, pady=8)
        
        show_total_btn = tk.Button(button_frame, text="Show Total", width=20, 
                                  bg=self.highlight_color, fg="white", font=('Segoe UI', 10),
                                  activebackground=self.primary_color, activeforeground="white",
                                  command=self.show_total)
        show_total_btn.grid(row=0, column=1, padx=8, pady=8)
        
        # Filter Frame with label and dropdown
        filter_frame = tk.Frame(button_frame, bg=self.bg_color)
        filter_frame.grid(row=1, column=0, padx=8, pady=8)
        
        filter_label = tk.Label(filter_frame, text="Filter: ", bg=self.bg_color, fg=self.text_color,
                               font=('Segoe UI', 10))
        filter_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.filter_var = tk.StringVar()
        self.filter_combo = ttk.Combobox(filter_frame, width=13, textvariable=self.filter_var, 
                                       font=('Segoe UI', 10), state="readonly")
        self.filter_combo.pack(side=tk.LEFT)
        self.update_filter_dropdown()
        
        # Filter button
        filter_btn = tk.Button(button_frame, text="Apply Filter", width=20, 
                              bg=self.highlight_color, fg="white", font=('Segoe UI', 10),
                              activebackground=self.primary_color, activeforeground="white",
                              command=self.filter_by_category)
        filter_btn.grid(row=1, column=1, padx=8, pady=8)
        
        # Exit button in a new row
        exit_btn = tk.Button(button_frame, text="Exit", width=20, 
                            bg="#cecece", fg=self.text_color, font=('Segoe UI', 10),
                            activebackground="#b1b1b1", activeforeground=self.text_color,
                            command=root.quit)
        exit_btn.grid(row=2, column=0, columnspan=2, padx=8, pady=(8, 0))

        # Output Frame
        output_frame = tk.Frame(root, bg=self.bg_color, bd=1, relief=tk.GROOVE, padx=2, pady=2)
        output_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Output Text widget
        self.output_text = tk.Text(output_frame, height=12, width=65, font=('Consolas', 11), 
                                  bg="white", fg=self.text_color, wrap=tk.WORD,
                                  borderwidth=1, relief=tk.SOLID)
        self.output_text.pack(padx=5, pady=5, fill="both", expand=True)
        
        # Status bar
        status_bar = tk.Frame(root, bg=self.primary_color, height=25)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        status_label = tk.Label(status_bar, text="💰 Expense Tracker v1.0", 
                               font=('Segoe UI', 9), bg=self.primary_color, fg="white")
        status_label.pack(pady=2)

    def configure_styles(self):
        # Configure ttk styles (for any remaining ttk widgets)
        style = ttk.Style()
        style.configure("TFrame", background=self.bg_color)
        style.configure("TLabel", font=('Segoe UI', 10), background=self.bg_color, foreground=self.text_color)
        style.configure("TButton", font=('Segoe UI', 10))
        
        # Configure combobox style
        style.map('TCombobox', fieldbackground=[('readonly', 'white')])
        style.map('TCombobox', selectbackground=[('readonly', self.primary_color)])
        style.map('TCombobox', selectforeground=[('readonly', 'white')])

    def update_filter_dropdown(self):
        # Get unique categories
        categories = get_unique_categories(self.expenses)
        
        # Add 'All Categories' option at the beginning
        dropdown_values = ['All Categories'] + categories
        
        # Update dropdown values
        self.filter_combo['values'] = dropdown_values
        
        # Set default value if not already set
        if not self.filter_var.get() or self.filter_var.get() not in dropdown_values:
            self.filter_var.set('All Categories')

    def add_expense_gui(self):
        try:
            amount = float(self.amount_entry.get())
            category = self.category_var.get().strip()
            if not category:
                raise ValueError("Category is required.")
            add_expense(self.expenses, amount, category)
            messagebox.showinfo("Success", f"Expense added: ₹{amount} for '{category}'")
            self.amount_entry.delete(0, tk.END)
            self.category_var.set("")  # Clear category
            
            # Update the filter dropdown with the new category
            self.update_filter_dropdown()
            
            # Update category dropdown to include the new category if it doesn't exist already
            current_values = list(self.category_combo['values'])
            if category not in current_values:
                self.category_combo['values'] = sorted(current_values + [category])
                
        except ValueError as e:
            messagebox.showerror("Invalid Input", f"Please enter a valid amount and category. {str(e)}")

    def show_expenses(self):
        self.output_text.delete(1.0, tk.END)
        if self.expenses:
            self.output_text.insert(tk.END, "📋 All Expenses:\n\n")
            result = print_expenses(self.expenses)
            self.output_text.insert(tk.END, result)
        else:
            self.output_text.insert(tk.END, "⚠️ No expenses recorded yet.")

    def show_total(self):
        total = total_expenses(self.expenses)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, f"💰 Total Expenses: ₹{total:.2f}")

    def filter_by_category(self):
        selected_category = self.filter_var.get()
        
        if not selected_category or selected_category == 'All Categories':
            # Show all expenses if 'All Categories' is selected
            self.show_expenses()
            return
            
        filtered = filter_expenses_by_category(self.expenses, selected_category)
        self.output_text.delete(1.0, tk.END)
        
        if filtered:
            self.output_text.insert(tk.END, f"🔍 Expenses for '{selected_category}':\n\n")
            result = print_expenses(filtered)
            self.output_text.insert(tk.END, result)
            
            # Add category total
            category_total = sum(expense['amount'] for expense in filtered)
            self.output_text.insert(tk.END, f"\n\nTotal for '{selected_category}': ₹{category_total:.2f}")
        else:
            self.output_text.insert(tk.END, f"❌ No expenses found for category '{selected_category}'.")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()