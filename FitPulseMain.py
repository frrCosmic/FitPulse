from datetime import date
from pathlib import Path
from tkinter import *
from tkinter import messagebox
import FitPulseBackend as backend
BG = "#f5f7fa"
TEXT = "#111111"
MUTED = "#666666"
UI_SCALE = 1.0  # Lower this (for example, 0.85) on smaller displays.
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
ACTION_BUTTON_STYLE = {**BUTTON_STYLE, "width": 14, "height": 1}
LOGO_FILE = Path(__file__).resolve().parent / "assets" / "fitpulse_logo.png"
GOALS = ["Weight Loss", "Muscle Gain", "Maintain"]
GENDERS = ["Male", "Female"]
PLANS = ["GOLD", "PLATINUM", "DIAMOND"]
DURATIONS = ["monthly", "yearly"]
INTENSITIES = ["Low", "Medium", "High"]
MEMBER_FIELDS = ("Name", "Age", "Height", "Weight", "Password")
DEFAULT_MEMBERS = [
    [101001, "Arjun", 18, 172, 68, "Muscle Gain", "arjun123", 5000],
    [101002, "Rahul", 19, 175, 74, "Weight Loss", "rahul123", 4500],
    [101003, "Neeraj", 20, 168, 65, "Maintain", "neeraj123", 4000],
    [101004, "Aditya", 18, 180, 78, "Muscle Gain", "aditya123", 5500],
    [101005, "Vishnu", 21, 170, 72, "Maintain", "vishnu123", 4800],
]
window = None
page_content = None
current_admin = None
def initialize_window():
    global window
    window = Tk()
    window.title("FitPulse")
    base_tk_scaling = float(window.tk.call("tk", "scaling"))
    window.tk.call("tk", "scaling", base_tk_scaling * UI_SCALE)
    window.geometry(f"{round(1000 * UI_SCALE)}x{round(700 * UI_SCALE)}")
    window.config(bg=BG)
def create_files():
    if not backend.load_data("admins.dat"):
        backend.save_data("admins.dat", [[1001, "Admin", "Owner", "admin123"]])
    if backend.load_data("members.dat"):
        return
    join_date = date.today().isoformat()
    members = [
        [mid, name, age, height, weight, goal, join_date, password, True, GENDERS[0]]
        for mid, name, age, height, weight, goal, password, fee in DEFAULT_MEMBERS
    ]
    memberships = [
        [mid, "GOLD", "monthly", fee, join_date, join_date, 0, "", ""]
        for mid, name, age, height, weight, goal, password, fee in DEFAULT_MEMBERS
    ]
    backend.save_data("members.dat", members)
    backend.save_data("membership.dat", memberships)
def clear_window():
    global page_content
    for widget in window.winfo_children():
        widget.destroy()
    page_content = None
def create_page():
    global page_content
    page_content = Frame(window, bg=BG)
    page_content.pack(fill=BOTH, expand=True)
def label(text, size=12, weight="normal", parent=None, **kwargs):
    pady = kwargs.pop("pady", 5)
    widget = Label(parent or page_content, text=text, font=("Poppins", size, weight),
                   bg=BG, fg=kwargs.pop("fg", TEXT), **kwargs)
    widget.pack(pady=pady)
    return widget
def button(text, command, pady=10):
    Button(page_content, text=text, command=command, **BUTTON_STYLE).pack(pady=pady)
def save_action(action, refresh, error_msg="Invalid Details"):
    try:
        messagebox.showinfo("Success", action())
        refresh()
    except (ValueError, TypeError, KeyError):
        messagebox.showerror("Error", error_msg)
def save_row(text, action, refresh, back, error_msg="Invalid Details"):
    action_row((text, lambda: save_action(action, refresh, error_msg)), ("Back", back))
def action_row(*actions, pady=14):
    """Place related actions beside each other and keep the group centered."""
    row = Frame(page_content, bg=BG)
    row.pack(pady=pady)
    for text, command in actions:
        Button(row, text=text, command=command, **ACTION_BUTTON_STYLE).pack(
            side=LEFT, padx=6
        )
def small_button(parent, text, command):
    style = {**ACTION_BUTTON_STYLE, "font": ("Poppins", 10, "bold"), "width": 8}
    Button(parent, text=text, command=command, **style).pack(side=LEFT, padx=4)
def entry(title, show=None):
    label(title)
    field = Entry(page_content, show=show, font=("Poppins", 12), width=30)
    field.pack(pady=5)
    return field
def dropdown(title, options, selected=None):
    label(title)
    variable = StringVar(value=selected or options[0])
    menu = OptionMenu(page_content, variable, *options)
    menu.config(font=("Poppins", 12), width=25, bg="white", fg=TEXT)
    menu.pack(pady=5)
    return variable

def form_entries(fields, values=None):
    entries = {name: entry(name, show) for name, show in fields}
    for name, value in zip(entries, values or ()):
        entries[name].insert(0, str(value))
    return entries
def member_gender(member):
    gender = member[9] if len(member) > 9 else GENDERS[0]
    return gender if gender in GENDERS else GENDERS[0]
def member_form(member=None):
    values = (member[1], member[2], member[3], member[4], member[7]) if member else None
    fields = form_entries([(name, None) for name in MEMBER_FIELDS], values)
    gender = member_gender(member) if member else GENDERS[0]
    goal = dropdown("Goal", GOALS, member[5] if member else GOALS[0])
    return fields, goal, dropdown("Gender", GENDERS, gender)
def member_form_values(fields, goal_var, gender_var):
    values = (fields[name].get() for name in MEMBER_FIELDS)
    name, age, height, weight, password = values
    return name, int(age), float(height), float(weight), goal_var.get(), password, gender_var.get()
def get_member_fitness(member_id):
    return next((record for record in backend.load_data("fitness.dat") if record[0] == member_id), None)
def member_detail_lines(member, id_label="ID"):
    details = [(id_label, member[0]), ("Name", member[1]), ("Age", member[2]),
               ("Height", f"{member[3]} cm"), ("Weight", f"{member[4]} kg"),
               ("Goal", member[5]), ("Gender", member_gender(member)),
               ("Joined", member[6]), ("Status", "Active" if member[8] else "Inactive")]
    return [f"{name}: {value}" for name, value in details]
def show_lines(lines, size=12, pady=2):
    for item in lines:
        label(item, size, pady=pady)
def detail_page(title, lines_func, action_text, action_func, back_func, empty_text=None):
    start_page(title)
    lines = lines_func()
    if lines is None:
        label(empty_text, 14)
    else:
        show_lines(lines)
    button(action_text, action_func, pady=14)
    button("Back", back_func, pady=0)
def show_logo():
    top = Frame(page_content, bg=BG)
    top.pack(fill="x")
    if LOGO_FILE.exists():
        window.logo_image = PhotoImage(file=str(LOGO_FILE))
        Label(top, image=window.logo_image, bg=BG).pack(pady=(12, 0))
    else:
        Label(top, text="FitPulse", font=("Poppins", 34, "bold"), bg=BG, fg=TEXT).pack(pady=(12, 0))
    Label(top, text="Gains, Tracked.",
          font=("Poppins", 12), bg=BG, fg=MUTED).pack(pady=(0, 10))
def start_page(title):
    clear_window()
    window.unbind("<MouseWheel>")
    create_page()
    show_logo()
    label(title, 22, "bold", pady=16)
def add_member(name, age, height, weight, goal, password, gender):
    member_id = backend.add_member(
        name, age, height, weight, goal, date.today().isoformat(), password, gender
    )
    backend.update_membership(member_id, "Gold", "monthly")
    backend.update_workout_plan(member_id, goal, "Medium", 3)
    return member_id
def member_name_map():
    return {member[0]: member[1] for member in backend.load_data("members.dat")}
def records_page(title, records, empty_text, formatter, back=None, header=None):
    start_page(title)
    if header:
        header()
    if not records:
        label(empty_text, 14)
    else:
        for record in records:
            label(formatter(record), 13, pady=3)
    button("Back", back or admin_dashboard, pady=20)
def lookup_action(get_record, on_found, not_found_msg="Not Found", error_msg="Invalid ID",
                   exceptions=(ValueError, TypeError)):
    try:
        record = get_record()
        if record:
            on_found(record)
        else:
            messagebox.showerror("Error", not_found_msg)
    except exceptions:
        messagebox.showerror("Error", error_msg)
def entity_lookup_page(title, id_label, action_text, search_func, on_found, not_found_msg, back):
    start_page(title)
    id_field = entry(id_label)
    def submit():
        lookup_action(lambda: search_func(int(id_field.get())), on_found, not_found_msg)
    action_row((action_text, submit), ("Back", back))
def member_lookup_page(title, action_text, on_member):
    entity_lookup_page(title, "Member ID", action_text, backend.search_member_by_id,
                        on_member, "Member Not Found", manage_members_page)
def home_page():
    global current_admin
    current_admin = None
    start_page("Welcome to Alappuzha Gymkhana!")
    button("Admin Login", admin_login_page)
    button("User Login", user_login_page)
def login_page(title, id_title, login_func, success_func):
    start_page(title)
    id_field = entry(id_title)
    password_field = entry("Password", show="*")
    def login():
        lookup_action(
            lambda: login_func(int(id_field.get()), password_field.get()),
            success_func, "Wrong ID or Password", "Invalid Details",
            exceptions=(ValueError, TypeError, IndexError),
        )
    button("Login", login, pady=20)
    button("Back", home_page, pady=0)
def admin_login_page():
    login_page("Admin Login", "Admin ID", backend.admin_login, admin_dashboard)
def user_login_page():
    login_page("User Login", "Member ID", backend.user_login, user_dashboard)
def menu_page(title, items, back_func=None, subtitle=None):
    start_page(title)
    if subtitle:
        label(subtitle, 13, fg=MUTED, pady=2)
    for text, command in items:
        button(text, command)
    if back_func:
        button("Back", back_func, pady=20)
def admin_dashboard(admin=None):
    global current_admin
    if admin is not None:
        current_admin = admin
    subtitle = None
    if current_admin:
        subtitle = f"Logged in as: {current_admin[1]} | Position: {current_admin[2]}"
    menu_page(
        "Admin Dashboard",
        [
            ("Membership Fees", membership_page),
            ("Attendance Logs", attendance_page),
            ("Deletion Logs", deletion_logs_page),
            ("Manage Admins", admin_controls_page),
            ("Manage Members", manage_members_page),
            ("Logout", home_page),
        ],
        subtitle=subtitle,
    )
def membership_page():
    names = member_name_map()
    memberships = backend.load_data("membership.dat")
    def header():
        label("Total Fees Earned", 18, pady=4)
        label("Rs. " + str(backend.get_total_fees_earned()), 28, "bold", fg="green", pady=8)
        if memberships:
            label("Member payment details", 16, "bold", pady=8)
    def formatter(m):
        member_id, plan, duration, fee, paid_on, expiry, visits, last_visit, auto_pay = m[:9]
        return (f"{names.get(member_id, 'Unknown')} ({member_id}) | "
                f"{plan} {duration} | Paid Rs. {fee} on {paid_on} | "
                f"Expires {expiry} | Visits {visits}")
    records_page("Membership Fees", memberships, "No membership payments found",
                 formatter, admin_dashboard, header)
def attendance_page():
    names = member_name_map()
    records_page("Attendance Logs", backend.load_data("attendance.dat"), "No Attendance Logs",
        lambda r: f"{names.get(r[0], 'Unknown')} ({r[0]}) - {r[1]} - {r[2]} - Streak {r[3] if len(r) > 3 else 1}")
def deletion_logs_page():
    records_page("Deletion Logs", reversed(backend.load_data("deletion_logs.dat")), "No Deletion Logs",
        lambda r: f"{r[4] if len(r) > 4 else 'Member'}: {r[1]} ({r[0]}) - {r[3]} - {r[2]}")
def manage_members_page():
    menu_page(
        "Manage Members",
        [
            ("Add Member", member_editor_page),
            ("Delete Member", delete_member_page),
            ("Edit Member", edit_member_lookup_page),
            ("Search Member", search_member_page),
        ],
        admin_dashboard,
    )
def entity_delete_page(title, id_label, search_func, delete_func, label_func,
                        default_reason, back, record=None):
    start_page(title)
    entity = title.split()[-1]
    id_field = None if record else entry(id_label)
    if record:
        label(label_func(record), 14, "bold")
    reason_field = entry("Deletion Reason")
    def remove():
        target = record
        if target is None:
            try:
                target = search_func(int(id_field.get()))
            except (ValueError, TypeError):
                messagebox.showerror("Error", "Invalid ID")
                return
        if not target:
            messagebox.showerror("Error", f"{entity} Not Found")
            return
        if not messagebox.askyesno("Confirm Deletion", f"Delete {label_func(target)}?\nThis cannot be undone."):
            return
        reason = reason_field.get().strip() or default_reason
        if delete_func(target[0], reason):
            messagebox.showinfo("Success", f"{entity} Deleted")
            back()
        else:
            messagebox.showerror("Error", f"{entity} Not Found")
    action_row(("Delete", remove), ("Back", back))
def delete_member_page():
    entity_delete_page("Delete Member", "Member ID", backend.search_member_by_id,
                        backend.delete_member, lambda m: f"{m[1]} ({m[0]})",
                        "Deleted from admin UI", manage_members_page)
def admin_controls_page():
    menu_page(
        "Manage Admins",
        [
            ("Add Admin", admin_editor_page),
            ("Search Admin", search_admin_page),
            ("Edit Admin", edit_admin_lookup_page),
            ("Delete Admin", admin_delete_form_page),
        ],
        admin_dashboard,
    )
def admin_lookup_page(title, action_text, callback):
    entity_lookup_page(title, "Admin ID", action_text, backend.search_admin_by_id,
                        callback, "Admin Not Found", admin_controls_page)
def editor_page(title, build_fields, save_func, save_text, back, error_msg="Invalid Details"):
    start_page(title)
    fields = build_fields()
    save_row(save_text, lambda: save_func(fields), back, back, error_msg)
    return fields
def admin_editor_page(admin=None):
    editing = admin is not None
    values = (admin[1], admin[2], admin[3]) if editing else None
    def save(fields):
        name = fields["Name"].get().strip()
        position = fields["Position"].get().strip()
        password = fields["Password"].get()
        if not name or not position or not password:
            raise ValueError("All fields are required")
        if editing:
            backend.modify_admin(admin[0], name, position, password)
            return "Admin Updated"
        return f"Admin Added\nID: {backend.add_admin(name, position, password)}"
    editor_page("Edit Admin" if editing else "Add Admin",
                lambda: form_entries([("Name", None), ("Position", None), ("Password", "*")], values),
                save, "Save Changes" if editing else "Save Admin", admin_controls_page,
                "All fields are required")

def edit_admin_lookup_page():
    admin_lookup_page("Edit Admin", "Edit", admin_editor_page)
def result_row(parent, title_text, actions):
    row = Frame(parent, bg="white", highlightbackground="#d6dbe3", highlightthickness=1)
    row.pack(fill="x", padx=16, pady=4)
    Label(row, text=title_text, font=("Poppins", 12, "bold"), bg="white", fg=TEXT,
          anchor="w", width=34).pack(side=LEFT, padx=12, pady=8)
    for text, command in actions:
        small_button(row, text, command)
def search_admin_page():
    def row(parent, admin):
        result_row(parent, f"{admin[1]} ({admin[0]}) - {admin[2]}", [
            ("Edit", lambda: admin_editor_page(admin)),
            ("Delete", lambda: admin_delete_form_page(admin)),
        ])
    search_list_page("Search Admin", "Enter Admin ID or Name", "No matching admin found",
                      lambda: backend.load_data("admins.dat"), id_or_name_match, row, admin_controls_page)
def admin_delete_form_page(admin=None):
    entity_delete_page("Delete Admin", "Admin ID", backend.search_admin_by_id,
                        backend.delete_admin, lambda a: f"Admin: {a[1]} ({a[0]})",
                        "Deleted from Manage Admins", admin_controls_page, admin)
def edit_member_lookup_page():
    member_lookup_page("Edit Member", "Edit", member_editor_page)
def member_editor_page(member=None):
    is_editing = member is not None
    def build_fields():
        fields, goal_var, gender_var = member_form(member)
        fields["_goal"], fields["_gender"] = goal_var, gender_var
        return fields
    def save(fields):
        goal_var, gender_var = fields["_goal"], fields["_gender"]
        name, age, height, weight, goal, password, gender = member_form_values(
            fields, goal_var, gender_var
        )
        if is_editing:
            backend.modify_member(member[0], name, age, height, weight, goal, password, gender)
            backend.update_workout_plan(member[0], goal, "Medium", 3)
            return "Member Updated"
        member_id = add_member(name, age, height, weight, goal, password, gender)
        return "Member Added\nID : " + str(member_id)
    editor_page("Edit Member" if is_editing else "Add Member", build_fields, save,
                "Save Changes" if is_editing else "Save Member", manage_members_page)
def search_list_page(title, placeholder, empty_text, load_func, matches_query, row_builder, back):
    start_page(title)
    search_field = entry(placeholder)
    label("Press Enter to search", 10, fg=MUTED, pady=(0, 6))
    result_box = Frame(page_content, bg=BG); result_box.pack(pady=12)
    results_canvas = Canvas(result_box, bg=BG, width=round(620 * UI_SCALE),
                            height=round(200 * UI_SCALE), highlightthickness=0)
    results_scrollbar = Scrollbar(result_box, orient=VERTICAL, command=results_canvas.yview)
    results_canvas.configure(yscrollcommand=results_scrollbar.set)
    results_scrollbar.pack(side=RIGHT, fill=Y)
    results_canvas.pack(side=LEFT, fill=BOTH, expand=True)
    results_frame = Frame(results_canvas, bg=BG)
    results_window = results_canvas.create_window((0, 0), window=results_frame, anchor="nw")
    results_frame.bind("<Configure>", lambda event: results_canvas.configure(
        scrollregion=results_canvas.bbox("all")))
    results_canvas.bind("<Configure>", lambda event: results_canvas.itemconfigure(
        results_window, width=event.width))
    def scroll_results(event):
        direction = -1 if event.delta > 0 else 1
        results_canvas.yview_scroll(direction, "units")
        return "break"
    window.bind("<MouseWheel>", scroll_results)
    def show_matches(event=None):
        for widget in results_frame.winfo_children():
            widget.destroy()
        query = search_field.get().strip().lower()
        matches = [item for item in load_func() if matches_query(item, query)]
        if not matches:
            label(empty_text, 12, parent=results_frame)
        else:
            for item in matches:
                row_builder(results_frame, item)
    search_field.bind("<Return>", show_matches)
    show_matches()
    button("Back", back, pady=16)
def id_or_name_match(item, query):
    return not query or query in str(item[0]) or query in item[1].lower()
def search_member_page():
    def row(parent, member):
        result_row(parent, f"{member[1]} ({member[0]})", [
            ("View", lambda: view_member_page(member)),
            ("Edit", lambda: member_editor_page(member)),
        ])
    search_list_page("Search Member", "Enter Member ID or Name", "No matching member found",
                      lambda: backend.load_data("members.dat"), id_or_name_match, row, manage_members_page)
def view_member_page(member):
    def lines():
        details = member_detail_lines(member)
        membership = backend.get_membership_info(member[0])
        if membership:
            details.append(
                f"Membership: {membership[1]} {membership[2]}, Rs. {membership[3]}, paid {membership[4]}"
            )
        return details
    detail_page("Member Details", lines, "Edit", lambda: member_editor_page(member), search_member_page)
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
    suggestions = {
        "Underweight": "Eat more calories and focus on strength training.",
        "Normal": "BMI is in a healthy range. Maintain your routine.",
        "Overweight": "Add regular cardio and keep calories controlled.",
    }
    return suggestions.get(category, "Focus on low-impact cardio and a steady calorie deficit.")
def user_profile_page(member):
    member = backend.search_member_by_id(member[0]) or member
    def lines():
        bmi, category = backend.calculate_bmi(member[4], member[3])
        return member_detail_lines(member, "Member ID") + [
            f"BMI: {bmi} ({category})",
            "BMI Analysis: " + bmi_suggestion(category),
        ]
    detail_page("Profile", lines, "Update Body Stats",
                lambda: update_body_stats_page(member), lambda: user_dashboard(member))
def update_body_stats_page(member):
    start_page("Update Body Stats")
    weight_field = entry("Weight")
    height_field = entry("Height")
    weight_field.insert(0, str(member[4]))
    height_field.insert(0, str(member[3]))
    def do_update():
        bmi, category = backend.update_body_stats(
            member[0], float(weight_field.get()), float(height_field.get())
        )
        return f"BMI: {bmi} ({category})"
    def refresh():
        user_profile_page(backend.search_member_by_id(member[0]) or member)
    save_row("Save", do_update, refresh, lambda: user_profile_page(member), "Invalid height or weight")
def user_membership_page(member):
    def lines():
        membership = backend.get_membership_info(member[0])
        if not membership:
            return None
        member_id, plan, duration, fee, start, expiry, visits, last_visit, auto_pay = membership[:9]
        try:
            days_left = (date.fromisoformat(expiry) - date.today()).days
        except (ValueError, TypeError):
            days_left = 0
        return [f"Plan: {plan}", f"Duration: {duration}", f"Fee Paid: Rs. {fee}",
                f"Start Date: {start}", f"Expiry Date: {expiry}",
                f"Days Remaining: {days_left}", f"Days Visited: {visits}",
                f"Last Visit: {last_visit or 'Not marked'}"]
    detail_page("Membership", lines, "Change Plan", lambda: change_membership_page(member),
                lambda: user_dashboard(member), "No membership found")
def change_membership_page(member):
    start_page("Change Membership Plan")
    current = backend.get_membership_info(member[0])
    selected_plan = current[1] if current and current[1] in PLANS else PLANS[0]
    selected_duration = current[2] if current and current[2] in DURATIONS else DURATIONS[0]
    plan_var = dropdown("Plan", PLANS, selected_plan)
    duration_var = dropdown("Duration", DURATIONS, selected_duration)
    def do_update():
        backend.update_membership(member[0], plan_var.get(), duration_var.get())
        return "Membership Updated"
    save_row("Save Plan", do_update, lambda: user_membership_page(member),
              lambda: user_membership_page(member), "Invalid Plan")
def user_workout_page(member):
    def lines():
        fitness = get_member_fitness(member[0])
        if not fitness:
            backend.update_workout_plan(member[0], member[5], "Medium", 3)
            fitness = get_member_fitness(member[0])
        if not fitness:
            return None
        member_id, workout, intensity, frequency, diet_type, calorie_mode, progress = fitness[:7]
        diet = ["- " + item for item in backend.get_diet_plan(member[5], member_gender(member))]
        return [f"Workout Plan: {workout}", f"Intensity: {intensity}", f"Frequency: {frequency} days/week",
                f"Diet Type: {diet_type}", f"Calorie Mode: {calorie_mode}", "Diet Plan:"] + diet
    detail_page("Workout & Diet", lines, "Change Workout",
                lambda: change_workout_page(member), lambda: user_dashboard(member))
def change_workout_page(member):
    start_page("Change Workout")
    goal_var = dropdown("Goal", GOALS, member[5])
    intensity_var = dropdown("Intensity", INTENSITIES, "Medium")
    frequency_field = entry("Frequency Per Week")
    frequency_field.insert(0, "3")
    def do_update():
        backend.modify_member(member[0], goal=goal_var.get())
        backend.update_workout_plan(member[0], goal_var.get(), intensity_var.get(), int(frequency_field.get()))
        return "Workout Updated"
    def refresh():
        user_workout_page(backend.search_member_by_id(member[0]) or member)
    save_row("Save Workout", do_update, refresh, lambda: user_workout_page(member), "Invalid Workout Details")
def main():
    initialize_window()
    create_files()
    home_page()
    window.mainloop()
if __name__ == "__main__":
    main()
