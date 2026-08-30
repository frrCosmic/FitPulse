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
    "DIAMOND_YEARLY": 19999,}

# generic .dat file helpers
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

def find_record(filename, record_id):
    for record in load_data(filename):
        if record[0] == record_id:
            return record
    return None

def generate_unique_id(records, low, high):
    existing_ids = []
    for record in records:
        existing_ids.append(record[0])
    while True:
        new_id = random.randint(low, high)
        if new_id not in existing_ids:
            return new_id

# deletion logs record: record_id, name, reason, timestamp, [entity_label]
# entity_label is only added for admin deletions
def log_deletion(record, reason, entity_label=None):
    deletion_logs = load_data("deletion_logs.dat")
    if entity_label:
        deletion_logs.append([record[0], record[1], reason, datetime.now().isoformat(timespec="seconds"), entity_label])
    else:
        deletion_logs.append([record[0], record[1], reason, datetime.now().isoformat(timespec="seconds")])
    save_data("deletion_logs.dat", deletion_logs)

def delete_record(filename, record_id, reason, entity_label=None):
    records = load_data(filename)
    for index in range(len(records)):
        if records[index][0] == record_id:
            log_deletion(records[index], reason, entity_label)
            records.pop(index)
            save_data(filename, records)
            return True
    return False

# admin record: admin_id, name, position, password
def admin_login(admin_id, password):
    admin = find_record("admins.dat", admin_id)
    return admin if admin and admin[-1] == password else None

def add_admin(name, position, password):
    admins = load_data("admins.dat")
    admin_id = generate_unique_id(admins, 1000, 9999)
    admins.append([admin_id, name, position, password])
    save_data("admins.dat", admins)
    return admin_id

def search_admin_by_id(admin_id):
    return find_record("admins.dat", admin_id)

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
    return delete_record("admins.dat", admin_id, reason, "Admin")

# member record: member_id, name, age, height, weight, goal, join_date, password,is_active, gender
def user_login(member_id, password):
    member = find_record("members.dat", member_id)
    if member and member[7] == password:
        check_expiry(member_id)
        mark_attendance(member_id)
        return member
    return None

def add_member(name, age, height, weight, goal, join_date, password, gender=DEFAULT_GENDER):
    members = load_data("members.dat")
    member_id = generate_unique_id(members, 100000, 999999)
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
    gender=None,):
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
    return delete_record("members.dat", member_id, reason or "Deleted")

def search_member_by_id(member_id):
    return find_record("members.dat", member_id)

# membership records keep their existing field order; subscription status is stored at index 9.
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
            if len(membership) < 10:
                membership.append("Active")
            else:
                membership[9] = "Active"
            found = True
            break
    if not found:
        memberships.append([member_id, plan, duration, fee, today.isoformat(),
                            expiry.isoformat(), 0, "", "", "Active"])
    save_data("membership.dat", memberships)
    return True

def get_membership_info(member_id):
    return find_record("membership.dat", member_id)

def get_membership_status(member_id):
    membership = get_membership_info(member_id)
    return membership[9] if membership and len(membership) > 9 else "Active"

def cancel_membership(member_id):
    memberships = load_data("membership.dat")
    for membership in memberships:
        if membership[0] == member_id:
            if len(membership) < 10:
                membership.append("Inactive")
            else:
                membership[9] = "Inactive"
            save_data("membership.dat", memberships)
            return True
    return False

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

# attendance record: member_id, date, check_in_time, streak
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

# body stats record: member_id, date, weight, height, bmi, category
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
    members = load_data("members.dat")
    for member in members:
        if member[0] == member_id:
            member[3] = height
            member[4] = weight
            save_data("members.dat", members)
            break
    return bmi, category

# fitness record: member_id, workout, intensity, frequency, diet_type, calorie_mode, progress
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
        "Limit highly processed foods and excess sugar",],}

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
