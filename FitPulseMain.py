from datetime import date
from pathlib import Path
from tkinter import *
from tkinter import messagebox

import FitPulseBackend as backend

BG = "#f5f7fa"
TEXT = "#111111"
MUTED = "#666666"
BUTTON_STYLE = {
    "font": ("Poppins", 12, "bold"),
    "bg": TEXT,
    "fg": "white",
    "activebackground": "#333333",
    "activeforeground": "white",
    "width": 25,
    "height": 2,
    "bd": 0,
    "cursor": "hand2",
}

LOGO_FILE = Path(__file__).resolve().parent / "assets" / "fitpulse_logo.png"
GOALS = ["Weight Loss", "Muscle Gain", "Maintain"]
PLANS = ["GOLD", "PLATINUM", "DIAMOND"]
DURATIONS = ["monthly", "yearly"]
INTENSITIES = ["Low", "Medium", "High"]
DEFAULT_MEMBERS = [
    [101001, "Arjun", 18, 172, 68, "Muscle Gain", "arjun123", 5000],
    [101002, "Rahul", 19, 175, 74, "Weight Loss", "rahul123", 4500],
    [101003, "Neeraj", 20, 168, 65, "Maintain", "neeraj123", 4000],
    [101004, "Aditya", 18, 180, 78, "Muscle Gain", "aditya123", 5500],
    [101005, "Vishnu", 21, 170, 72, "Maintain", "vishnu123", 4800],
]

window = Tk()
window.title("FitPulse")
window.geometry("1000x700")
window.config(bg=BG)


def create_files():
    if not backend.load_admins():
        backend.save_admins([[1001, "Admin", "Owner", "admin123"]])

    if backend.load_members():
        return

    join_date = date.today().isoformat()
    members = [
        [mid, name, age, height, weight, goal, join_date, password, True]
        for mid, name, age, height, weight, goal, password, fee in DEFAULT_MEMBERS
    ]
    memberships = [
        [mid, "GOLD", "monthly", fee, join_date, join_date, 0, "", ""]
        for mid, name, age, height, weight, goal, password, fee in DEFAULT_MEMBERS
    ]
    backend.save_members(members)
    backend.save_memberships(memberships)


def clear_window():
    for widget in window.winfo_children():
        widget.destroy()


def label(text, size=12, weight="normal", parent=None, **kwargs):
    pady = kwargs.pop("pady", 5)
    widget = Label(
        parent or window,
        text=text,
        font=("Poppins", size, weight),
        bg=BG,
        fg=kwargs.pop("fg", TEXT),
        **kwargs,
    )
    widget.pack(pady=pady)
    return widget


def button(text, command, pady=10):
    Button(window, text=text, command=command, **BUTTON_STYLE).pack(pady=pady)


def small_button(parent, text, command):
    Button(
        parent,
        text=text,
        command=command,
        font=("Poppins", 10, "bold"),
        bg=TEXT,
        fg="white",
        activebackground="#333333",
        activeforeground="white",
        width=8,
        height=1,
        bd=0,
        cursor="hand2",
    ).pack(side=LEFT, padx=4)


def entry(title, show=None):
    label(title)
    field = Entry(window, show=show, font=("Poppins", 12), width=30)
    field.pack(pady=5)
    return field


def dropdown(title, options, selected=None):
    label(title)
    variable = StringVar(value=selected or options[0])
    menu = OptionMenu(window, variable, *options)
    menu.config(font=("Poppins", 12), width=25, bg="white", fg=TEXT)
    menu.pack(pady=5)
    return variable


def member_form(member=None):
    fields = {name: entry(name) for name in ["Name", "Age", "Height", "Weight", "Password"]}
    if member:
        values = {"Name": member[1], "Age": member[2], "Height": member[3], "Weight": member[4], "Password": member[7]}
        for name in fields:
            fields[name].insert(0, str(values[name]))
    return fields, dropdown("Goal", GOALS, member[5] if member else GOALS[0])


def get_member_fitness(member_id):
    for record in backend.load_fitness():
        if record[0] == member_id:
            return record
    return None


def show_lines(lines, size=12, pady=2):
    for item in lines:
        label(item, size, pady=pady)


def show_logo():
    top = Frame(window, bg=BG)
    top.pack(fill="x")

    if LOGO_FILE.exists():
        window.logo_image = PhotoImage(file=str(LOGO_FILE))
        Label(top, image=window.logo_image, bg=BG).pack(pady=(12, 0))
    else:
        Label(top, text="FitPulse", font=("Poppins", 34, "bold"), bg=BG, fg=TEXT).pack(pady=(12, 0))

    Label(
        top,
        text="An All in One Gym Management and Fitness App.",
        font=("Poppins", 12),
        bg=BG,
        fg=MUTED,
    ).pack(pady=(0, 10))


def start_page(title):
    clear_window()
    show_logo()
    label(title, 22, "bold", pady=16)


def add_member(name, age, height, weight, goal, password):
    member_id = backend.add_member(
        name, age, height, weight, goal, date.today().isoformat(), password
    )
    backend.update_membership(member_id, "Gold", "monthly")
    backend.update_workout_plan(member_id, goal, "Medium", 3)
    return member_id


def member_name_map():
    return {member[0]: member[1] for member in backend.load_members()}


def home_page():
    start_page("Welcome to Orbit Prime Gym!")
    button("Admin Login", admin_login_page)
    button("User Login", user_login_page)


def login_page(title, id_title, login_func, success_func):
    start_page(title)
    id_field = entry(id_title)
    password_field = entry("Password", show="*")

    def login():
        try:
            user = login_func(int(id_field.get()), password_field.get())
            if user:
                success_func(user)
            else:
                messagebox.showerror("Error", "Wrong ID or Password")
        except:
            messagebox.showerror("Error", "Invalid Details")

    button("Login", login, pady=20)
    button("Back", home_page, pady=0)


def admin_login_page():
    login_page("Admin Login", "Admin ID", backend.admin_login, lambda admin: admin_dashboard())


def user_login_page():
    login_page("User Login", "Member ID", backend.user_login, user_dashboard)


def menu_page(title, items, back_func=None):
    start_page(title)
    for text, command in items:
        button(text, command)
    if back_func:
        button("Back", back_func, pady=20)


def admin_dashboard():
    menu_page(
        "Admin Dashboard",
        [
            ("Membership Fees", membership_page),
            ("Attendance Logs", attendance_page),
            ("Manage Members", manage_members_page),
            ("Logout", home_page),
        ],
    )


def membership_page():
    start_page("Membership Fees")
    label("Total Fees Earned", 18, pady=4)
    label("Rs. " + str(backend.get_total_fees_earned()), 28, "bold", fg="green", pady=8)

    names = member_name_map()
    memberships = backend.load_memberships()
    if not memberships:
        label("No membership payments found", 14)
    else:
        label("Member payment details", 16, "bold", pady=8)
        for membership in memberships:
            member_id, plan, duration, fee, paid_on, expiry, visits, last_visit, auto_pay = membership[:9]
            text = (
                f"{names.get(member_id, 'Unknown')} ({member_id}) | "
                f"{plan} {duration} | Paid Rs. {fee} on {paid_on} | "
                f"Expires {expiry} | Visits {visits}"
            )
            label(text, 11, pady=2)

    button("Back", admin_dashboard, pady=16)


def attendance_page():
    start_page("Attendance Logs")
    logs = backend.get_attendance_logs()

    if not logs:
        label("No Attendance Logs", 14)
    else:
        names = member_name_map()
        for record in logs:
            member_id, log_date, log_time = record[:3]
            streak = record[3] if len(record) > 3 else 1
            label(f"{names.get(member_id, 'Unknown')} ({member_id}) - {log_date} - {log_time} - Streak {streak}", 13)

    button("Back", admin_dashboard, pady=20)


def manage_members_page():
    menu_page(
        "Manage Members",
        [
            ("Add Member", add_member_page),
            ("Delete Member", delete_member_page),
            ("Edit Member", edit_member_lookup_page),
            ("Search Member", search_member_page),
        ],
        admin_dashboard,
    )


def add_member_page():
    start_page("Add Member")
    fields, goal_var = member_form()

    def save():
        try:
            member_id = add_member(
                fields["Name"].get(),
                int(fields["Age"].get()),
                float(fields["Height"].get()),
                float(fields["Weight"].get()),
                goal_var.get(),
                fields["Password"].get(),
            )
            messagebox.showinfo("Success", "Member Added\nID : " + str(member_id))
        except:
            messagebox.showerror("Error", "Invalid Details")

    button("Save Member", save, pady=20)
    button("Back", manage_members_page, pady=0)


def delete_member_page():
    start_page("Delete Member")
    id_field = entry("Member ID")

    def remove():
        try:
            deleted = backend.delete_member(int(id_field.get()), "Deleted from admin UI")
            if deleted:
                messagebox.showinfo("Success", "Member Deleted")
            else:
                messagebox.showerror("Error", "Member Not Found")
        except:
            messagebox.showerror("Error", "Invalid ID")

    button("Delete", remove, pady=20)
    button("Back", manage_members_page, pady=0)


def edit_member_lookup_page():
    start_page("Edit Member")
    id_field = entry("Member ID")

    def open_editor():
        try:
            member = backend.search_member_by_id(int(id_field.get()))
            if member:
                edit_member_page(member)
            else:
                messagebox.showerror("Error", "Member Not Found")
        except:
            messagebox.showerror("Error", "Invalid ID")

    button("Edit", open_editor, pady=20)
    button("Back", manage_members_page, pady=0)


def edit_member_page(member):
    start_page("Edit Member")
    fields, goal_var = member_form(member)

    def save():
        try:
            backend.modify_member(
                member[0],
                name=fields["Name"].get(),
                age=int(fields["Age"].get()),
                height=float(fields["Height"].get()),
                weight=float(fields["Weight"].get()),
                goal=goal_var.get(),
                password=fields["Password"].get(),
            )
            backend.update_workout_plan(member[0], goal_var.get(), "Medium", 3)
            messagebox.showinfo("Success", "Member Updated")
            manage_members_page()
        except:
            messagebox.showerror("Error", "Invalid Details")

    button("Save Changes", save, pady=20)
    button("Back", manage_members_page, pady=0)


def search_member_page():
    start_page("Search Member")
    search_field = entry("Enter Member ID or Name")
    result_box = Frame(window, bg=BG, width=620, height=260)
    result_box.pack_propagate(False)
    result_box.pack(pady=12)

    def show_result_row(member):
        row = Frame(result_box, bg="white", highlightbackground="#d6dbe3", highlightthickness=1)
        row.pack(fill="x", padx=16, pady=4)

        Label(
            row,
            text=f"{member[1]} ({member[0]})",
            font=("Poppins", 12, "bold"),
            bg="white",
            fg=TEXT,
            anchor="w",
            width=34,
        ).pack(side=LEFT, padx=12, pady=8)

        small_button(row, "View", lambda member=member: view_member_page(member))
        small_button(row, "Edit", lambda member=member: edit_member_page(member))

    def search():
        for widget in result_box.winfo_children():
            widget.destroy()

        query = search_field.get().strip().lower()
        if not query:
            label("Enter a member ID or name", 12, parent=result_box)
            return

        matches = []
        for member in backend.load_members():
            if query == str(member[0]) or query in member[1].lower():
                matches.append(member)

        if not matches:
            label("No matching member found", 12, parent=result_box)
        else:
            for member in matches[:6]:
                show_result_row(member)
            if len(matches) > 6:
                label(f"Showing 6 of {len(matches)} matches. Type more to narrow it down.", 10, parent=result_box, fg=MUTED, pady=4)

    button("Search", search, pady=16)
    button("Back", manage_members_page, pady=0)


def view_member_page(member):
    start_page("Member Details")
    status = "Active" if member[8] else "Inactive"
    membership = backend.get_membership_info(member[0])
    details = [
        f"ID: {member[0]}",
        f"Name: {member[1]}",
        f"Age: {member[2]}",
        f"Height: {member[3]} cm",
        f"Weight: {member[4]} kg",
        f"Goal: {member[5]}",
        f"Joined: {member[6]}",
        f"Status: {status}",
    ]
    if membership:
        details.append(
            f"Membership: {membership[1]} {membership[2]}, Rs. {membership[3]}, paid {membership[4]}"
        )
    show_lines(details)
    button("Edit", lambda: edit_member_page(member), pady=14)
    button("Back", search_member_page, pady=0)


def user_dashboard(member):
    member = backend.search_member_by_id(member[0]) or member
    menu_page(
        "Welcome " + member[1],
        [
            ("Profile", lambda: user_profile_page(member)),
            ("Membership", lambda: user_membership_page(member)),
            ("Workout & Diet", lambda: user_workout_page(member)),
            ("Logout", home_page),
        ],
    )


def bmi_suggestion(category):
    if category == "Underweight":
        return "Eat more calories and focus on strength training."
    if category == "Normal":
        return "BMI is in a healthy range. Maintain your routine."
    if category == "Overweight":
        return "Add regular cardio and keep calories controlled."
    return "Focus on low-impact cardio and a steady calorie deficit."


def user_profile_page(member):
    member = backend.search_member_by_id(member[0]) or member
    bmi, category = backend.calculate_bmi(member[4], member[3])
    status = "Active" if member[8] else "Inactive"

    start_page("Profile")
    details = [
        f"Member ID: {member[0]}",
        f"Name: {member[1]}",
        f"Age: {member[2]}",
        f"Height: {member[3]} cm",
        f"Weight: {member[4]} kg",
        f"Goal: {member[5]}",
        f"Joined: {member[6]}",
        f"Status: {status}",
        f"BMI: {bmi} ({category})",
        "BMI Analysis: " + bmi_suggestion(category),
    ]
    show_lines(details)

    button("Update Body Stats", lambda: update_body_stats_page(member), pady=14)
    button("Back", lambda: user_dashboard(member), pady=0)


def update_body_stats_page(member):
    start_page("Update Body Stats")
    weight_field = entry("Weight")
    height_field = entry("Height")
    weight_field.insert(0, str(member[4]))
    height_field.insert(0, str(member[3]))

    def save():
        try:
            bmi, category = backend.update_body_stats(
                member[0],
                float(weight_field.get()),
                float(height_field.get()),
            )
            messagebox.showinfo("Saved", f"BMI: {bmi} ({category})")
            user_profile_page(backend.search_member_by_id(member[0]) or member)
        except:
            messagebox.showerror("Error", "Invalid height or weight")

    button("Save", save, pady=20)
    button("Back", lambda: user_profile_page(member), pady=0)


def user_membership_page(member):
    start_page("Membership")
    membership = backend.get_membership_info(member[0])

    if not membership:
        label("No membership found", 14)
    else:
        member_id, plan, duration, fee, start, expiry, visits, last_visit, auto_pay = membership[:9]
        today = date.today()
        try:
            days_left = (date.fromisoformat(expiry) - today).days
        except:
            days_left = 0
        show_lines([
            f"Plan: {plan}",
            f"Duration: {duration}",
            f"Fee Paid: Rs. {fee}",
            f"Start Date: {start}",
            f"Expiry Date: {expiry}",
            f"Days Remaining: {days_left}",
            f"Days Visited: {visits}",
            f"Last Visit: {last_visit or 'Not marked'}",
        ], pady=3)

    button("Change Plan", lambda: change_membership_page(member), pady=14)
    button("Back", lambda: user_dashboard(member), pady=0)


def change_membership_page(member):
    start_page("Change Membership Plan")
    current = backend.get_membership_info(member[0])
    selected_plan = current[1] if current and current[1] in PLANS else PLANS[0]
    selected_duration = current[2] if current and current[2] in DURATIONS else DURATIONS[0]
    plan_var = dropdown("Plan", PLANS, selected_plan)
    duration_var = dropdown("Duration", DURATIONS, selected_duration)

    def save():
        try:
            backend.update_membership(member[0], plan_var.get(), duration_var.get())
            messagebox.showinfo("Success", "Membership Updated")
            user_membership_page(member)
        except:
            messagebox.showerror("Error", "Invalid Plan")

    button("Save Plan", save, pady=20)
    button("Back", lambda: user_membership_page(member), pady=0)


def user_workout_page(member):
    start_page("Workout & Diet")
    fitness = get_member_fitness(member[0])

    if not fitness:
        backend.update_workout_plan(member[0], member[5], "Medium", 3)
        fitness = get_member_fitness(member[0])

    if fitness:
        member_id, workout, intensity, frequency, diet_type, calorie_mode, progress = fitness[:7]
        show_lines([
            f"Workout Plan: {workout}",
            f"Intensity: {intensity}",
            f"Frequency: {frequency} days/week",
            f"Diet Type: {diet_type}",
            f"Calorie Mode: {calorie_mode}",
        ], pady=3)

        label("Diet Plan", 16, "bold", pady=10)
        for item in backend.get_diet_plan(member[5]):
            label("- " + item, 12, pady=2)

    button("Change Workout", lambda: change_workout_page(member), pady=14)
    button("Back", lambda: user_dashboard(member), pady=0)


def change_workout_page(member):
    start_page("Change Workout")
    goal_var = dropdown("Goal", GOALS, member[5])
    intensity_var = dropdown("Intensity", INTENSITIES, "Medium")
    frequency_field = entry("Frequency Per Week")
    frequency_field.insert(0, "3")

    def save():
        try:
            frequency = int(frequency_field.get())
            backend.modify_member(member[0], goal=goal_var.get())
            backend.update_workout_plan(member[0], goal_var.get(), intensity_var.get(), frequency)
            messagebox.showinfo("Success", "Workout Updated")
            updated_member = backend.search_member_by_id(member[0]) or member
            user_workout_page(updated_member)
        except:
            messagebox.showerror("Error", "Invalid Workout Details")

    button("Save Workout", save, pady=20)
    button("Back", lambda: user_workout_page(member), pady=0)


create_files()
home_page()
window.mainloop()
