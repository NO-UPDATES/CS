from tkinter import *
from tkinter import messagebox
import mysql.connector
from datetime import datetime

# Global variables used by beginner-level functions
con = None
cur = None
current_log_id = None


def db_connect():
    """Create MySQL connection once and reuse in all windows."""
    global con, cur
    try:
        # Connect to local MySQL gym database
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="gym"
        )
        # Create cursor object to run SQL statements
        cur = con.cursor()
    except Exception as e:
        messagebox.showerror("Database Error", "Database Connection Error\n" + str(e))


def load_trainers(lb):
    # Load trainers from MySQL and show in Listbox
    lb.delete(0, END)
    cur.execute("select trainername, specialization, rating from trainers")
    data = cur.fetchall()
    for i in data:
        lb.insert(END, str(i[0]) + " - " + str(i[1]) + " - " + str(i[2]))


def load_items(lb):
    # Load item name and quantity from MySQL and show in Listbox
    lb.delete(0, END)
    cur.execute("select itemname, quantity from items")
    data = cur.fetchall()
    for i in data:
        lb.insert(END, str(i[0]) + " - " + str(i[1]))


def open_new_customer_window():
    w = Toplevel(root)
    w.title("New Customer Window")
    w.geometry("500x600")
    w.configure(bg="black")

    Label(w, text="WELCOME NEW CUSTOMER", bg="black", fg="red", font=("Arial", 16, "bold")).pack(pady=8)

    f1 = Frame(w, bg="black")
    f1.pack(pady=10)
    Label(f1, text="TRAINERS", bg="black", fg="white", font=("Arial", 12, "bold")).pack()
    lb1 = Listbox(f1, width=55, height=8)
    lb1.pack()
    load_trainers(lb1)

    f2 = Frame(w, bg="black")
    f2.pack(pady=10)
    Label(f2, text="GYM ITEMS", bg="black", fg="white", font=("Arial", 12, "bold")).pack()
    lb2 = Listbox(f2, width=55, height=10)
    lb2.pack()
    load_items(lb2)


def register_window():
    rw = Toplevel(root)
    rw.title("Register")
    rw.geometry("500x600")
    rw.configure(bg="black")

    Label(rw, text="MEMBER REGISTRATION", bg="black", fg="red", font=("Arial", 16, "bold")).pack(pady=10)

    f = Frame(rw, bg="black")
    f.pack()

    Label(f, text="Name", bg="black", fg="white").grid(row=0, column=0, padx=10, pady=6)
    e1 = Entry(f)
    e1.grid(row=0, column=1, padx=10, pady=6)

    Label(f, text="Regd No", bg="black", fg="white").grid(row=1, column=0, padx=10, pady=6)
    e2 = Entry(f)
    e2.grid(row=1, column=1, padx=10, pady=6)

    Label(f, text="Age", bg="black", fg="white").grid(row=2, column=0, padx=10, pady=6)
    e3 = Entry(f)
    e3.grid(row=2, column=1, padx=10, pady=6)

    Label(f, text="Phone", bg="black", fg="white").grid(row=3, column=0, padx=10, pady=6)
    e4 = Entry(f)
    e4.grid(row=3, column=1, padx=10, pady=6)

    Label(f, text="Gender", bg="black", fg="white").grid(row=4, column=0, padx=10, pady=6)
    g = StringVar()
    g.set("Male")
    Radiobutton(f, text="Male", variable=g, value="Male", bg="black", fg="white", selectcolor="black").grid(row=4, column=1)
    Radiobutton(f, text="Female", variable=g, value="Female", bg="black", fg="white", selectcolor="black").grid(row=5, column=1)

    Label(f, text="Membership", bg="black", fg="white").grid(row=6, column=0, padx=10, pady=6)
    c1 = IntVar()
    c2 = IntVar()
    c3 = IntVar()
    c4 = IntVar()
    c5 = IntVar()
    Checkbutton(f, text="Cardio", variable=c1, bg="black", fg="white", selectcolor="black").grid(row=6, column=1)
    Checkbutton(f, text="Weight Training", variable=c2, bg="black", fg="white", selectcolor="black").grid(row=7, column=1)
    Checkbutton(f, text="Steam Bath", variable=c3, bg="black", fg="white", selectcolor="black").grid(row=8, column=1)
    Checkbutton(f, text="Personal Training", variable=c4, bg="black", fg="white", selectcolor="black").grid(row=9, column=1)
    Checkbutton(f, text="Yoga Sessions", variable=c5, bg="black", fg="white", selectcolor="black").grid(row=10, column=1)

    def submit_register():
        n = e1.get().strip()
        r = e2.get().strip()
        a = e3.get().strip()
        p = e4.get().strip()

        if n == "" or r == "" or a == "" or p == "":
            messagebox.showerror("Error", "Empty Field Warning")
            return

        m = []
        if c1.get() == 1:
            m.append("Cardio")
        if c2.get() == 1:
            m.append("Weight Training")
        if c3.get() == 1:
            m.append("Steam Bath")
        if c4.get() == 1:
            m.append("Personal Training")
        if c5.get() == 1:
            m.append("Yoga Sessions")

        mem = ", ".join(m)
        if mem == "":
            mem = "Cardio"

        try:
            cur.execute("insert into members(regdno,name,age,gender,phone,membership) values(%s,%s,%s,%s,%s,%s)", (r, n, int(a), g.get(), p, mem))
            cur.execute("insert into payments(regdno,paymentstatus) values(%s,%s)", (r, "NOT PAID"))
            con.commit()
            messagebox.showinfo("Success", "Registration Successful")
            open_new_customer_window()
            rw.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    Button(rw, text="Submit", bg="green", fg="white", width=15, command=submit_register).pack(pady=15)


def customer_window(nm, reg):
    global current_log_id
    cw = Toplevel(root)
    cw.title("Customer Dashboard")
    cw.geometry("500x600")
    cw.configure(bg="black")

    Label(cw, text="CUSTOMER DASHBOARD", bg="black", fg="red", font=("Arial", 16, "bold")).pack(pady=8)

    cur.execute("select name, regdno, membership from members where name=%s and regdno=%s", (nm, reg))
    d = cur.fetchone()
    cur.execute("select paymentstatus from payments where regdno=%s", (reg,))
    p = cur.fetchone()

    f1 = Frame(cw, bg="black")
    f1.pack(pady=8)
    Label(f1, text="Name: " + str(d[0]), bg="black", fg="white").pack()
    Label(f1, text="Regd No: " + str(d[1]), bg="black", fg="white").pack()
    Label(f1, text="Membership: " + str(d[2]), bg="black", fg="white").pack()

    Label(cw, text="Payment Status: " + str(p[0]), bg="black", fg="white", font=("Arial", 12, "bold")).pack(pady=6)

    intime = datetime.now()
    cur.execute("insert into logs(regdno,intime,outtime) values(%s,%s,%s)", (reg, intime, None))
    con.commit()
    current_log_id = cur.lastrowid

    Label(cw, text="Weekly Logs (Last 7 Days)", bg="black", fg="red", font=("Arial", 12, "bold")).pack(pady=6)
    f2 = Frame(cw, bg="black")
    f2.pack(pady=4)
    cur.execute("select intime,outtime from logs where regdno=%s and intime >= NOW() - INTERVAL 7 DAY", (reg,))
    logs = cur.fetchall()
    if len(logs) == 0:
        Label(f2, text="No logs found", bg="black", fg="white").pack()
    else:
        for i in logs:
            Label(f2, text="In: " + str(i[0]) + "  Out: " + str(i[1]), bg="black", fg="white").pack()

    def c_exit():
        ans = messagebox.askyesno("Exit", "Are you sure you want to exit?")
        if ans:
            outtime = datetime.now()
            if current_log_id is not None:
                cur.execute("update logs set outtime=%s where logid=%s", (outtime, current_log_id))
                con.commit()
            cw.destroy()

    Button(cw, text="Exit", bg="green", fg="white", width=15, command=c_exit).pack(pady=10)


def admin_window():
    aw = Toplevel(root)
    aw.title("Admin Dashboard")
    aw.geometry("500x600")
    aw.configure(bg="black")

    Label(aw, text="ADMIN DASHBOARD", bg="black", fg="red", font=("Arial", 16, "bold")).pack(pady=6)
    Label(aw, text="Gym Timing: 5:00 AM to 10:00 PM", bg="black", fg="white").pack()

    f1 = Frame(aw, bg="black")
    f1.pack(pady=5)

    t = Text(f1, width=62, height=24)
    t.pack()

    def load_all():
        t.delete("1.0", END)
        t.insert(END, "MEMBERS TABLE\n")
        cur.execute("select * from members")
        for i in cur.fetchall():
            t.insert(END, str(i) + "\n")

        t.insert(END, "\nITEMS TABLE\n")
        cur.execute("select * from items")
        for i in cur.fetchall():
            t.insert(END, str(i) + "\n")

        t.insert(END, "\nTRAINERS TABLE\n")
        cur.execute("select * from trainers")
        for i in cur.fetchall():
            t.insert(END, str(i) + "\n")

        t.insert(END, "\nPAYMENTS TABLE\n")
        cur.execute("select * from payments")
        for i in cur.fetchall():
            t.insert(END, str(i) + "\n")

        t.insert(END, "\nLOGS TABLE\n")
        cur.execute("select * from logs")
        for i in cur.fetchall():
            t.insert(END, str(i) + "\n")

    load_all()

    f2 = Frame(aw, bg="black")
    f2.pack(pady=6)
    Label(f2, text="Item Name", bg="black", fg="white").grid(row=0, column=0)
    e1 = Entry(f2)
    e1.grid(row=0, column=1)
    Label(f2, text="New Qty", bg="black", fg="white").grid(row=1, column=0)
    e2 = Entry(f2)
    e2.grid(row=1, column=1)

    def update_item():
        name = e1.get().strip()
        qty = e2.get().strip()
        if name == "" or qty == "":
            messagebox.showerror("Error", "Empty Field Warning")
            return
        if not qty.isdigit():
            messagebox.showerror("Error", "Invalid Quantity")
            return

        cur.execute("select quantity from items where itemname=%s", (name,))
        old = cur.fetchone()
        if old is None:
            messagebox.showerror("Error", "Item not found")
            return

        oldq = old[0]
        cur.execute("update items set quantity=%s where itemname=%s", (int(qty), name))
        con.commit()
        dt = datetime.now()
        messagebox.showinfo("Info", "Item Updated Successfully\nItem: " + name + "\nOld Quantity: " + str(oldq) + "\nNew Quantity: " + str(qty) + "\nUpdated On: " + str(dt))
        load_all()

    Button(aw, text="Update Item Quantity", bg="green", fg="white", command=update_item).pack(pady=5)


def admin_login():
    u = e_name.get().strip()
    p = e_pass.get().strip()
    if u == "" or p == "":
        messagebox.showerror("Error", "Empty Field Warning")
        return
    cur.execute("select * from admin where username=%s and password=%s", (u, p))
    d = cur.fetchone()
    if d is None:
        messagebox.showerror("Error", "Invalid Login")
    else:
        messagebox.showinfo("Success", "Login Successful")
        admin_window()


def customer_login():
    n = e_name.get().strip()
    r = e_reg.get().strip()
    if n == "" or r == "":
        messagebox.showerror("Error", "Empty Field Warning")
        return
    cur.execute("select * from members where name=%s and regdno=%s", (n, r))
    d = cur.fetchone()
    if d is None:
        messagebox.showerror("Error", "Invalid Login")
    else:
        messagebox.showinfo("Success", "Login Successful")
        customer_window(n, r)


def app_exit():
    ans = messagebox.askyesno("Exit", "Are you sure you want to exit?")
    if ans:
        root.destroy()


# Main login window
root = Tk()
root.title("GYM MANAGEMENT SYSTEM")
root.geometry("500x600")
root.configure(bg="black")

db_connect()

Label(root, text="GYM MANAGEMENT SYSTEM", bg="black", fg="red", font=("Arial", 18, "bold")).pack(pady=20)

f_main = Frame(root, bg="black")
f_main.pack(pady=20)

Label(f_main, text="Name", bg="black", fg="white").grid(row=0, column=0, padx=10, pady=8)
e_name = Entry(f_main)
e_name.grid(row=0, column=1, padx=10, pady=8)

Label(f_main, text="Regd No", bg="black", fg="white").grid(row=1, column=0, padx=10, pady=8)
e_reg = Entry(f_main)
e_reg.grid(row=1, column=1, padx=10, pady=8)

Label(f_main, text="Password (Admin)", bg="black", fg="white").grid(row=2, column=0, padx=10, pady=8)
e_pass = Entry(f_main, show="*")
e_pass.grid(row=2, column=1, padx=10, pady=8)

Button(root, text="Admin Login", bg="green", fg="white", width=20, command=admin_login).pack(pady=7)
Button(root, text="Customer Login", bg="green", fg="white", width=20, command=customer_login).pack(pady=7)
Button(root, text="Register", bg="green", fg="white", width=20, command=register_window).pack(pady=7)
Button(root, text="Exit", bg="green", fg="white", width=20, command=app_exit).pack(pady=7)

root.mainloop()
