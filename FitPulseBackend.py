import pickle
import random as r
from datetime import date, datetime, timedelta

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


# Admin records: admin_id, name, position, username/extra, password
def load_admins():
    return load_data("admins.dat")


def save_admins(admins):
    save_data("admins.dat", admins)


def admin_login(admin_id, password):
    admins = load_admins()
    for admin in admins:
        if admin[0] == admin_id and admin[-1] == password:
            return admin
    return None


# Member records: id, name, age, height, weight, goal, join_date, password, status
def load_members():
    return load_data("members.dat")


def save_members(members):
    save_data("members.dat", members)


def add_member(name, age, height, weight, goal, join_date, password):
    members = load_members()
    while True:
        member_id = r.randint(100000, 999999)
        exists = False
        for member in members:
            if member[0] == member_id:
                exists = True
                break
        if not exists:
            break

    members.append([member_id, name, age, height, weight, goal, join_date, password, True])
    save_members(members)
    return member_id


def modify_member(member_id, name=None, age=None, height=None, weight=None, goal=None, password=None):
    members = load_members()
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
            save_members(members)
            return True
    return False


def delete_member(member_id, reason=None):
    members = load_members()
    new_members = []
    found = False

    for member in members:
        if member[0] == member_id:
            found = True
        else:
            new_members.append(member)

    if not found:
        return False
    save_members(new_members)
    return True


def search_member_by_id(member_id):
    members = load_members()
    for member in members:
        if member[0] == member_id:
            return member
    return None


# Membership records: id, plan, duration, fee, start, expiry, visits, last_visit, auto_pay
def load_memberships():
    return load_data("membership.dat")


def save_memberships(memberships):
    save_data("membership.dat", memberships)


def update_membership(member_id, plan, duration):
    memberships = load_memberships()
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

    save_memberships(memberships)
    return True


def get_membership_info(member_id):
    memberships = load_memberships()
    for membership in memberships:
        if membership[0] == member_id:
            return membership
    return None


def get_total_fees_earned():
    total = 0
    memberships = load_memberships()
    for membership in memberships:
        total = total + membership[3]
    return total


def check_expiry(member_id):
    membership = get_membership_info(member_id)
    if membership is None:
        return True
    if date.today().isoformat() <= membership[5]:
        return True

    members = load_members()
    for member in members:
        if member[0] == member_id:
            member[8] = False
            save_members(members)
            break
    return False


# Attendance records: member_id, date, check_in_time, streak
def load_attendance():
    return load_data("attendance.dat")


def save_attendance(attendance):
    save_data("attendance.dat", attendance)


def mark_attendance(member_id):
    attendance = load_attendance()
    today = date.today().isoformat()
    yesterday = (date.today() - timedelta(days=1)).isoformat()

    for record in attendance:
        if record[0] == member_id and record[1] == today:
            return False

    streak = 1
    for record in attendance:
        if record[0] == member_id and record[1] == yesterday:
            streak = record[3] + 1

    attendance.append([member_id, today, datetime.now().strftime("%H:%M:%S"), streak])
    save_attendance(attendance)

    memberships = load_memberships()
    for membership in memberships:
        if membership[0] == member_id:
            membership[6] = membership[6] + 1
            membership[7] = today
            save_memberships(memberships)
            break
    return True


def get_attendance_logs():
    return load_attendance()


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
    members = load_members()
    for member in members:
        if member[0] == member_id:
            member[3] = height
            member[4] = weight
            save_members(members)
            break
    return bmi, category


# Fitness records: id, workout, intensity, frequency, diet_type, calorie_mode, progress
def load_fitness():
    return load_data("fitness.dat")


def save_fitness(fitness):
    save_data("fitness.dat", fitness)


def get_diet_plan(goal):
    if goal == "Weight Loss":
        return ["Low carb meals", "Calorie deficit", "More fruits and vegetables", "Avoid sugary drinks"]
    elif goal == "Muscle Gain":
        return ["High protein meals", "Calorie surplus", "Eggs, paneer, chicken or dal", "Banana, peanut butter and milk"]
    else:
        return ["Balanced Diet", "Eat Vegetables", "Stay Hydrated", "Avoid Excess Sugar"]


def get_fitness_logic(goal):
    if goal == "Weight Loss":
        return "Cardio", "Low Carb", "Deficit"
    elif goal == "Muscle Gain":
        return "Strength Training", "High Protein", "Surplus"
    else:
        return "Mixed Workout", "Balanced", "Maintenance"


def update_workout_plan(member_id, goal, intensity, frequency):
    fitness = load_fitness()
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

    save_fitness(fitness)
    return True


def user_login(member_id, password):
    members = load_members()
    for member in members:
        if member[0] == member_id and member[7] == password:
            check_expiry(member_id)
            mark_attendance(member_id)
            return member
    return None
