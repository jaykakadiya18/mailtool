import tkinter as tk
from tkinter import ttk

def submit_form():
    # Code to process the form data
    pass

root = tk.Tk()
root.title("Email Sending Tool")

# Styling
style = ttk.Style()
style.configure("TFrame", background="#F0F0F0")
style.configure("TLabel", background="#F0F0F0")
style.configure("TButton", background="#4CAF50", foreground="white")

main_frame = ttk.Frame(root, padding="20")
main_frame.place(relx=0.5, rely=0.5, anchor="center")

messages_frame = ttk.Frame(main_frame, padding="10")
messages_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
messages_label = ttk.Label(messages_frame, text="Messages:", font=("Helvetica", 12))
messages_label.grid(row=0, column=0, padx=5)
messages_combobox = ttk.Combobox(messages_frame, values=["Message 1", "Message 2"], state="readonly", font=("Helvetica", 12))
messages_combobox.grid(row=0, column=1, padx=5)

server_frame = ttk.Frame(main_frame, padding="10")
server_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
host_label = ttk.Label(server_frame, text="Server Host:", font=("Helvetica", 12))
host_label.grid(row=0, column=0, padx=5)
host_entry = ttk.Entry(server_frame, font=("Helvetica", 12))
host_entry.grid(row=0, column=1, padx=5)

port_label = ttk.Label(server_frame, text="Server Port:", font=("Helvetica", 12))
port_label.grid(row=1, column=0, padx=5)
port_entry = ttk.Entry(server_frame, font=("Helvetica", 12))
port_entry.grid(row=1, column=1, padx=5)

email_frame = ttk.Frame(main_frame, padding="10")
email_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")
username_label = ttk.Label(email_frame, text="Email Address:", font=("Helvetica", 12))
username_label.grid(row=0, column=0, padx=5)
username_entry = ttk.Entry(email_frame, font=("Helvetica", 12))
username_entry.grid(row=0, column=1, padx=5)

password_label = ttk.Label(email_frame, text="Password:", font=("Helvetica", 12))
password_label.grid(row=1, column=0, padx=5)
password_entry = ttk.Entry(email_frame, show="*", font=("Helvetica", 12))
password_entry.grid(row=1, column=1, padx=5)

submit_button = ttk.Button(main_frame, text="Submit", command=submit_form, width=15)
submit_button.grid(row=3, column=0, columnspan=2, pady=20)

logs_frame = ttk.Frame(main_frame, padding="10")
logs_frame.grid(row=4, column=0, columnspan=2, sticky="nsew")
view_logs_button = ttk.Button(logs_frame, text="View Logs", width=15)
view_logs_button.grid(row=0, column=0, padx=5)
download_logs_button = ttk.Button(logs_frame, text="Download Logs", width=15)
download_logs_button.grid(row=0, column=1, padx=5)

# Center the window on the screen
window_width = root.winfo_screenwidth()
window_height = root.winfo_screenheight()
window_x = int(window_width / 2 - main_frame.winfo_width() / 2)
window_y = int(window_height / 2 - main_frame.winfo_height() / 2)
root.geometry(f"+{window_x}+{window_y}")

root.mainloop()
