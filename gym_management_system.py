import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# ==========================================
# DATABASE CONNECTION & TABLE INITIALIZATION
# ==========================================
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="vasss",
    database="gym",
    use_pure=True
)
cur = conn.cursor()

def init_db():
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(50) NOT NULL
    )""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS members (
        regdno INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        age INT,
        gender VARCHAR(20),
        membership VARCHAR(50),
        phone VARCHAR(20)
    )""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS trainers (
        trainer_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        specialization VARCHAR(100),
        phone VARCHAR(20),
        salary DECIMAL(10,2)
    )""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INT AUTO_INCREMENT PRIMARY KEY,
        member_id INT,
        check_in_date DATE,
        status VARCHAR(20),
        FOREIGN KEY (member_id) REFERENCES members(regdno) ON DELETE CASCADE
    )""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS payments (
        payment_id INT AUTO_INCREMENT PRIMARY KEY,
        member_id INT,
        amount DECIMAL(10,2),
        payment_date DATE,
        method VARCHAR(50),
        FOREIGN KEY (member_id) REFERENCES members(regdno) ON DELETE CASCADE
    )""")
    conn.commit()

init_db()

# ==========================================
# SIMPLE VALIDATION FUNCTIONS
# ==========================================
def check_name(name, field_name="Name"):
    name = name.strip()
    if name == "":
        return field_name + " is required."
    if len(name) > 100:
        return field_name + " is too long."
    if name.isdigit():
        return field_name + " cannot contain only numbers."
    return ""

def check_phone(phone):
    phone = phone.strip()
    if phone == "":
        return "Phone is required."
    if not phone.isdigit():
        return "Phone must contain digits only."
    if len(phone) < 10 or len(phone) > 15:
        return "Phone length must be between 10 and 15 digits."
    return ""

def check_member_exists(member_id):
    cur.execute("SELECT regdno FROM members WHERE regdno=%s", (member_id,))
    return cur.fetchone() is not None

def check_positive_number(value, field_name):
    if value.strip() == "":
        return field_name + " is required."
    try:
        amount = float(value)
    except ValueError:
        return field_name + " must be a number."
    if amount <= 0:
        return field_name + " must be greater than zero."
    return ""

def validate_member_values(name, age, gender, membership, phone):
    msg = check_name(name)
    if msg:
        return msg
    if age.strip() == "":
        return "Age is required."
    if not age.strip().isdigit():
        return "Age must be an integer."
    if int(age) < 10 or int(age) > 100:
        return "Age must be between 10 and 100."
    if gender.strip() not in ["Male", "Female", "Other"]:
        return "Please select a valid gender."
    if membership.strip() == "":
        return "Membership is required."
    return check_phone(phone)

def validate_trainer_values(name, specialization, phone, salary):
    msg = check_name(name)
    if msg:
        return msg
    if specialization.strip() == "":
        return "Specialization is required."
    msg = check_phone(phone)
    if msg:
        return msg
    return check_positive_number(salary, "Salary")

# ==========================================
# AUTHENTICATION WINDOW
# ==========================================
def open_login_window():
    auth_win = tk.Tk()
    auth_win.title("Gym System - Authentication")
    auth_win.geometry("400x350")
    auth_win.configure(bg="#1e1e1e")
    auth_win.resizable(False, False)

    user_var = tk.StringVar()
    pass_var = tk.StringVar()

    tk.Label(auth_win, text="WELCOME BACK", font=("Arial", 18, "bold"), bg="#0f3460", fg="white", pady=15).pack(fill=tk.X)

    fields_frame = tk.Frame(auth_win, bg="#1e1e1e")
    fields_frame.pack(pady=25)

    tk.Label(fields_frame, text="Username", font=("Arial", 11, "bold"), bg="#1e1e1e", fg="white").grid(row=0, column=0, sticky="w", pady=8, padx=5)
    tk.Entry(fields_frame, textvariable=user_var, font=("Arial", 11), width=22).grid(row=0, column=1, pady=8, padx=5)
    tk.Label(fields_frame, text="Password", font=("Arial", 11, "bold"), bg="#1e1e1e", fg="white").grid(row=1, column=0, sticky="w", pady=8, padx=5)
    tk.Entry(fields_frame, textvariable=pass_var, font=("Arial", 11), width=22, show="*").grid(row=1, column=1, pady=8, padx=5)

    def login_action():
        username = user_var.get().strip()
        password = pass_var.get()
        if username == "":
            messagebox.showerror("Error", "Username is required.", parent=auth_win)
            return
        if password == "":
            messagebox.showerror("Error", "Password is required.", parent=auth_win)
            return
        try:
            cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
            if cur.fetchone():
                messagebox.showinfo("Success", "Login Successful!", parent=auth_win)
                auth_win.destroy()
                load_main_window()
            else:
                messagebox.showerror("Error", "Invalid Username or Password.", parent=auth_win)
        except Exception as e:
            messagebox.showerror("Error", "Login failed.\n" + str(e), parent=auth_win)

    def register_action():
        username = user_var.get()
        password = pass_var.get()
        if username == "":
            messagebox.showerror("Error", "Username is required.", parent=auth_win)
            return
        if username != username.strip():
            messagebox.showerror("Error", "Username must not have leading or trailing spaces.", parent=auth_win)
            return
        if len(username) < 4 or len(username) > 50:
            messagebox.showerror("Error", "Username length must be between 4 and 50.", parent=auth_win)
            return
        if password == "":
            messagebox.showerror("Error", "Password is required.", parent=auth_win)
            return
        if len(password) < 4 or len(password) > 50:
            messagebox.showerror("Error", "Password length must be between 4 and 50.", parent=auth_win)
            return
        try:
            cur.execute("SELECT id FROM users WHERE username=%s", (username,))
            if cur.fetchone():
                messagebox.showerror("Error", "Username already exists.", parent=auth_win)
                return
            cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            messagebox.showinfo("Success", "Registration Successful! You can now log in.", parent=auth_win)
        except Exception as e:
            messagebox.showerror("Error", "Registration failed.\n" + str(e), parent=auth_win)

    btn_box = tk.Frame(auth_win, bg="#1e1e1e")
    btn_box.pack(pady=10)
    tk.Button(btn_box, text="Login", bg="#007bff", fg="white", font=("Arial", 11, "bold"), width=12, command=login_action).grid(row=0, column=0, padx=10)
    tk.Button(btn_box, text="Register", bg="#28a745", fg="white", font=("Arial", 11, "bold"), width=12, command=register_action).grid(row=0, column=1, padx=10)
    auth_win.mainloop()

# ==========================================
# MAIN APPLICATION WINDOW & MODULES
# ==========================================
def load_main_window():
    root = tk.Tk()
    root.title("Gym Management System - Professional Edition")
    root.geometry("1000x700")
    root.configure(bg="#1e1e1e")

    tk.Label(root, text="GYM MANAGEMENT SYSTEM", font=("Arial", 20, "bold"), bg="#0f3460", fg="white", pady=10).pack(fill=tk.X)

    style = ttk.Style()
    style.theme_use("default")
    style.configure("TNotebook", background="#1e1e1e", borderwidth=0)
    style.configure("TNotebook.Tab", background="#2a2a2a", foreground="white", padding=[15, 5], font=('Arial', 10, 'bold'))
    style.map("TNotebook.Tab", background=[("selected", "#007bff")])

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both", padx=10, pady=10)

    tab_dash = tk.Frame(notebook, bg="#1e1e1e")
    tab_members = tk.Frame(notebook, bg="#1e1e1e")
    tab_trainers = tk.Frame(notebook, bg="#1e1e1e")
    tab_attendance = tk.Frame(notebook, bg="#1e1e1e")
    tab_payments = tk.Frame(notebook, bg="#1e1e1e")
    notebook.add(tab_dash, text="Dashboard")
    notebook.add(tab_members, text="Members")
    notebook.add(tab_trainers, text="Trainers")
    notebook.add(tab_attendance, text="Attendance")
    notebook.add(tab_payments, text="Payments")

    def refresh_dashboard():
        for widget in tab_dash.winfo_children():
            widget.destroy()
        try:
            cur.execute("SELECT COUNT(*) FROM members")
            m_count = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM trainers")
            t_count = cur.fetchone()[0]
            cur.execute("SELECT IFNULL(SUM(amount), 0) FROM payments")
            rev_count = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM attendance WHERE check_in_date = CURDATE()")
            att_count = cur.fetchone()[0]
        except Exception:
            m_count = t_count = att_count = 0
            rev_count = 0
        stats = [("Total Members", m_count, "#17a2b8"), ("Active Trainers", t_count, "#28a745"), ("Today's Check-ins", att_count, "#ffc107"), ("Total Revenue ($)", f"${rev_count:,.2f}", "#dc3545")]
        grid_frame = tk.Frame(tab_dash, bg="#1e1e1e")
        grid_frame.pack(pady=40)
        for i, (title, val, color) in enumerate(stats):
            box = tk.Frame(grid_frame, bg=color, width=200, height=120)
            box.grid(row=i//2, column=i%2, padx=20, pady=20)
            box.pack_propagate(False)
            tk.Label(box, text=title, font=("Arial", 12, "bold"), bg=color, fg="white").pack(pady=10)
            tk.Label(box, text=str(val), font=("Arial", 18, "bold"), bg=color, fg="white").pack()

    notebook.bind("<<NotebookTabChanged>>", lambda e: refresh_dashboard() if notebook.index("current") == 0 else None)

    # ------------------ 2. MEMBERS MODULE ------------------
    m_id, m_name, m_age, m_gender, m_ship, m_phone = tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(value="Male"), tk.StringVar(), tk.StringVar()
    m_selected = tk.StringVar()
    m_frame = tk.Frame(tab_members, bg="#1e1e1e")
    m_frame.pack(pady=10)
    fields = [("Name", m_name, None), ("Age", m_age, None), ("Gender", m_gender, ["Male", "Female", "Other"]), ("Membership", m_ship, None), ("Phone", m_phone, None)]
    for idx, (label, var, vals) in enumerate(fields):
        tk.Label(m_frame, text=label, fg="white", bg="#1e1e1e", font=("Arial", 10, "bold")).grid(row=idx//3, column=(idx%3)*2, padx=5, pady=5)
        if vals:
            ttk.Combobox(m_frame, textvariable=var, values=vals, width=18, state="readonly").grid(row=idx//3, column=(idx%3)*2+1, padx=5, pady=5)
        else:
            tk.Entry(m_frame, textvariable=var, width=20).grid(row=idx//3, column=(idx%3)*2+1, padx=5, pady=5)

    btn_f = tk.Frame(tab_members, bg="#1e1e1e")
    btn_f.pack(pady=10)
    m_table_frame = tk.Frame(tab_members, bg="white")
    m_table_frame.pack(fill="both", expand=True, padx=10, pady=10)
    m_canvas = tk.Canvas(m_table_frame, bg="white", highlightthickness=0)
    m_scroll = tk.Scrollbar(m_table_frame, orient="vertical", command=m_canvas.yview)
    m_canvas.configure(yscrollcommand=m_scroll.set)
    m_scroll.pack(side="right", fill="y")
    m_canvas.pack(side="left", fill="both", expand=True)
    m_rows = tk.Frame(m_canvas, bg="white")
    m_canvas.create_window((0, 0), window=m_rows, anchor="nw")
    m_rows.bind("<Configure>", lambda e: m_canvas.configure(scrollregion=m_canvas.bbox("all")))

    def clear_m_fields():
        m_id.set(""); m_selected.set("")
        for var in [m_name, m_age, m_ship, m_phone]: var.set("")
        m_gender.set("Male")
        fetch_members()

    def select_member_row(row):
        if m_selected.get() == str(row[0]):
            clear_m_fields(); return
        m_selected.set(str(row[0])); m_id.set(str(row[0])); m_name.set(str(row[1])); m_age.set(str(row[2])); m_gender.set(str(row[3])); m_ship.set(str(row[4])); m_phone.set(str(row[5]))
        fetch_members()

    def fetch_members():
        for widget in m_rows.winfo_children(): widget.destroy()
        heads = ["ID", "Name", "Age", "Gender", "Membership", "Phone"]
        widths = [10, 24, 12, 16, 24, 18]
        for c, h in enumerate(heads):
            tk.Label(m_rows, text=h, bg="#2a2a2a", fg="white", width=widths[c], relief="ridge", font=("Arial", 10, "bold")).grid(row=0, column=c, sticky="nsew")
        try:
            cur.execute("SELECT * FROM members")
            data = cur.fetchall()
            for r, row in enumerate(data, start=1):
                color = "#cce5ff" if m_selected.get() == str(row[0]) else "white"
                for c, val in enumerate(row):
                    lab = tk.Label(m_rows, text=str(val), bg=color, fg="black", width=widths[c], relief="ridge", font=("Arial", 10))
                    lab.grid(row=r, column=c, sticky="nsew")
                    lab.bind("<Button-1>", lambda e, x=row: select_member_row(x))
        except Exception as e:
            messagebox.showerror("Error", "Cannot load members.\n" + str(e))

    def add_member():
        msg = validate_member_values(m_name.get(), m_age.get(), m_gender.get(), m_ship.get(), m_phone.get())
        if msg: messagebox.showerror("Error", msg); return
        try:
            cur.execute("INSERT INTO members (name, age, gender, membership, phone) VALUES (%s,%s,%s,%s,%s)", (m_name.get().strip(), int(m_age.get()), m_gender.get(), m_ship.get().strip(), m_phone.get().strip()))
            conn.commit(); fetch_members(); clear_m_fields(); messagebox.showinfo("Success", "Member Added Successfully")
        except Exception as e: messagebox.showerror("Error", "Member could not be added.\n" + str(e))

    def update_member():
        if m_id.get() == "": messagebox.showerror("Error", "Select a member to update"); return
        msg = validate_member_values(m_name.get(), m_age.get(), m_gender.get(), m_ship.get(), m_phone.get())
        if msg: messagebox.showerror("Error", msg); return
        try:
            cur.execute("UPDATE members SET name=%s, age=%s, gender=%s, membership=%s, phone=%s WHERE regdno=%s", (m_name.get().strip(), int(m_age.get()), m_gender.get(), m_ship.get().strip(), m_phone.get().strip(), m_id.get()))
            conn.commit(); fetch_members(); clear_m_fields(); messagebox.showinfo("Success", "Member Updated Successfully")
        except Exception as e: messagebox.showerror("Error", "Member could not be updated.\n" + str(e))

    def delete_member():
        if m_id.get() == "": messagebox.showerror("Error", "Select a member to delete"); return
        if not messagebox.askyesno("Confirm", "Delete selected member?"): return
        try:
            cur.execute("DELETE FROM members WHERE regdno=%s", (m_id.get(),)); conn.commit(); fetch_members(); clear_m_fields(); messagebox.showinfo("Success", "Member Deleted Successfully")
        except Exception as e: messagebox.showerror("Error", "Member could not be deleted.\n" + str(e))

    tk.Button(btn_f, text="Add Member", bg="#28a745", fg="white", command=add_member, width=12).grid(row=0, column=0, padx=5)
    tk.Button(btn_f, text="Update", bg="#007bff", fg="white", command=update_member, width=12).grid(row=0, column=1, padx=5)
    tk.Button(btn_f, text="Delete", bg="#dc3545", fg="white", command=delete_member, width=12).grid(row=0, column=2, padx=5)
    tk.Button(btn_f, text="Clear", bg="#6c757d", fg="white", command=clear_m_fields, width=12).grid(row=0, column=3, padx=5)
    fetch_members()

    # ------------------ 3. TRAINERS MODULE ------------------
    t_id, t_name, t_spec, t_phone, t_sal = tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()
    t_selected = tk.StringVar()
    t_frame = tk.Frame(tab_trainers, bg="#1e1e1e")
    t_frame.pack(pady=10)
    t_fields = [("Name", t_name), ("Specialization", t_spec), ("Phone", t_phone), ("Salary", t_sal)]
    for idx, (label, var) in enumerate(t_fields):
        tk.Label(t_frame, text=label, fg="white", bg="#1e1e1e", font=("Arial", 10, "bold")).grid(row=idx//3, column=(idx%3)*2, padx=5, pady=5)
        tk.Entry(t_frame, textvariable=var, width=20).grid(row=idx//3, column=(idx%3)*2+1, padx=5, pady=5)
    t_btn_f = tk.Frame(tab_trainers, bg="#1e1e1e")
    t_btn_f.pack(pady=10)
    t_table_frame = tk.Frame(tab_trainers, bg="white")
    t_table_frame.pack(fill="both", expand=True, padx=10, pady=10)
    t_canvas = tk.Canvas(t_table_frame, bg="white", highlightthickness=0)
    t_scroll = tk.Scrollbar(t_table_frame, orient="vertical", command=t_canvas.yview)
    t_canvas.configure(yscrollcommand=t_scroll.set)
    t_scroll.pack(side="right", fill="y"); t_canvas.pack(side="left", fill="both", expand=True)
    t_rows = tk.Frame(t_canvas, bg="white"); t_canvas.create_window((0, 0), window=t_rows, anchor="nw")
    t_rows.bind("<Configure>", lambda e: t_canvas.configure(scrollregion=t_canvas.bbox("all")))

    def clear_t_fields():
        t_selected.set("")
        for var in [t_id, t_name, t_spec, t_phone, t_sal]: var.set("")
        fetch_trainers()
    def select_trainer_row(row):
        if t_selected.get() == str(row[0]): clear_t_fields(); return
        t_selected.set(str(row[0])); t_id.set(str(row[0])); t_name.set(str(row[1])); t_spec.set(str(row[2])); t_phone.set(str(row[3])); t_sal.set(str(row[4])); fetch_trainers()
    def fetch_trainers():
        for widget in t_rows.winfo_children(): widget.destroy()
        heads = ["ID", "Name", "Specialization", "Phone", "Salary"]; widths = [10, 28, 28, 18, 16]
        for c, h in enumerate(heads): tk.Label(t_rows, text=h, bg="#2a2a2a", fg="white", width=widths[c], relief="ridge", font=("Arial", 10, "bold")).grid(row=0, column=c, sticky="nsew")
        try:
            cur.execute("SELECT * FROM trainers")
            for r, row in enumerate(cur.fetchall(), start=1):
                color = "#cce5ff" if t_selected.get() == str(row[0]) else "white"
                for c, val in enumerate(row):
                    lab = tk.Label(t_rows, text=str(val), bg=color, fg="black", width=widths[c], relief="ridge", font=("Arial", 10)); lab.grid(row=r, column=c, sticky="nsew"); lab.bind("<Button-1>", lambda e, x=row: select_trainer_row(x))
        except Exception as e: messagebox.showerror("Error", "Cannot load trainers.\n" + str(e))
    def add_trainer():
        msg = validate_trainer_values(t_name.get(), t_spec.get(), t_phone.get(), t_sal.get())
        if msg: messagebox.showerror("Error", msg); return
        try:
            cur.execute("INSERT INTO trainers (name, specialization, phone, salary) VALUES (%s,%s,%s,%s)", (t_name.get().strip(), t_spec.get().strip(), t_phone.get().strip(), float(t_sal.get()))); conn.commit(); fetch_trainers(); clear_t_fields(); messagebox.showinfo("Success", "Trainer Added Successfully")
        except Exception as e: messagebox.showerror("Error", "Trainer could not be added.\n" + str(e))
    def update_trainer():
        if t_id.get() == "": messagebox.showerror("Error", "Select a trainer to update"); return
        msg = validate_trainer_values(t_name.get(), t_spec.get(), t_phone.get(), t_sal.get())
        if msg: messagebox.showerror("Error", msg); return
        try:
            cur.execute("UPDATE trainers SET name=%s, specialization=%s, phone=%s, salary=%s WHERE trainer_id=%s", (t_name.get().strip(), t_spec.get().strip(), t_phone.get().strip(), float(t_sal.get()), t_id.get())); conn.commit(); fetch_trainers(); clear_t_fields(); messagebox.showinfo("Success", "Trainer Updated Successfully")
        except Exception as e: messagebox.showerror("Error", "Trainer could not be updated.\n" + str(e))
    def delete_trainer():
        if t_id.get() == "": messagebox.showerror("Error", "Select a trainer to delete"); return
        if not messagebox.askyesno("Confirm", "Delete selected trainer?"): return
        try:
            cur.execute("DELETE FROM trainers WHERE trainer_id=%s", (t_id.get(),)); conn.commit(); fetch_trainers(); clear_t_fields(); messagebox.showinfo("Success", "Trainer Deleted Successfully")
        except Exception as e: messagebox.showerror("Error", "Trainer could not be deleted.\n" + str(e))
    tk.Button(t_btn_f, text="Add Trainer", bg="#28a745", fg="white", command=add_trainer, width=12).grid(row=0, column=0, padx=5)
    tk.Button(t_btn_f, text="Update", bg="#007bff", fg="white", command=update_trainer, width=12).grid(row=0, column=1, padx=5)
    tk.Button(t_btn_f, text="Delete", bg="#dc3545", fg="white", command=delete_trainer, width=12).grid(row=0, column=2, padx=5)
    tk.Button(t_btn_f, text="Clear", bg="#6c757d", fg="white", command=clear_t_fields, width=12).grid(row=0, column=3, padx=5)
    fetch_trainers()

    # ------------------ 4. ATTENDANCE MODULE ------------------
    att_m_id = tk.StringVar(); att_status = tk.StringVar(value="Present")
    att_f = tk.Frame(tab_attendance, bg="#1e1e1e"); att_f.pack(pady=10)
    tk.Label(att_f, text="Member ID", fg="white", bg="#1e1e1e", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5)
    tk.Entry(att_f, textvariable=att_m_id, width=15).grid(row=0, column=1, padx=5)
    tk.Label(att_f, text="Status", fg="white", bg="#1e1e1e", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=5)
    ttk.Combobox(att_f, textvariable=att_status, values=["Present", "Absent"], width=12, state="readonly").grid(row=0, column=3, padx=5)
    att_table_frame = tk.Frame(tab_attendance, bg="white"); att_table_frame.pack(fill="both", expand=True, padx=10, pady=10)
    att_canvas = tk.Canvas(att_table_frame, bg="white", highlightthickness=0); att_scroll = tk.Scrollbar(att_table_frame, orient="vertical", command=att_canvas.yview); att_canvas.configure(yscrollcommand=att_scroll.set); att_scroll.pack(side="right", fill="y"); att_canvas.pack(side="left", fill="both", expand=True)
    att_rows = tk.Frame(att_canvas, bg="white"); att_canvas.create_window((0, 0), window=att_rows, anchor="nw"); att_rows.bind("<Configure>", lambda e: att_canvas.configure(scrollregion=att_canvas.bbox("all")))
    def fetch_attendance():
        for widget in att_rows.winfo_children(): widget.destroy()
        heads = ["Record ID", "Member ID", "Date", "Status"]; widths = [20, 20, 28, 20]
        for c, h in enumerate(heads): tk.Label(att_rows, text=h, bg="#2a2a2a", fg="white", width=widths[c], relief="ridge", font=("Arial", 10, "bold")).grid(row=0, column=c, sticky="nsew")
        try:
            cur.execute("SELECT * FROM attendance ORDER BY check_in_date DESC")
            for r, row in enumerate(cur.fetchall(), start=1):
                for c, val in enumerate(row): tk.Label(att_rows, text=str(val), bg="white", fg="black", width=widths[c], relief="ridge", font=("Arial", 10)).grid(row=r, column=c, sticky="nsew")
        except Exception as e: messagebox.showerror("Error", "Cannot load attendance.\n" + str(e))
    def mark_attendance():
        mid = att_m_id.get().strip()
        if mid == "": messagebox.showerror("Error", "Member ID is required."); return
        if not mid.isdigit(): messagebox.showerror("Error", "Member ID must be an integer."); return
        try:
            if not check_member_exists(mid): messagebox.showerror("Error", "Member ID does not exist."); return
            cur.execute("SELECT id FROM attendance WHERE member_id=%s AND check_in_date=CURDATE()", (mid,))
            if cur.fetchone(): messagebox.showerror("Error", "Attendance already recorded for this member today."); return
            cur.execute("INSERT INTO attendance (member_id, check_in_date, status) VALUES (%s, CURDATE(), %s)", (mid, att_status.get())); conn.commit(); fetch_attendance(); att_m_id.set(""); messagebox.showinfo("Success", "Attendance Recorded Successfully")
        except Exception as e: messagebox.showerror("Error", "Attendance could not be recorded.\n" + str(e))
    tk.Button(att_f, text="Mark Attendance", bg="#007bff", fg="white", command=mark_attendance).grid(row=0, column=4, padx=10)
    fetch_attendance()

    # ------------------ 5. PAYMENTS MODULE ------------------
    p_m_id, p_amt, p_method = tk.StringVar(), tk.StringVar(), tk.StringVar(value="Cash")
    p_f = tk.Frame(tab_payments, bg="#1e1e1e"); p_f.pack(pady=10)
    tk.Label(p_f, text="Member ID", fg="white", bg="#1e1e1e", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5)
    tk.Entry(p_f, textvariable=p_m_id, width=15).grid(row=0, column=1, padx=5)
    tk.Label(p_f, text="Amount ($)", fg="white", bg="#1e1e1e", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=5)
    tk.Entry(p_f, textvariable=p_amt, width=15).grid(row=0, column=3, padx=5)
    tk.Label(p_f, text="Method", fg="white", bg="#1e1e1e", font=("Arial", 10, "bold")).grid(row=0, column=4, padx=5)
    ttk.Combobox(p_f, textvariable=p_method, values=["Cash", "Credit Card", "Debit Card", "UPI"], width=12, state="readonly").grid(row=0, column=5, padx=5)
    p_table_frame = tk.Frame(tab_payments, bg="white"); p_table_frame.pack(fill="both", expand=True, padx=10, pady=10)
    p_canvas = tk.Canvas(p_table_frame, bg="white", highlightthickness=0); p_scroll = tk.Scrollbar(p_table_frame, orient="vertical", command=p_canvas.yview); p_canvas.configure(yscrollcommand=p_scroll.set); p_scroll.pack(side="right", fill="y"); p_canvas.pack(side="left", fill="both", expand=True)
    p_rows = tk.Frame(p_canvas, bg="white"); p_canvas.create_window((0, 0), window=p_rows, anchor="nw"); p_rows.bind("<Configure>", lambda e: p_canvas.configure(scrollregion=p_canvas.bbox("all")))
    def fetch_payments():
        for widget in p_rows.winfo_children(): widget.destroy()
        heads = ["Payment ID", "Member ID", "Amount", "Date", "Method"]; widths = [18, 18, 18, 24, 20]
        for c, h in enumerate(heads): tk.Label(p_rows, text=h, bg="#2a2a2a", fg="white", width=widths[c], relief="ridge", font=("Arial", 10, "bold")).grid(row=0, column=c, sticky="nsew")
        try:
            cur.execute("SELECT * FROM payments ORDER BY payment_date DESC")
            for r, row in enumerate(cur.fetchall(), start=1):
                for c, val in enumerate(row): tk.Label(p_rows, text=str(val), bg="white", fg="black", width=widths[c], relief="ridge", font=("Arial", 10)).grid(row=r, column=c, sticky="nsew")
        except Exception as e: messagebox.showerror("Error", "Cannot load payments.\n" + str(e))
    def record_payment():
        mid = p_m_id.get().strip(); amount = p_amt.get().strip(); method = p_method.get().strip()
        if mid == "": messagebox.showerror("Error", "Member ID is required."); return
        if not mid.isdigit(): messagebox.showerror("Error", "Member ID must be an integer."); return
        msg = check_positive_number(amount, "Amount")
        if msg: messagebox.showerror("Error", msg); return
        if method not in ["Cash", "Credit Card", "Debit Card", "UPI"]: messagebox.showerror("Error", "Please select a payment method."); return
        try:
            if not check_member_exists(mid): messagebox.showerror("Error", "Member ID does not exist."); return
            cur.execute("INSERT INTO payments (member_id, amount, payment_date, method) VALUES (%s, %s, CURDATE(), %s)", (mid, float(amount), method)); conn.commit(); fetch_payments(); p_m_id.set(""); p_amt.set(""); p_method.set("Cash"); messagebox.showinfo("Success", "Payment Recorded Successfully")
        except Exception as e: messagebox.showerror("Error", "Payment could not be recorded.\n" + str(e))
    tk.Button(p_f, text="Record Payment", bg="#28a745", fg="white", command=record_payment).grid(row=0, column=6, padx=10)
    fetch_payments(); refresh_dashboard(); root.mainloop()

# ==========================================
# APPLICATION ENTRYPOINT
# ==========================================
if __name__ == "__main__":
    open_login_window()
    try:
        cur.close(); conn.close()
    except Exception:
        pass
