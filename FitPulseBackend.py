import pickle
import random
from datetime import date, datetime, timedelta

DEFAULT_GENDER = "Male"
PLAN_FEES = {
    "GOLD_MONTHLY": 999,
    "GOLD_YEARLY": 9999,
    "PLATINUM_MONTHLY": 1499,
    "PLATINUM_YEARLY": 14999,
    "DIAMOND_MONTHLY": 1999,
    "DIAMOND_YEARLY": 19999,
}

def load_data(filename):
    data_list = []
    try:
        with open(filename, "rb") as file:
            while True:
                try:
                    data_list.append(pickle.load(file))
                except EOFError:
                    break
    except FileNotFoundError:
        return []
    return data_list

def save_data(filename, data_list):
    with open(filename, "wb") as file:
        for data in data_list:
            pickle.dump(data, file)

def user_login(member_id, password):
    members = load_data("members.dat")
    for member in members:
        if member[0] == member_id and member[7] == password:
            check_expiry(member_id)
            mark_attendance(member_id)
            return member
    return None

def admin_login(admin_id, password):
    admins = load_data("admins.dat")
    for admin in admins:
        if admin[0] == admin_id and admin[-1] == password:
            return admin
    return None

def add_admin(name, position, password):
    admins = load_data("admins.dat")
    existing_ids = {admin[0] for admin in admins}
    while True:
        admin_id = random.randint(1000, 9999)
        if admin_id not in existing_ids:
            break
    admins.append([admin_id, name, position, password])
    save_data("admins.dat", admins)
    return admin_id

def search_admin_by_id(admin_id):
    for admin in load_data("admins.dat"):
        if admin[0] == admin_id:
            return admin
    return None

def modify_admin(admin_id, name=None, position=None, password=None):
    admins = load_data("admins.dat")
    for admin in admins:
        if admin[0] == admin_id:
            if name is not None:
                admin[1] = name
            if position is not None:
                admin[2] = position
            if password is not None:
                admin[3] = password
            save_data("admins.dat", admins)
            return True
    return False

def delete_admin(admin_id, reason="Deleted from Manage Admins"):
    admins = load_data("admins.dat")
    for index, admin in enumerate(admins):
        if admin[0] == admin_id:
            deletion_logs = load_data("deletion_logs.dat")
            deletion_logs.append(
                [
                    admin[0],
                    admin[1],
                    reason,
                    datetime.now().isoformat(timespec="seconds"),
                    "Admin",
                ]
            )
            save_data("deletion_logs.dat", deletion_logs)
            admins.pop(index)
            save_data("admins.dat", admins)
            return True
    return False

def add_member(name, age, height, weight, goal, join_date, password, gender=DEFAULT_GENDER):
    members = load_data("members.dat")
    while True:
        member_id = random.randint(100000, 999999)
        exists = False
        for member in members:
            if member[0] == member_id:
                exists = True
                break
        if not exists:
            break
    members.append([member_id, name, age, height, weight, goal, join_date, password, True, gender])
    save_data("members.dat", members)
    return member_id

def modify_member(
    member_id,
    name=None,
    age=None,
    height=None,
    weight=None,
    goal=None,
    password=None,
    gender=None,
):
    members = load_data("members.dat")
    for member in members:
        if member[0] == member_id:
            if name is not None:
                member[1] = name
            if age is not None:
                member[2] = age
            if height is not None:
                member[3] = height
            if weight is not None:
                member[4] = weight
            if goal is not None:
                member[5] = goal
            if password is not None:
                member[7] = password
            if gender is not None:
                if len(member) < 10:
                    member.append(gender)
                else:
                    member[9] = gender
            save_data("members.dat", members)
            return True
    return False

def delete_member(member_id, reason=None):
    members = load_data("members.dat")
    for index, member in enumerate(members):
        if member[0] != member_id:
            continue
        deletion_logs = load_data("deletion_logs.dat")
        deletion_logs.append([
            member[0],
            member[1],
            reason or "Deleted",
            datetime.now().isoformat(timespec="seconds"),])
        save_data("deletion_logs.dat", deletion_logs)
        members.pop(index)
        save_data("members.dat", members)
        return True
    return False

def search_member_by_id(member_id):
    members = load_data("members.dat")
    for member in members:
        if member[0] == member_id:
            return member
    return None

def update_membership(member_id, plan, duration):
    memberships = load_data("membership.dat")
    today = date.today()
    if duration == "monthly":
        expiry = today + timedelta(days=30)
    else:
        expiry = today + timedelta(days=365)
    fee = PLAN_FEES[plan.upper() + "_" + duration.upper()]
    found = False
    for membership in memberships:
        if membership[0] == member_id:
            membership[1] = plan
            membership[2] = duration
            membership[3] = fee
            membership[4] = today.isoformat()
            membership[5] = expiry.isoformat()
            found = True
            break
    if not found:
        memberships.append([member_id, plan, duration, fee, today.isoformat(), expiry.isoformat(), 0, "", ""])
    save_data("membership.dat", memberships)
    return True

def get_membership_info(member_id):
    memberships = load_data("membership.dat")
    for membership in memberships:
        if membership[0] == member_id:
            return membership
    return None

def get_total_fees_earned():
    total = 0
    memberships = load_data("membership.dat")
    for membership in memberships:
        total = total + membership[3]
    return total

def check_expiry(member_id):
    membership = get_membership_info(member_id)
    if membership is None:
        return True
    if date.today().isoformat() <= membership[5]:
        return True
    members = load_data("members.dat")
    for member in members:
        if member[0] == member_id:
            member[8] = False
            save_data("members.dat", members)
            break
    return False

# Attendance records: member_id, date, check_in_time, streak
def mark_attendance(member_id):
    attendance = load_data("attendance.dat")
    current_date = date.today()
    today = current_date.isoformat()
    yesterday = (current_date - timedelta(days=1)).isoformat()
    if any(record[0] == member_id and record[1] == today for record in attendance):
        return False
    streak = 1
    for record in attendance:
        if record[0] == member_id and record[1] == yesterday:
            streak = record[3] + 1
            break
    attendance.append([member_id, today, datetime.now().strftime("%H:%M:%S"), streak])
    save_data("attendance.dat", attendance)

    memberships = load_data("membership.dat")
    for membership in memberships:
        if membership[0] == member_id:
            membership[6] += 1
            membership[7] = today
            save_data("membership.dat", memberships)
            break
    return True

def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100
    bmi = round(weight / (height_m * height_m), 2)
    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"
    return bmi, category

def update_body_stats(member_id, weight, height):
    stats = load_data("bodystats.dat")
    bmi, category = calculate_bmi(weight, height)
    stats.append([member_id, date.today().isoformat(), weight, height, bmi, category])
    save_data("bodystats.dat", stats)

    # Keep member height and weight equal to the latest body stats.
    members = load_data("members.dat")
    for member in members:
        if member[0] == member_id:
            member[3] = height
            member[4] = weight
            save_data("members.dat", members)
            break
    return bmi, category

# Fitness records: id, workout, intensity, frequency, diet_type, calorie_mode, progress
DIET_PLANS = {
    ("Male", "Weight Loss"): [
        "Choose lean proteins and plenty of vegetables",
        "Prefer whole grains and smaller portions",
        "Choose fruit or unsweetened snacks",
        "Limit fried foods and sugary drinks",
    ],
    ("Male", "Muscle Gain"): [
        "Include protein-rich foods in each meal",
        "Choose rice, oats, potatoes, or whole grains",
        "Include eggs, paneer, chicken, fish, or dal",
        "Add milk, fruit, or nuts as practical snacks",
    ],
    ("Male", "Maintain"): [
        "Build meals around vegetables and lean proteins",
        "Choose balanced portions of whole grains",
        "Drink water regularly through the day",
        "Limit highly processed foods and excess sugar",
    ],
    ("Female", "Weight Loss"): [
        "Choose lean proteins and plenty of vegetables",
        "Prefer whole grains and satisfying portions",
        "Choose fruit, yogurt, or unsweetened snacks",
        "Limit fried foods and sugary drinks",
    ],
    ("Female", "Muscle Gain"): [
        "Include protein-rich foods in each meal",
        "Choose oats, rice, potatoes, or whole grains",
        "Include eggs, paneer, chicken, fish, or dal",
        "Add milk, fruit, nuts, or yogurt as snacks",
    ],
    ("Female", "Maintain"): [
        "Build meals around vegetables and lean proteins",
        "Choose balanced portions of whole grains",
        "Drink water regularly through the day",
        "Limit highly processed foods and excess sugar",
    ],
}

def get_diet_plan(goal, gender=DEFAULT_GENDER):
    return DIET_PLANS.get((gender, goal), DIET_PLANS[(DEFAULT_GENDER, goal)])

def get_fitness_logic(goal):
    if goal == "Weight Loss":
        return "Cardio", "Low Carb", "Deficit"
    elif goal == "Muscle Gain":
        return "Strength Training", "High Protein", "Surplus"
    else:
        return "Mixed Workout", "Balanced", "Maintenance"

def update_workout_plan(member_id, goal, intensity, frequency):
    fitness = load_data("fitness.dat")
    workout, diet_type, calorie_mode = get_fitness_logic(goal)
    found = False
    for record in fitness:
        if record[0] == member_id:
            record[1] = workout
            record[2] = intensity
            record[3] = frequency
            record[4] = diet_type
            record[5] = calorie_mode
            found = True
            break
    if not found:
        fitness.append([member_id, workout, intensity, frequency, diet_type, calorie_mode, 0])
    save_data("fitness.dat", fitness)
    return True

