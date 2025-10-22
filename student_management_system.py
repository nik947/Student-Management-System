import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# ---------- Database Setup ----------
def connect_db():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll_no TEXT UNIQUE,
            name TEXT,
            email TEXT,
            gender TEXT,
            contact TEXT,
            dob TEXT,
            address TEXT
        )
    """)
    conn.commit()
    conn.close()

connect_db()

# ---------- Functions ----------
def add_student():
    if roll_no_var.get() == "" or name_var.get() == "":
        messagebox.showerror("Error", "All Fields Are Required!")
        return
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO student (roll_no, name, email, gender, contact, dob, address) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (roll_no_var.get(), name_var.get(), email_var.get(), gender_var.get(), contact_var.get(), dob_var.get(), address_text.get('1.0', tk.END)))
        conn.commit()
        messagebox.showinfo("Success", "Record Added Successfully")
        fetch_data()
        clear_fields()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Roll Number already exists!")
    conn.close()

def fetch_data():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student")
    rows = cursor.fetchall()
    if len(rows) != 0:
        student_table.delete(*student_table.get_children())
        for row in rows:
            student_table.insert('', tk.END, values=row)
    conn.close()

def clear_fields():
    roll_no_var.set("")
    name_var.set("")
    email_var.set("")
    gender_var.set("")
    contact_var.set("")
    dob_var.set("")
    address_text.delete("1.0", tk.END)

def get_cursor(event):
    cursor_row = student_table.focus()
    content = student_table.item(cursor_row)
    row = content["values"]
    if row:
        roll_no_var.set(row[1])
        name_var.set(row[2])
        email_var.set(row[3])
        gender_var.set(row[4])
        contact_var.set(row[5])
        dob_var.set(row[6])
        address_text.delete("1.0", tk.END)
        address_text.insert(tk.END, row[7])

def update_data():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE student SET 
        name=?, email=?, gender=?, contact=?, dob=?, address=? 
        WHERE roll_no=?
    """, (name_var.get(), email_var.get(), gender_var.get(), contact_var.get(), dob_var.get(), address_text.get('1.0', tk.END), roll_no_var.get()))
    conn.commit()
    messagebox.showinfo("Success", "Record Updated Successfully")
    fetch_data()
    clear_fields()
    conn.close()

def delete_data():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM student WHERE roll_no=?", (roll_no_var.get(),))
    conn.commit()
    messagebox.showinfo("Deleted", "Record Deleted Successfully")
    fetch_data()
    clear_fields()
    conn.close()

def search_data():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student WHERE " + search_by.get() + " LIKE ?", ('%' + search_txt.get() + '%',))
    rows = cursor.fetchall()
    if len(rows) != 0:
        student_table.delete(*student_table.get_children())
        for row in rows:
            student_table.insert('', tk.END, values=row)
    conn.close()

# ---------- GUI Setup ----------
root = tk.Tk()
root.title("Student Management System")
root.geometry("1050x600")
root.config(bg="#f0f0f0")

title = tk.Label(root, text="Student Management System", bd=10, relief=tk.GROOVE, font=("Helvetica", 22, "bold"), bg="lightblue", fg="black")
title.pack(side=tk.TOP, fill=tk.X)

# ---------- Variables ----------
roll_no_var = tk.StringVar()
name_var = tk.StringVar()
email_var = tk.StringVar()
gender_var = tk.StringVar()
contact_var = tk.StringVar()
dob_var = tk.StringVar()
search_by = tk.StringVar()
search_txt = tk.StringVar()

# ---------- Manage Frame ----------
Manage_Frame = tk.Frame(root, bd=4, relief=tk.RIDGE, bg="white")
Manage_Frame.place(x=20, y=80, width=450, height=500)

m_title = tk.Label(Manage_Frame, text="Manage Students", bg="white", font=("Helvetica", 20, "bold"))
m_title.grid(row=0, columnspan=2, pady=10)

lbl_roll = tk.Label(Manage_Frame, text="Roll No", bg="white", font=("Helvetica", 12))
lbl_roll.grid(row=1, column=0, pady=10, padx=20, sticky="w")
txt_roll = tk.Entry(Manage_Frame, textvariable=roll_no_var, font=("Helvetica", 12), bd=2, relief=tk.GROOVE)
txt_roll.grid(row=1, column=1, pady=10, padx=20, sticky="w")

lbl_name = tk.Label(Manage_Frame, text="Name", bg="white", font=("Helvetica", 12))
lbl_name.grid(row=2, column=0, pady=10, padx=20, sticky="w")
txt_name = tk.Entry(Manage_Frame, textvariable=name_var, font=("Helvetica", 12), bd=2, relief=tk.GROOVE)
txt_name.grid(row=2, column=1, pady=10, padx=20, sticky="w")

lbl_email = tk.Label(Manage_Frame, text="Email", bg="white", font=("Helvetica", 12))
lbl_email.grid(row=3, column=0, pady=10, padx=20, sticky="w")
txt_email = tk.Entry(Manage_Frame, textvariable=email_var, font=("Helvetica", 12), bd=2, relief=tk.GROOVE)
txt_email.grid(row=3, column=1, pady=10, padx=20, sticky="w")

lbl_gender = tk.Label(Manage_Frame, text="Gender", bg="white", font=("Helvetica", 12))
lbl_gender.grid(row=4, column=0, pady=10, padx=20, sticky="w")
combo_gender = ttk.Combobox(Manage_Frame, textvariable=gender_var, font=("Helvetica", 12), state="readonly")
combo_gender['values'] = ("Male", "Female", "Other")
combo_gender.grid(row=4, column=1, pady=10, padx=20, sticky="w")

lbl_contact = tk.Label(Manage_Frame, text="Contact", bg="white", font=("Helvetica", 12))
lbl_contact.grid(row=5, column=0, pady=10, padx=20, sticky="w")
txt_contact = tk.Entry(Manage_Frame, textvariable=contact_var, font=("Helvetica", 12), bd=2, relief=tk.GROOVE)
txt_contact.grid(row=5, column=1, pady=10, padx=20, sticky="w")

lbl_dob = tk.Label(Manage_Frame, text="D.O.B", bg="white", font=("Helvetica", 12))
lbl_dob.grid(row=6, column=0, pady=10, padx=20, sticky="w")
txt_dob = tk.Entry(Manage_Frame, textvariable=dob_var, font=("Helvetica", 12), bd=2, relief=tk.GROOVE)
txt_dob.grid(row=6, column=1, pady=10, padx=20, sticky="w")

lbl_address = tk.Label(Manage_Frame, text="Address", bg="white", font=("Helvetica", 12))
lbl_address.grid(row=7, column=0, pady=10, padx=20, sticky="w")
address_text = tk.Text(Manage_Frame, width=25, height=3, font=("Helvetica", 12))
address_text.grid(row=7, column=1, pady=10, padx=20, sticky="w")

# Buttons Frame
btn_frame = tk.Frame(Manage_Frame, bg="white")
btn_frame.place(x=10, y=420, width=420)

tk.Button(btn_frame, text="Add", width=10, command=add_student, bg="lightgreen").grid(row=0, column=0, padx=10, pady=10)
tk.Button(btn_frame, text="Update", width=10, command=update_data, bg="lightblue").grid(row=0, column=1, padx=10, pady=10)
tk.Button(btn_frame, text="Delete", width=10, command=delete_data, bg="salmon").grid(row=0, column=2, padx=10, pady=10)
tk.Button(btn_frame, text="Clear", width=10, command=clear_fields, bg="lightgray").grid(row=0, column=3, padx=10, pady=10)

# ---------- Detail Frame ----------
Detail_Frame = tk.Frame(root, bd=4, relief=tk.RIDGE, bg="white")
Detail_Frame.place(x=500, y=80, width=520, height=500)

lbl_search = tk.Label(Detail_Frame, text="Search By", bg="white", font=("Helvetica", 12))
lbl_search.grid(row=0, column=0, pady=10, padx=10, sticky="w")

combo_search = ttk.Combobox(Detail_Frame, textvariable=search_by, width=10, font=("Helvetica", 12), state="readonly")
combo_search['values'] = ("roll_no", "name", "contact")
combo_search.grid(row=0, column=1, pady=10, padx=10, sticky="w")

txt_search = tk.Entry(Detail_Frame, textvariable=search_txt, width=15, font=("Helvetica", 12), bd=2, relief=tk.GROOVE)
txt_search.grid(row=0, column=2, pady=10, padx=10, sticky="w")

tk.Button(Detail_Frame, text="Search", width=10, command=search_data, bg="lightblue").grid(row=0, column=3, padx=10, pady=10)
tk.Button(Detail_Frame, text="Show All", width=10, command=fetch_data, bg="lightgreen").grid(row=0, column=4, padx=10, pady=10)

# Table Frame
Table_Frame = tk.Frame(Detail_Frame, bd=4, relief=tk.RIDGE, bg="white")
Table_Frame.place(x=10, y=70, width=490, height=400)

scroll_x = tk.Scrollbar(Table_Frame, orient=tk.HORIZONTAL)
scroll_y = tk.Scrollbar(Table_Frame, orient=tk.VERTICAL)
student_table = ttk.Treeview(Table_Frame, columns=("id", "roll", "name", "email", "gender", "contact", "dob", "address"),
                             xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
scroll_x.config(command=student_table.xview)
scroll_y.config(command=student_table.yview)

student_table.heading("id", text="ID")
student_table.heading("roll", text="Roll No")
student_table.heading("name", text="Name")
student_table.heading("email", text="Email")
student_table.heading("gender", text="Gender")
student_table.heading("contact", text="Contact")
student_table.heading("dob", text="D.O.B")
student_table.heading("address", text="Address")
student_table["show"] = "headings"
student_table.pack(fill=tk.BOTH, expand=1)
student_table.bind("<ButtonRelease-1>", get_cursor)

fetch_data()

root.mainloop()
