import pickle
import random
from datetime import date, datetime, timedelta

def load_data(filename):
    data = []
    try:
        file = open(filename, "rb")
        while True:
            try:
                record = pickle.load(file)
                data.append(record)
            except EOFError:
                break
        file.close()
    except FileNotFoundError:
        return []
    return data

def save_data(filename, data):
    file = open(filename, "wb")

    for record in data:
        pickle.dump(record, file)

    file.close()

def load_admins():
    return load_data("admins.dat")

def save_admins(admins):
    save_data("admins.dat", admins)

def add_admin(name, position, password):
    admins = load_admins()
    while True:
        admin_id = random.randint(1000, 9999)
        found = False
        for admin in admins:
            if admin[0] == admin_id:
                found = True
                break
        if found == False:
            break
    new_admin = [admin_id, name, position, password]
    admins.append(new_admin)
    save_admins(admins)
    return admin_id

def admin_login(admin_id, password):
    admins = load_admins()
    for admin in admins:
        if admin[0] == admin_id and admin[3] == password:
            return admin
    return None

def load_members():
    return load_data("members.dat")

def save_members(members):
    save_data("members.dat", members)

def add_member(name, age, height, weight, goal, join_date, password):
    members = load_members()
    while True:
        member_id = random.randint(100000, 999999)
        exists = False
        for member in members:
            if member[0] == member_id:
                exists = True
                break
        if exists == False:
            break
    status = True
    new_member = [
        member_id,
        name,
        age,
        height,
        weight,
        goal,
        join_date,
        password,
        status
    ]
    members.append(new_member)
    save_members(members)
    return member_id

def modify_member(member_id, name=None, age=None, height=None,
                  weight=None, goal=None, password=None):
    members = load_members()
    for member in members:
        if member[0] == member_id:
            if name != None:
                member[1] = name
            if age != None:
                member[2] = age
            if height != None:
                member[3] = height
            if weight != None:
                member[4] = weight
            if goal != None:
                member[5] = goal
            if password != None:
                member[7] = password
            save_members(members)
            return True
    return False

def delete_member(member_id, reason):
    members = load_members()
    new_members = []
    found = False
    for member in members:
        if member[0] != member_id:
            new_members.append(member)
        else:
            found = True
    if found == False:
        return False
    save_members(new_members)
    today = date.today().isoformat()
    log_file = open("deletions.log", "a")
    log_file.write(str(member_id) + " | " + today + " | " + reason + "\n" )
    log_file.close()
    return True

def search_member_by_id(member_id):
    members = load_members()
    for member in members:
        if member[0] == member_id:
            return member
    return None

# MEMBERSHIP FUNCTIONS

PLAN_FEES = {
    "GOLD_MONTHLY": 999,
    "GOLD_YEARLY": 9999,
    "PLATINUM_MONTHLY": 1499,
    "PLATINUM_YEARLY": 14999,
    "DIAMOND_MONTHLY": 1999,
    "DIAMOND_YEARLY": 19999
}

def load_memberships():
    return load_data("membership.dat")

def save_memberships(data):
    save_data("membership.dat", data)

def update_membership(member_id, plan, duration):
    memberships = load_memberships()
    today = date.today()
    if duration == "monthly":
        expiry_date = today + timedelta(days=30)
    else:
        expiry_date = today + timedelta(days=365)
    key = plan.upper() + "_" + duration.upper()
    fee = PLAN_FEES[key]
    found = False
    for membership in memberships:
        if membership[0] == member_id:
            membership[1] = plan
            membership[2] = duration
            membership[3] = fee
            membership[4] = today.isoformat()
            membership[5] = expiry_date.isoformat()
            found = True
            break
    if found == False:
        new_membership = [
            member_id,
            plan,
            duration,
            fee,
            today.isoformat(),
            expiry_date.isoformat(),
            0
        ]
        memberships.append(new_membership)
    save_memberships(memberships)
    return True

def get_membership_info(member_id):
    memberships = load_memberships()
    for membership in memberships:
        if membership[0] == member_id:
            return membership
    return None

def get_total_fees_earned():
    memberships = load_memberships()
    total = 0
    for membership in memberships:
        total = total + membership[3]
    return total

def check_expiry(member_id):
    memberships = load_memberships()
    today = date.today().isoformat()
    for membership in memberships:
        if membership[0] == member_id:
            expiry = membership[5]
            if today > expiry:
                members = load_members()
                for member in members:
                    if member[0] == member_id:
                        member[8] = False
                        break
                save_members(members)
                return False
    return True

def load_attendance():
    return load_data("attendance.dat")

def save_attendance(data):
    save_data("attendance.dat", data)

def mark_attendance(member_id):
    attendance = load_attendance()
    today = date.today().isoformat()
    current_time = datetime.now().strftime("%H:%M:%S")
    for record in attendance:
        if record[0] == member_id and record[1] == today:
            return False
    new_record = [member_id, today, current_time]
    attendance.append(new_record)
    save_attendance(attendance)
    memberships = load_memberships()
    for membership in memberships:
        if membership[0] == member_id:
            membership[6] = membership[6] + 1
            break
    save_memberships(memberships)
    return True

def get_attendance_logs():
    return load_attendance()

def get_daily_summary():
    attendance = load_attendance()
    members = load_members()
    today = date.today().isoformat()
    total_present = 0
    for record in attendance:
        if record[1] == today:
            total_present = total_present + 1
    total_members = 0
    for member in members:
        if member[8] == True:
            total_members = total_members + 1
    absent = total_members - total_present
    summary = {
        "present": total_present,
        "absent": absent,
        "total_members": total_members
    }
    return summary

# BMI FUNCTIONS

def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100
    bmi = weight / (height_m * height_m)
    bmi = round(bmi, 2)
    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"
    return bmi, category

# BODY STATS

def load_body_stats():
    return load_data("bodystats.dat")

def save_body_stats(data):
    save_data("bodystats.dat", data)

def update_body_stats(member_id, weight, height):
    stats = load_body_stats()
    today = date.today().isoformat()
    bmi, category = calculate_bmi(weight, height)
    new_record = [
        member_id,
        today,
        weight,
        height,
        bmi,
        category
    ]
    stats.append(new_record)
    save_body_stats(stats)
    return bmi, category

# FITNESS FUNCTIONS

def load_fitness():
    return load_data("fitness.dat")

def save_fitness(data):
    save_data("fitness.dat", data)

def get_diet_plan(goal):
    if goal == "Weight Loss":
        return [
            "High Protein Diet",
            "Avoid Junk Food",
            "Drink More Water",
            "Eat More Fruits"
        ]
    elif goal == "Muscle Gain":
        return [
            "Protein Rich Foods",
            "Eggs and Chicken",
            "Bananas and Peanut Butter",
            "Eat More Calories"
        ]
    else:
        return [
            "Balanced Diet",
            "Eat Vegetables",
            "Stay Hydrated",
            "Avoid Excess Sugar"
        ]

def update_workout_plan(member_id, goal, intensity, frequency):
    fitness = load_fitness()
    if goal == "Weight Loss":
        workout = "Cardio"
    elif goal == "Muscle Gain":
        workout = "Strength Training"
    else:
        workout = "Mixed Workout"
    diet = get_diet_plan(goal)
    found = False
    for record in fitness:
        if record[0] == member_id:
            record[1] = workout
            record[2] = intensity
            record[3] = frequency
            record[4] = diet
            found = True
            break
    if found == False:
        new_record = [
            member_id,
            workout,
            intensity,
            frequency,
            diet
        ]
        fitness.append(new_record)
    save_fitness(fitness)
    return True

def get_profile_details(member_id):
    member = search_member_by_id(member_id)
    if member == None:
        return None
    fitness = load_fitness()
    stats = load_body_stats()
    profile = {}
    profile["member"] = member
    for record in fitness:
        if record[0] == member_id:
            profile["fitness"] = record
            break
    latest_stat = None
    for record in stats:
        if record[0] == member_id:
            latest_stat = record
    profile["latest_stats"] = latest_stat
    return profile

def user_login(member_id, password):
    members = load_members()
    for member in members:
        if member[0] == member_id and member[7] == password:
            check_expiry(member_id)
            mark_attendance(member_id)
            return member
    return None
