import tkinter as tk
from tkinter import messagebox
import mysql.connector
import random

def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="Quote_App",
            port=3307
        )
        return connection
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Cannot connect to MySQL:\n{e}")
        exit()

current_quote_id = None
root = tk.Tk()
root.title("Quote of the Day App")
root.geometry("600x480")
root.resizable(False, False)
root.configure(bg="#f4f6f8")

quote_text = tk.StringVar()
author_text = tk.StringVar()

def show_random_quote():
    global current_quote_id
    conn = connect_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM quotes ORDER BY RAND() LIMIT 1")
    quote = cur.fetchone()
    conn.close()

    if quote:
        current_quote_id = quote['id']
        quote_text.set(f"“{quote['quote']}”")
        author_text.set(f"- {quote['author']}")
    else:
        current_quote_id = None
        quote_text.set("No quotes available.")
        author_text.set("")

def delete_quote():
    """Delete the currently shown quote"""
    global current_quote_id
    if current_quote_id is None:
        messagebox.showwarning("Delete Error", "No quote selected to delete.")
        return

    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this quote?")
    if not confirm:
        return

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM quotes WHERE id = %s", (current_quote_id,))
    conn.commit()
    conn.close()

    messagebox.showinfo("Deleted", "Quote deleted successfully!")
    show_random_quote()

def add_quote():
    author = author_entry.get().strip()
    quote = quote_entry.get("1.0", tk.END).strip()

    if author == "" or quote == "":
        messagebox.showwarning("Input Error", "Please enter both author and quote.")
        return

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO quotes (author, quote) VALUES (%s, %s)", (author, quote))
    conn.commit()
    conn.close()

    author_entry.delete(0, tk.END)
    quote_entry.delete("1.0", tk.END)
    messagebox.showinfo("Success", "Quote added successfully!")

# ------------------ PAGE SWITCHING ------------------
def show_main_page():
    """Show the main quote viewing page"""
    add_frame.pack_forget()
    main_frame.pack(fill="both", expand=True)

def show_add_page():
    """Show the add quote page"""
    main_frame.pack_forget()
    add_frame.pack(fill="both", expand=True)

# ------------------ MAIN PAGE (VIEW + DELETE) ------------------
main_frame = tk.Frame(root, bg="#f4f6f8")

title_label = tk.Label(main_frame, text="Quote of the Day",
                       font=("Georgia", 18, "bold"), bg="#f4f6f8", fg="#333")
title_label.pack(pady=20)

frame_display = tk.Frame(main_frame, bg="white", bd=2, relief="groove")
frame_display.pack(pady=20, ipadx=10, ipady=10)

quote_label = tk.Label(frame_display, textvariable=quote_text, wraplength=480,
                       font=("Georgia", 13), bg="white", fg="#222", justify="center")
quote_label.pack(padx=10, pady=15)

author_label = tk.Label(frame_display, textvariable=author_text,
                        font=("Arial", 10, "italic"), bg="white", fg="#666")
author_label.pack(pady=5)

refresh_btn = tk.Button(main_frame, text="Show Another Quote", command=show_random_quote,
                        bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
                        relief="flat", width=25, height=2)
refresh_btn.pack(pady=10)

delete_btn = tk.Button(main_frame, text="Delete Quote", command=delete_quote,
                       bg="#E53935", fg="white", font=("Arial", 10, "bold"),
                       relief="flat", width=25, height=2)
delete_btn.pack(pady=5)

to_add_page_btn = tk.Button(main_frame, text="➕ Add New Quote", command=show_add_page,
                            bg="#2196F3", fg="white", font=("Arial", 10, "bold"),
                            relief="flat", width=25, height=2)
to_add_page_btn.pack(pady=35)

# ------------------ ADD QUOTE PAGE ------------------
add_frame = tk.Frame(root, bg="#f4f6f8")

add_title = tk.Label(add_frame, text="Add a New Quote",
                     font=("Georgia", 18, "bold"), bg="#f4f6f8", fg="#333")
add_title.pack(pady=20)

author_label2 = tk.Label(add_frame, text="Author Name:", bg="#f4f6f8", font=("Arial", 11))
author_label2.pack(pady=5)
author_entry = tk.Entry(add_frame, width=50, font=("Arial", 11))
author_entry.pack(pady=5)

quote_label2 = tk.Label(add_frame, text="Quote:", bg="#f4f6f8", font=("Arial", 11))
quote_label2.pack(pady=5)
quote_entry = tk.Text(add_frame, width=50, height=5, font=("Arial", 11))
quote_entry.pack(pady=5)

add_btn = tk.Button(add_frame, text="✅ Add Quote", command=add_quote,
                    bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
                    relief="flat", width=20, height=2)
add_btn.pack(pady=15)

back_btn = tk.Button(add_frame, text="Back to Quotes", command=show_main_page,
                     bg="#607D8B", fg="white", font=("Arial", 10, "bold"),
                     relief="flat", width=20, height=2)
back_btn.pack(pady=5)

# ------------------ START APP ------------------
show_main_page()

show_random_quote()

root.mainloop()

