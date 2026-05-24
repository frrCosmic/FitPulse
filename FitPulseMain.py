
from tkinter import *
from tkinter import messagebox
from FitPulseBackend import *

window = Tk()
window.title("FitPulse")
window.geometry("1000x700")
window.config(bg="white")

logo = """
███████╗██╗████████╗██████╗ ██╗   ██╗██╗     ███████╗███████╗
██╔════╝██║╚══██╔══╝██╔══██╗██║   ██║██║     ██╔════╝██╔════╝
█████╗  ██║   ██║   ██████╔╝██║   ██║██║     ███████╗█████╗
██╔══╝  ██║   ██║   ██╔═══╝ ██║   ██║██║     ╚════██║██╔══╝
██║     ██║   ██║   ██║     ╚██████╔╝███████╗███████║███████╗
╚═╝     ╚═╝   ╚═╝   ╚═╝      ╚═════╝ ╚══════╝╚══════╝╚══════╝
"""

def clear_window():
    for widget in window.winfo_children():
        widget.destroy()

def show_logo():
    Label(
        window,
        text=logo,
        font=("Courier", 10, "bold"),
        bg="white",
        justify=LEFT
    ).pack(pady=20)

def home_page():
    clear_window()

    show_logo()

    Label(
        window,
        text="FitPulse Gym Management System",
        font=("Arial", 22, "bold"),
        bg="white"
    ).pack(pady=20)

    Button(
        window,
        text="Admin Login",
        width=25,
        height=2,
        font=("Arial", 14),
        command=admin_login_page
    ).pack(pady=20)

    Button(
        window,
        text="User Login",
        width=25,
        height=2,
        font=("Arial", 14),
        command=user_login_page
    ).pack(pady=20)

def admin_login_page():
    clear_window()

    show_logo()

    Label(
        window,
        text="Admin Login",
        font=("Arial", 20, "bold"),
        bg="white"
    ).pack(pady=20)

    Label(window, text="Admin ID", font=("Arial", 14), bg="white").pack()

    id_entry = Entry(window, font=("Arial", 14))
    id_entry.pack(pady=10)

    Label(window, text="Password", font=("Arial", 14), bg="white").pack()

    password_entry = Entry(window, show="*", font=("Arial", 14))
    password_entry.pack(pady=10)

    def login():
        try:
            admin = admin_login(int(id_entry.get()), password_entry.get())

            if admin != None:
                admin_dashboard(admin)
            else:
                messagebox.showerror("Error", "Invalid Login")

        except:
            messagebox.showerror("Error", "Enter Valid Details")

    Button(window, text="Login", command=login).pack(pady=20)

    Button(window, text="Back", command=home_page).pack()

def user_login_page():
    clear_window()

    show_logo()

    Label(
        window,
        text="User Login",
        font=("Arial", 20, "bold"),
        bg="white"
    ).pack(pady=20)

    Label(window, text="Member ID", font=("Arial", 14), bg="white").pack()

    id_entry = Entry(window, font=("Arial", 14))
    id_entry.pack(pady=10)

    Label(window, text="Password", font=("Arial", 14), bg="white").pack()

    password_entry = Entry(window, show="*", font=("Arial", 14))
    password_entry.pack(pady=10)

    def login():
        try:
            member = user_login(int(id_entry.get()), password_entry.get())

            if member != None:
                user_dashboard(member)
            else:
                messagebox.showerror("Error", "Invalid Login")

        except:
            messagebox.showerror("Error", "Enter Valid Details")

    Button(window, text="Login", command=login).pack(pady=20)

    Button(window, text="Back", command=home_page).pack()

def admin_dashboard(admin):
    clear_window()

    show_logo()

    Label(
        window,
        text="Admin Dashboard",
        font=("Arial", 20, "bold"),
        bg="white"
    ).pack(pady=20)

    Label(
        window,
        text="Welcome " + admin[1],
        font=("Arial", 14),
        bg="white"
    ).pack(pady=10)

    Button(window, text="Membership Fees", width=25, height=2,
           command=membership_page).pack(pady=10)

    Button(window, text="Attendance Logs", width=25, height=2,
           command=attendance_page).pack(pady=10)

    Button(window, text="Manage Members", width=25, height=2,
           command=manage_members_page).pack(pady=10)

    Button(window, text="Logout", width=25, height=2,
           command=home_page).pack(pady=20)

def membership_page():
    clear_window()

    show_logo()

    Label(window, text="Membership Fees",
          font=("Arial", 20, "bold"),
          bg="white").pack(pady=20)

    total = get_total_fees_earned()

    Label(
        window,
        text="Total Fees Earned: Rs. " + str(total),
        font=("Arial", 16, "bold"),
        fg="green",
        bg="white"
    ).pack(pady=20)

    memberships = load_memberships()

    for membership in memberships:
        text = (
            "Member ID: "
            + str(membership[0])
            + " | "
            + membership[1]
            + " | Rs. "
            + str(membership[3])
        )

        Label(window, text=text, font=("Arial", 12),
              bg="white").pack()

    Button(window, text="Back", command=home_page).pack(pady=20)

def attendance_page():
    clear_window()

    show_logo()

    Label(window, text="Attendance Logs",
          font=("Arial", 20, "bold"),
          bg="white").pack(pady=20)

    logs = get_attendance_logs()

    for log in logs:
        text = (
            "Member ID: "
            + str(log[0])
            + " | "
            + log[1]
            + " | "
            + log[2]
        )

        Label(window, text=text, font=("Arial", 12),
              bg="white").pack()

    Button(window, text="Back", command=home_page).pack(pady=20)

def manage_members_page():
    clear_window()

    show_logo()

    Label(window, text="Manage Members",
          font=("Arial", 20, "bold"),
          bg="white").pack(pady=20)

    Button(window, text="Add Member", width=25, height=2,
           command=add_member_page).pack(pady=10)

    Button(window, text="Delete Member", width=25, height=2,
           command=delete_member_page).pack(pady=10)

    Button(window, text="Back", command=home_page).pack(pady=20)

def add_member_page():

    clear_window()

    show_logo()

    Label(
        window,
        text="Add Member",
        font=("Arial", 20, "bold"),
        bg="white"
    ).pack(pady=20)

    # =========================
    # NAME
    # =========================

    Label(window, text="Name", bg="white").pack()

    name_entry = Entry(window, font=("Arial", 14))
    name_entry.pack(pady=5)

    # =========================
    # AGE DROPDOWN
    # =========================

    Label(window, text="Age", bg="white").pack()

    age_var = StringVar()
    age_var.set("18")

    age_menu = OptionMenu(
        window,
        age_var,
        *[str(i) for i in range(16, 61)]
    )

    age_menu.pack(pady=5)

    # =========================
    # HEIGHT DROPDOWN
    # =========================

    Label(window, text="Height (cm)", bg="white").pack()

    height_var = StringVar()
    height_var.set("170")

    height_menu = OptionMenu(
        window,
        height_var,
        *[str(i) for i in range(140, 221)]
    )

    height_menu.pack(pady=5)

    # =========================
    # WEIGHT DROPDOWN
    # =========================

    Label(window, text="Weight (kg)", bg="white").pack()

    weight_var = StringVar()
    weight_var.set("70")

    weight_menu = OptionMenu(
        window,
        weight_var,
        *[str(i) for i in range(40, 151)]
    )

    weight_menu.pack(pady=5)

    # =========================
    # GOAL DROPDOWN
    # =========================

    Label(window, text="Fitness Goal", bg="white").pack()

    goal_var = StringVar()
    goal_var.set("Maintain")

    goal_menu = OptionMenu(
        window,
        goal_var,
        "Weight Loss",
        "Muscle Gain",
        "Maintain"
    )

    goal_menu.pack(pady=5)

    # =========================
    # PASSWORD
    # =========================

    Label(window, text="Password", bg="white").pack()

    password_entry = Entry(window, font=("Arial", 14))
    password_entry.pack(pady=5)

    # =========================
    # SAVE FUNCTION
    # =========================

    def save():

        name = name_entry.get().strip()
        password = password_entry.get().strip()

        if name == "" or password == "":

            messagebox.showerror(
                "Error",
                "Name and Password cannot be empty"
            )

            return

        member_id = add_member(
            name,
            int(age_var.get()),
            float(height_var.get()),
            float(weight_var.get()),
            goal_var.get(),
            str(date.today()),
            password
        )

        messagebox.showinfo(
            "Success",
            "Member Added Successfully\n\nMember ID: "
            + str(member_id)
        )

    Button(
        window,
        text="Save Member",
        bg="green",
        fg="white",
        font=("Arial", 12, "bold"),
        command=save
    ).pack(pady=20)

    Button(
        window,
        text="Back",
        command=manage_members_page
    ).pack()
    def save():
        try:
            member_id = add_member(
                name_entry.get(),
                int(age_entry.get()),
                float(height_entry.get()),
                float(weight_entry.get()),
                goal_entry.get(),
                "2026-01-01",
                password_entry.get()
            )

            messagebox.showinfo(
                "Success",
                "Member Added\nID: " + str(member_id)
            )

        except:
            messagebox.showerror("Error", "Enter Valid Details")

    Button(window, text="Save", bg="green",
           fg="white", command=save).pack(pady=20)

    Button(window, text="Back",
           command=manage_members_page).pack()

def delete_member_page():
    clear_window()

    show_logo()

    Label(window, text="Delete Member",
          font=("Arial", 20, "bold"),
          bg="white").pack(pady=20)

    id_entry = Entry(window, font=("Arial", 14))
    id_entry.pack(pady=10)
    id_entry.insert(0, "Member ID")

    reason_entry = Entry(window, font=("Arial", 14))
    reason_entry.pack(pady=10)
    reason_entry.insert(0, "Reason")

    def remove():
        try:
            result = delete_member(
                int(id_entry.get()),
                reason_entry.get()
            )

            if result == True:
                messagebox.showinfo("Success", "Member Deleted")
            else:
                messagebox.showerror("Error", "Member Not Found")

        except:
            messagebox.showerror("Error", "Enter Valid Details")

    Button(window, text="Delete", bg="red",
           fg="white", command=remove).pack(pady=20)

    Button(window, text="Back",
           command=manage_members_page).pack()

def user_dashboard(member):
    clear_window()

    show_logo()

    Label(window, text="User Dashboard",
          font=("Arial", 20, "bold"),
          bg="white").pack(pady=20)

    Label(window, text="Welcome " + member[1],
          font=("Arial", 14),
          bg="white").pack(pady=10)

    Button(window, text="Profile", width=25, height=2,
           command=lambda: profile_page(member)).pack(pady=10)

    Button(window, text="Membership Info", width=25, height=2,
           command=lambda: membership_info_page(member)).pack(pady=10)

    Button(window, text="Logout", width=25, height=2,
           command=home_page).pack(pady=20)

def profile_page(member):
    clear_window()

    show_logo()

    Label(window, text="Profile",
          font=("Arial", 20, "bold"),
          bg="white").pack(pady=20)

    bmi, category = calculate_bmi(member[4], member[3])

    details = [
        "Name: " + member[1],
        "Age: " + str(member[2]),
        "Height: " + str(member[3]),
        "Weight: " + str(member[4]),
        "Goal: " + member[5],
        "BMI: " + str(bmi),
        "BMI Category: " + category
    ]

    for item in details:
        Label(window, text=item,
              font=("Arial", 14),
              bg="white").pack(pady=5)

    Label(window, text="Diet Plan",
          font=("Arial", 16, "bold"),
          bg="white").pack(pady=20)

    diet = get_diet_plan(member[5])

    for item in diet:
        Label(window, text="• " + item,
              font=("Arial", 12),
              bg="white").pack()

    Button(window, text="Back",
           command=lambda: user_dashboard(member)).pack(pady=20)

def membership_info_page(member):
    clear_window()

    show_logo()

    Label(window, text="Membership Info",
          font=("Arial", 20, "bold"),
          bg="white").pack(pady=20)

    membership = get_membership_info(member[0])

    if membership != None:

        details = [
            "Plan: " + membership[1],
            "Duration: " + membership[2],
            "Fee: Rs. " + str(membership[3]),
            "Start Date: " + membership[4],
            "Expiry Date: " + membership[5],
            "Visits: " + str(membership[6])
        ]

        for item in details:
            Label(window, text=item,
                  font=("Arial", 14),
                  bg="white").pack(pady=5)

    else:
        Label(window, text="No Membership Found",
              font=("Arial", 14),
              bg="white").pack()

    Button(window, text="Back",
           command=lambda: user_dashboard(member)).pack(pady=20)

home_page()

window.mainloop()
