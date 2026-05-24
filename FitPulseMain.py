from tkinter import *
from tkinter import messagebox
import pickle
from datetime import datetime

# =====================================
# WINDOW
# =====================================

window = Tk()

window.title("FitPulse")

window.geometry("1000x700")

window.config(bg="#f5f7fa")

# =====================================
# LOGO
# =====================================

logo = """
███████╗██╗████████╗██████╗ ██╗   ██╗██╗     ███████╗███████╗
██╔════╝██║╚══██╔══╝██╔══██╗██║   ██║██║     ██╔════╝██╔════╝
█████╗  ██║   ██║   ██████╔╝██║   ██║██║     ███████╗█████╗
██╔══╝  ██║   ██║   ██╔═══╝ ██║   ██║██║     ╚════██║██╔══╝
██║     ██║   ██║   ██║     ╚██████╔╝███████╗███████║███████╗
╚═╝     ╚═╝   ╚═╝   ╚═╝      ╚═════╝ ╚══════╝╚══════╝╚══════╝
"""

# =====================================
# FILES
# =====================================

MEMBER_FILE = "members.dat"
ATTENDANCE_FILE = "attendance.dat"

# =====================================
# ADMIN DATA
# =====================================

admins = [
    [1001, "Admin", "admin123"]
]

# =====================================
# BUTTON STYLE
# =====================================

button_style = {
    "font": ("Poppins", 12, "bold"),
    "bg": "#111111",
    "fg": "white",
    "activebackground": "#333333",
    "activeforeground": "white",
    "width": 25,
    "height": 2,
    "bd": 0,
    "cursor": "hand2"
}

# =====================================
# DEFAULT MEMBERS
# =====================================

default_members = [

    [101001, "Arjun", 18, 172, 68, "Muscle Gain", "arjun123", 5000],

    [101002, "Rahul", 19, 175, 74, "Weight Loss", "rahul123", 4500],

    [101003, "Neeraj", 20, 168, 65, "Maintain", "neeraj123", 4000],

    [101004, "Aditya", 18, 180, 78, "Muscle Gain", "aditya123", 5500],

    [101005, "Vishnu", 21, 170, 72, "Maintain", "vishnu123", 4800]
]

# =====================================
# CREATE FILE
# =====================================

def create_files():

    try:

        with open(MEMBER_FILE, "rb") as f:
            pass

    except:

        with open(MEMBER_FILE, "wb") as f:

            for member in default_members:

                pickle.dump(member, f)

create_files()

# =====================================
# CLEAR WINDOW
# =====================================

def clear_window():

    for widget in window.winfo_children():

        widget.destroy()

# =====================================
# SHOW LOGO
# =====================================

def show_logo():

    top = Frame(window, bg="#f5f7fa")

    top.pack(fill="x")

    Label(
        top,
        text=logo,
        font=("Courier New", 9, "bold"),
        bg="#f5f7fa",
        fg="#111111",
        justify=LEFT
    ).pack(pady=(20,5))

    Label(
        top,
        text="Modern Gym Management System",
        font=("Poppins", 12),
        bg="#f5f7fa",
        fg="#666666"
    ).pack(pady=(0,15))

# =====================================
# MEMBER FUNCTIONS
# =====================================

def load_members():

    members = []

    try:

        with open(MEMBER_FILE, "rb") as f:

            while True:

                try:

                    members.append(pickle.load(f))

                except EOFError:
                    break

    except:
        pass

    return members

def save_members(members):

    with open(MEMBER_FILE, "wb") as f:

        for member in members:

            pickle.dump(member, f)

def add_member(name, age, height, weight, goal, password):

    members = load_members()

    member_id = 101000 + len(members) + 1

    new_member = [

        member_id,
        name,
        age,
        height,
        weight,
        goal,
        password,
        5000
    ]

    members.append(new_member)

    save_members(members)

    return member_id

def delete_member(member_id):

    members = load_members()

    new_members = []

    found = False

    for member in members:

        if member[0] != member_id:

            new_members.append(member)

        else:

            found = True

    save_members(new_members)

    return found

# =====================================
# LOGIN FUNCTIONS
# =====================================

def admin_login(admin_id, password):

    for admin in admins:

        if admin[0] == admin_id and admin[2] == password:

            return admin

    return None

def user_login(member_id, password):

    members = load_members()

    for member in members:

        if member[0] == member_id and member[6] == password:

            return member

    return None

# =====================================
# ATTENDANCE
# =====================================

def mark_attendance(member):

    time_now = datetime.now().strftime("%H:%M:%S")

    log = (
        member[1],
        member[0],
        time_now
    )

    with open(ATTENDANCE_FILE, "ab") as f:

        pickle.dump(log, f)

def get_attendance_logs():

    logs = []

    try:

        with open(ATTENDANCE_FILE, "rb") as f:

            while True:

                try:

                    logs.append(pickle.load(f))

                except EOFError:
                    break

    except:
        pass

    return logs

# =====================================
# MEMBERSHIP FEES
# =====================================

def get_total_fees():

    members = load_members()

    total = 0

    for member in members:

        total += member[7]

    return total

# =====================================
# HOME PAGE
# =====================================

def home_page():

    clear_window()

    show_logo()

    Label(
        window,
        text="FitPulse Gym Management System",
        font=("Poppins", 24, "bold"),
        bg="#f5f7fa"
    ).pack(pady=20)

    Button(
        window,
        text="Admin Login",
        command=admin_login_page,
        **button_style
    ).pack(pady=10)

    Button(
        window,
        text="User Login",
        command=user_login_page,
        **button_style
    ).pack(pady=10)

# =====================================
# ADMIN LOGIN
# =====================================

def admin_login_page():

    clear_window()

    show_logo()

    Label(
        window,
        text="Admin Login",
        font=("Poppins",22,"bold"),
        bg="#f5f7fa"
    ).pack(pady=20)

    Label(window,text="Admin ID",font=("Poppins",12),bg="#f5f7fa").pack()

    id_entry = Entry(window,font=("Poppins",12),width=30)
    id_entry.pack(pady=5)

    Label(window,text="Password",font=("Poppins",12),bg="#f5f7fa").pack()

    pass_entry = Entry(window,show="*",font=("Poppins",12),width=30)
    pass_entry.pack(pady=5)

    def login():

        try:

            admin = admin_login(
                int(id_entry.get()),
                pass_entry.get()
            )

            if admin:

                admin_dashboard()

            else:

                messagebox.showerror(
                    "Error",
                    "Wrong Admin ID or Password"
                )

        except:

            messagebox.showerror(
                "Error",
                "Invalid Details"
            )

    Button(
        window,
        text="Login",
        command=login,
        **button_style
    ).pack(pady=20)

    Button(
        window,
        text="Back",
        command=home_page,
        **button_style
    ).pack()

# =====================================
# USER LOGIN
# =====================================

def user_login_page():

    clear_window()

    show_logo()

    Label(
        window,
        text="User Login",
        font=("Poppins",22,"bold"),
        bg="#f5f7fa"
    ).pack(pady=20)

    Label(window,text="Member ID",font=("Poppins",12),bg="#f5f7fa").pack()

    id_entry = Entry(window,font=("Poppins",12),width=30)
    id_entry.pack(pady=5)

    Label(window,text="Password",font=("Poppins",12),bg="#f5f7fa").pack()

    pass_entry = Entry(window,show="*",font=("Poppins",12),width=30)
    pass_entry.pack(pady=5)

    def login():

        try:

            member = user_login(
                int(id_entry.get()),
                pass_entry.get()
            )

            if member:

                mark_attendance(member)

                user_dashboard(member)

            else:

                messagebox.showerror(
                    "Error",
                    "Wrong Member ID or Password"
                )

        except:

            messagebox.showerror(
                "Error",
                "Invalid Details"
            )

    Button(
        window,
        text="Login",
        command=login,
        **button_style
    ).pack(pady=20)

    Button(
        window,
        text="Back",
        command=home_page,
        **button_style
    ).pack()

# =====================================
# ADMIN DASHBOARD
# =====================================

def admin_dashboard():

    clear_window()

    show_logo()

    Label(
        window,
        text="Admin Dashboard",
        font=("Poppins",24,"bold"),
        bg="#f5f7fa"
    ).pack(pady=20)

    Button(
        window,
        text="Membership Fees",
        command=membership_page,
        **button_style
    ).pack(pady=10)

    Button(
        window,
        text="Attendance Logs",
        command=attendance_page,
        **button_style
    ).pack(pady=10)

    Button(
        window,
        text="Manage Members",
        command=manage_members_page,
        **button_style
    ).pack(pady=10)

    Button(
        window,
        text="Logout",
        command=home_page,
        **button_style
    ).pack(pady=20)

# =====================================
# MEMBERSHIP PAGE
# =====================================

def membership_page():

    clear_window()

    show_logo()

    Label(
        window,
        text="Membership Fees",
        font=("Poppins",22,"bold"),
        bg="#f5f7fa"
    ).pack(pady=20)

    total = get_total_fees()

    Label(
        window,
        text="Total Fees Earned",
        font=("Poppins",18),
        bg="#f5f7fa"
    ).pack(pady=10)

    Label(
        window,
        text="₹ " + str(total),
        font=("Poppins",30,"bold"),
        fg="green",
        bg="#f5f7fa"
    ).pack(pady=20)

    Button(
        window,
        text="Back",
        command=admin_dashboard,
        **button_style
    ).pack(pady=20)

# =====================================
# ATTENDANCE PAGE
# =====================================

def attendance_page():

    clear_window()

    show_logo()

    Label(
        window,
        text="Attendance Logs",
        font=("Poppins",22,"bold"),
        bg="#f5f7fa"
    ).pack(pady=20)

    logs = get_attendance_logs()

    if len(logs) == 0:

        Label(
            window,
            text="No Attendance Logs",
            font=("Poppins",14),
            bg="#f5f7fa"
        ).pack()

    else:

        for log in logs:

            text = (
                str(log[0]) +
                " (" +
                str(log[1]) +
                ") - " +
                str(log[2])
            )

            Label(
                window,
                text=text,
                font=("Poppins",13),
                bg="#f5f7fa"
            ).pack(pady=5)

    Button(
        window,
        text="Back",
        command=admin_dashboard,
        **button_style
    ).pack(pady=20)

# =====================================
# MANAGE MEMBERS
# =====================================

def manage_members_page():

    clear_window()

    show_logo()

    Label(
        window,
        text="Manage Members",
        font=("Poppins",22,"bold"),
        bg="#f5f7fa"
    ).pack(pady=20)

    Button(
        window,
        text="Add Member",
        command=add_member_page,
        **button_style
    ).pack(pady=10)

    Button(
        window,
        text="Delete Member",
        command=delete_member_page,
        **button_style
    ).pack(pady=10)

    Button(
        window,
        text="Back",
        command=admin_dashboard,
        **button_style
    ).pack(pady=20)

# =====================================
# ADD MEMBER
# =====================================

def add_member_page():

    clear_window()

    show_logo()

    Label(
        window,
        text="Add Member",
        font=("Poppins",22,"bold"),
        bg="#f5f7fa"
    ).pack(pady=20)

    labels = [
        "Name",
        "Age",
        "Height",
        "Weight",
        "Goal",
        "Password"
    ]

    entries = []

    for item in labels:

        Label(
            window,
            text=item,
            font=("Poppins",12),
            bg="#f5f7fa"
        ).pack()

        entry = Entry(
            window,
            font=("Poppins",12),
            width=30
        )

        entry.pack(pady=5)

        entries.append(entry)

    def save():

        try:

            member_id = add_member(
                entries[0].get(),
                int(entries[1].get()),
                float(entries[2].get()),
                float(entries[3].get()),
                entries[4].get(),
                entries[5].get()
            )

            messagebox.showinfo(
                "Success",
                "Member Added\nID : " + str(member_id)
            )

        except:

            messagebox.showerror(
                "Error",
                "Invalid Details"
            )

    Button(
        window,
        text="Save Member",
        command=save,
        **button_style
    ).pack(pady=20)

    Button(
        window,
        text="Back",
        command=manage_members_page,
        **button_style
    ).pack()

# =====================================
# DELETE MEMBER
# =====================================

def delete_member_page():

    clear_window()

    show_logo()

    Label(
        window,
        text="Delete Member",
        font=("Poppins",22,"bold"),
        bg="#f5f7fa"
    ).pack(pady=20)

    Label(
        window,
        text="Member ID",
        font=("Poppins",12),
        bg="#f5f7fa"
    ).pack()

    id_entry = Entry(
        window,
        font=("Poppins",12),
        width=30
    )

    id_entry.pack(pady=5)

    def remove():

        try:

            result = delete_member(
                int(id_entry.get())
            )

            if result:

                messagebox.showinfo(
                    "Success",
                    "Member Deleted"
                )

            else:

                messagebox.showerror(
                    "Error",
                    "Member Not Found"
                )

        except:

            messagebox.showerror(
                "Error",
                "Invalid ID"
            )

    Button(
        window,
        text="Delete",
        command=remove,
        **button_style
    ).pack(pady=20)

    Button(
        window,
        text="Back",
        command=manage_members_page,
        **button_style
    ).pack()

# =====================================
# USER DASHBOARD
# =====================================

def user_dashboard(member):

    clear_window()

    show_logo()

    Label(
        window,
        text="Welcome " + member[1],
        font=("Poppins",24,"bold"),
        bg="#f5f7fa"
    ).pack(pady=20)

    bmi = round(member[4] / ((member[3]/100) ** 2), 2)

    Label(
        window,
        text="BMI : " + str(bmi),
        font=("Poppins",14),
        bg="#f5f7fa"
    ).pack(pady=10)

    Button(
        window,
        text="Logout",
        command=home_page,
        **button_style
    ).pack(pady=20)

# =====================================
# START
# =====================================

home_page()

window.mainloop()
