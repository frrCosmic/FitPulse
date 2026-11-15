<div align="center">
  <h1>FITPULSE</h1>
  <p><sub>Gains, Tracked.</sub></p>
  <p>A gym management desktop app made with Python and Tkinter.</p>
</div>

---

## About

FitPulse keeps a gym's member, membership and attendance records in one place. It has two sections: **Admin Mode** for managing the gym and **Member Mode** for viewing personal fitness and membership details.

The interface follows the same simple black-and-white style throughout the app.

## What you can do

### Admin Mode

- Add, search, view, edit and delete members.
- Add, search, edit and remove admin accounts.
- Check membership payments and total fees earned.
- View attendance records and visit streaks.
- Review deletion records, including the reason and time of deletion.

### Member Mode

- View profile details and BMI analysis.
- Update height and weight.
- Check membership plan, fee, expiry date and visits.
- Change or cancel a membership.
- View the suggested workout and diet plan.
- Change fitness goal, workout intensity and weekly frequency.

### Automatic tasks

When a member logs in, FitPulse checks the membership expiry date and records the visit. It does not add another attendance entry for the same member on the same day. Consecutive daily visits are counted as a streak.

## Built with

- **Python** — application logic
- **Tkinter** — desktop interface
- **Pickle** — saving and loading records
- **Binary files** — local data storage in `.dat` files

## Project files

```
FitPulse/
├── FitPulseMain.py
├── FitPulseBackend.py
└── README.md
```

`FitPulseMain.py` contains the Tkinter screens and navigation. `FitPulseBackend.py` handles member records, memberships, attendance, BMI and fitness-plan data.

The app creates its data files in the working directory when needed. Keep the `.dat` files with the project if you want to retain existing records.

## Run FitPulse

You need Python 3 installed. On Windows, Tkinter is normally included with the standard Python installation.

1. Download the repository using **Code → Download ZIP**, or clone it:

   ```bash
   git clone https://github.com/frrCosmic/FitPulse.git
   cd FitPulse
   ```

2. Run the main file:

   ```bash
   python FitPulseMain.py
   ```

No separate database setup is required.

## Default login

On the first run, the app creates a default admin account and sample member accounts if the relevant data files are empty.

| Account | ID | Password |
| --- | --- | --- |
| Admin | `1001` | `admin123` |

Sample member logins are also created:

| Member | ID | Password |
| --- | --- | --- |
| Arjun | `101001` | `arjun123` |
| Rahul | `101002` | `rahul123` |
| Neeraj | `101003` | `neeraj123` |
| Aditya | `101004` | `aditya123` |
| Vishnu | `101005` | `vishnu123` |

These are only for trying out the project. The passwords are stored locally in the data files, so do not use the demo setup for real member accounts.

## Membership plans

| Plan | Monthly | Yearly |
| --- | ---: | ---: |
| Gold | ₹999 | ₹9,999 |
| Platinum | ₹1,499 | ₹14,999 |
| Diamond | ₹1,999 | ₹19,999 |

---

<div align="center">
  <sub>FITPULSE · Gains, Tracked.</sub>
</div>
