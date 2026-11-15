# FitPulse

<p align="center">
  <strong>A simple gym management system built with Python and Tkinter.</strong><br>
  Manage members, memberships, attendance, fitness goals and more from one desktop application.
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img alt="GUI" src="https://img.shields.io/badge/GUI-Tkinter-2E8B57?style=for-the-badge">
  <img alt="Storage" src="https://img.shields.io/badge/Storage-Pickle%20%2F%20.dat-orange?style=for-the-badge">
  <img alt="Status" src="https://img.shields.io/badge/Project-Desktop%20App-111111?style=for-the-badge">
</p>

---

## ✨ Overview

**FitPulse** is a desktop-based gym management application designed to make everyday gym administration easier. It provides separate **Admin** and **Member** areas, with a straightforward interface built using **Tkinter**.

The application stores its records locally in binary `.dat` files using Python's `pickle` module.

## 🚀 Features

### 🛡️ Admin dashboard
- **Admin login** with ID and password.
- **Membership fees:** view membership payment records and total fees earned.
- **Attendance logs:** review member check-ins and attendance streaks.
- **Deletion logs:** view deleted records, reasons and timestamps.
- **Manage members:** add, search, view, edit and delete member records.
- **Manage admins:** add, search, edit and delete administrator records.

### 💪 Member dashboard
- **Profile:** view personal details, BMI and a basic BMI analysis.
- **Body statistics:** update height and weight; BMI is recalculated.
- **Membership:** view plan details, payment, expiry, remaining days and visits.
- **Plan management:** change or cancel a membership.
- **Workout & diet:** view a goal-based workout recommendation and diet suggestions, and update workout intensity and weekly frequency.

### ⚙️ Automatic tasks
- A successful member login checks membership expiry and records attendance.
- A member can only receive one attendance entry per day.
- Consecutive-day attendance streaks are tracked.
- Expired memberships cause the member account to be marked inactive.

## 🧰 Tech stack

| Technology | Purpose |
| --- | --- |
| Python | Application logic |
| Tkinter | Desktop graphical user interface |
| Pickle | Reading and writing Python objects |
| Binary `.dat` files | Local data storage |
| `datetime` | Dates, membership expiry and attendance timestamps |
| `random` | Generating unique member and admin IDs |

## 📁 Project structure

```text
FitPulse/
├── FitPulseMain.py       # Tkinter application and user interface
├── FitPulseBackend.py    # Data handling and application functions
├── README.md             # Project documentation
├── files.zip             # Additional project files
└── assets/
    └── fitpulse_logo.png # Optional application logo
```

The application creates its required `.dat` data files in the working directory when it runs. Keep these files together with the Python files so existing records remain available.

## ▶️ Getting started

### 1. Install Python

Install Python 3 from [python.org](https://www.python.org/downloads/). Tkinter is included with most standard Windows Python installations.

### 2. Download the project

Clone the repository:

```bash
git clone https://github.com/frrCosmic/FitPulse.git
cd FitPulse
```

Or use **Code → Download ZIP** on this GitHub page and extract the downloaded folder.

### 3. Run FitPulse

Make sure `FitPulseMain.py` and `FitPulseBackend.py` are in the same folder, then run:

```bash
python FitPulseMain.py
```

No separate database server is required.

## 🔐 Demo login

On a fresh run, the application creates a default administrator account and sample member records if the corresponding data files do not already contain records.

| Account | ID | Password |
| --- | ---: | --- |
| Admin | `1001` | `admin123` |

Sample member accounts:

| Member | ID | Password |
| --- | ---: | --- |
| Arjun | `101001` | `arjun123` |
| Rahul | `101002` | `rahul123` |
| Neeraj | `101003` | `neeraj123` |
| Aditya | `101004` | `aditya123` |
| Vishnu | `101005` | `vishnu123` |

> **Note:** These are default demonstration credentials created by the application. Change or remove them before using the application with real member information. The application stores passwords in local data files, so it is intended as an educational/demo project rather than a production authentication system.

## 🏷️ Membership plans

The backend defines the following plan fees:

| Plan | Monthly | Yearly |
| --- | ---: | ---: |
| Gold | ₹999 | ₹9,999 |
| Platinum | ₹1,499 | ₹14,999 |
| Diamond | ₹1,999 | ₹19,999 |

## 🧠 Fitness goal logic

FitPulse uses the selected fitness goal to suggest a basic workout and diet direction.

| Fitness goal | Workout recommendation | Diet direction | Calorie mode |
| --- | --- | --- | --- |
| Weight Loss | Cardio | Low Carb | Deficit |
| Muscle Gain | Strength Training | High Protein | Surplus |
| Maintain | Mixed Workout | Balanced | Maintenance |

The diet suggestions are general examples, not personalised medical or nutrition advice.

## 💾 Data files

The program uses local binary files to keep records between runs:

| File | Stores |
| --- | --- |
| `admins.dat` | Administrator records |
| `members.dat` | Member profiles |
| `membership.dat` | Membership plans and payment information |
| `attendance.dat` | Check-in dates, times and streaks |
| `bodystats.dat` | Body-stat history and BMI records |
| `fitness.dat` | Workout and diet settings |
| `deletion_logs.dat` | Deletion history |

These files are generated as needed by the application. **Back them up** before deleting or replacing them.

## 📌 Notes

- This is a local desktop application; it does not use an online account system or remote database.
- Keep the backend and main application files in the same directory.
- The logo is optional. Without `assets/fitpulse_logo.png`, the interface displays a text heading instead.
- Demo passwords are included for testing and should not be used for real accounts.

---

<p align="center">
  Made as a Python gym management project · <strong>FitPulse — Gains, Tracked.</strong>
</p>
