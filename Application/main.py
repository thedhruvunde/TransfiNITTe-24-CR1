import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import openai
import time
import threading
from tkcalendar import DateEntry  # Import DateEntry for date selection

def get_gpt_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error: {str(e)}"

def on_submit():
    shop_name = shop_entry.get().strip()
    city_name = city_entry.get().strip()
    state_name = state_combobox.get().strip()
    start_date = date_entry_start.get()
    end_date = date_entry_end.get()

    if not all([shop_name, city_name, state_name, start_date, end_date]):
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return

    selected_sections = []
    if business_model_var.get():
        selected_sections.append("Key differentiators in Business Model")
    if geographical_presence_var.get():
        selected_sections.append("Geographical presence & store formats")
    if customer_feedback_var.get():
        selected_sections.append("Customer feedback (NPS, reviews etc.)")
    if strategic_initiatives_var.get():
        selected_sections.append("Any major strategic initiatives – investments, acquisitions, etc.")
    if future_outlook_var.get():
        selected_sections.append("Future outlook")

    prompt = (
        f"Please provide detailed information on the following aspects for the retailer '{shop_name}' "
        f"located in '{city_name}', '{state_name}' from {start_date} to {end_date}:\n"
    )

    if selected_sections:
        prompt += "\n".join(selected_sections) + "\n"

    chat_area.config(state='normal')
    chat_area.delete(1.0, tk.END)  # Clear the chat area
    chat_area.config(state='disabled')

    progress_bar.start()
    threading.Thread(target=fetch_response, args=(prompt,)).start()

def fetch_response(prompt):
    time.sleep(1)  # Simulate a delay for loading
    result = get_gpt_response(prompt)

    chat_area.config(state='normal')
    chat_area.insert(tk.END, f"Bot: {result}\n\n")
    chat_area.config(state='disabled')

    progress_bar.stop()  # Stop the progress bar

def refresh_fields():
    shop_entry.delete(0, tk.END)
    city_entry.delete(0, tk.END)
    state_combobox.set('')  # Clear the dropdown selection
    date_entry_start.set_date('')  # Clear the start date entry
    date_entry_end.set_date('')  # Clear the end date entry

    business_model_var.set(0)
    geographical_presence_var.set(0)
    customer_feedback_var.set(0)
    strategic_initiatives_var.set(0)
    future_outlook_var.set(0)

    chat_area.config(state='normal')
    chat_area.delete(1.0, tk.END)  # Clear the chat area
    chat_area.config(state='disabled')

def on_exit():
    root.quit()

# Create the main window
root = tk.Tk()
root.title("Electronics Retailer Finder")
root.geometry("800x700")  # Set a larger window size
root.configure(bg="#121212")  # Dark background
root.resizable(False, False)  # Lock the window size

# Swoosh animation
swoosh_label = tk.Label(root, text="Electronics Retailer Finder", font=("Arial", 24), fg="white", bg="#121212")
swoosh_label.place(x=-300, y=20)  # Start off-screen above the input fields

def continuous_scroll():
    x_pos = -300  # Starting position off-screen
    while True:
        x_pos += 2  # Move the label to the right
        if x_pos > 800:  # Reset position if it goes off the right side of the window
            x_pos = -300
        swoosh_label.place(x=x_pos, y=20)
        root.update()
        time.sleep(0.02)  # Control the speed of scrolling

# Start the continuous scrolling in a separate thread
threading.Thread(target=continuous_scroll, daemon=True).start()

# Create a frame for the input area
input_frame = tk.Frame(root, bg="#1E1E1E", padx=10, pady=10)
input_frame.pack(pady=80)  # Adjust padding to avoid overlap with the scrolling label

# Create labels and entry fields
tk.Label(input_frame, text="Shop Name:", bg="#1E1E1E", fg="white", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
shop_entry = tk.Entry(input_frame, width=40, font=("Arial", 12), bg="#2E2E2E", fg="white")
shop_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(input_frame, text="City Name:", bg="#1E1E1E", fg="white", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5)
city_entry = tk.Entry(input_frame, width=40, font=("Arial", 12), bg="#2E2E2E", fg="white")
city_entry.grid(row=1, column=1, padx=5, pady=5)

# Create a label for the state selection
tk.Label(input_frame, text="Choose State:", bg="#1E1E1E", fg="white", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5)

# Create a dropdown menu for states with increased width
states_of_india = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa",
    "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala",
    "Maharashtra", "Madhya Pradesh", "Manipur", "Meghalaya", "Mizoram", "Nagaland",
    "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Tripura", "Telangana",
    "Uttar Pradesh", "Uttarakhand", "West Bengal", "Andaman & Nicobar (UT)",
    "Chandigarh (UT)", "Dadra & Nagar Haveli and Daman & Diu (UT)",
    "Delhi [National Capital Territory (NCT)]", "Jammu & Kashmir (UT)", "Ladakh (UT)",
    "Lakshadweep (UT)", "Puducherry (UT)"
]

state_combobox = ttk.Combobox(input_frame, values=states_of_india, font=("Arial", 12), width=42, state="readonly", justify="center")
state_combobox.grid(row=2, column=1, padx=5, pady=5)

# Create labels for date range selection
tk.Label(input_frame, text="Select Date Range:", bg="#1E1E1E", fg="white", font=("Arial", 12)).grid(row=3, column=0, padx=5, pady=5)

# Date range entry fields
date_entry_start = DateEntry(input_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
date_entry_start.grid(row=3, column=1, padx=5, pady=5)

tk.Label(input_frame, text="to", bg="#1E1E1E", fg="white", font=("Arial", 12)).grid(row=3, column=2, padx=5, pady=5)

date_entry_end = DateEntry(input_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
date_entry_end.grid(row=3, column=3, padx=5, pady=5)

# Create checkboxes for optional sections
business_model_var = tk.IntVar()
geographical_presence_var = tk.IntVar()
customer_feedback_var = tk.IntVar()
strategic_initiatives_var = tk.IntVar()
future_outlook_var = tk.IntVar()

tk.Checkbutton(input_frame, text="Key differentiators in Business Model", variable=business_model_var, bg="#1E1E1E", fg="white", font=("Arial", 10)).grid(row=4, columnspan=2, sticky="w", padx=5, pady=2)
tk.Checkbutton(input_frame, text="Geographical presence & store formats", variable=geographical_presence_var, bg="#1E1E1E", fg="white", font=("Arial", 10)).grid(row=5, columnspan=2, sticky="w", padx=5, pady=2)
tk.Checkbutton(input_frame, text="Customer feedback (NPS, reviews etc.)", variable=customer_feedback_var, bg="#1E1E1E", fg="white", font=("Arial", 10)).grid(row=6, columnspan=2, sticky="w", padx=5, pady=2)
tk.Checkbutton(input_frame, text="Any major strategic initiatives", variable=strategic_initiatives_var, bg="#1E1E1E", fg="white", font=("Arial", 10)).grid(row=7, columnspan=2, sticky="w", padx=5, pady=2)
tk.Checkbutton(input_frame, text="Future outlook", variable=future_outlook_var, bg="#1E1E1E", fg="white", font=("Arial", 10)).grid(row=8, columnspan=2, sticky="w", padx=5, pady=2)

# Create a frame for buttons
button_frame = tk.Frame(input_frame, bg="#1E1E1E")
button_frame.grid(row=9, columnspan=2, pady=10, sticky="ew")

# Create a submit button
submit_button = tk.Button(button_frame, text="Submit", command=on_submit, bg="#007ACC", fg="black", font=("Arial", 12))
submit_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

# Create a refresh button
refresh_button = tk.Button(button_frame, text="Refresh", command=refresh_fields, bg="#FFC107", fg="black", font=("Arial", 12))
refresh_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

# Create an exit button
exit_button = tk.Button(button_frame, text="End", command=on_exit, bg="#FF3D00", fg="black", font=("Arial", 12))
exit_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

# Create a frame for the output area
output_frame = tk.Frame(root, bg="#1E1E1E", padx=10, pady=10)
output_frame.pack(pady=10)

# Create a label for the output
output_label = tk.Label(output_frame, text="Retailer Data:", bg="#1E1E1E", fg="white", font=("Arial", 12))
output_label.pack()

# Create a text area for displaying the chat history
chat_area = scrolledtext.ScrolledText(output_frame, width=70, height=20, wrap=tk.WORD, state='disabled', font=("Arial", 12), bg="#2E2E2E", fg="white")
chat_area.pack(pady=5)

# Create a progress bar
progress_bar = ttk.Progressbar(output_frame, mode='indeterminate')
progress_bar.pack(pady=5, fill=tk.X)

# Start the GUI event loop
root.mainloop()
