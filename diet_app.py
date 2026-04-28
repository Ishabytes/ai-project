import tkinter as tk
from tkinter import messagebox

# ------------------ LOGIC ------------------
def normalize_input(value):
    value = value.strip().lower()
    if value in ["m", "male"]:
        return "Male"
    if value in ["f", "female"]:
        return "Female"
    if value == "g":
        return "Invalid"   # handle wrong input
    return "Invalid"

def calculate_bmr(age, height, weight, gender):
    if gender == "Male":
        return 88.36 + (13.4 * weight) + (4.8 * height) - (5.7 * age)
    elif gender == "Female":
        return 447.6 + (9.2 * weight) + (3.1 * height) - (4.3 * age)
    else:
        return None

def calorie_needs(bmr, activity):
    factors = {
        "Sedentary": 1.2,
        "Light": 1.375,
        "Moderate": 1.55,
        "Active": 1.725,
        "Very Active": 1.9
    }
    return bmr * factors.get(activity, 1.2)

def calculate_bmi(weight, height):
    h = height / 100
    return weight / (h * h)

def bmi_category(bmi):
    if bmi < 18.5: return "Underweight"
    elif bmi < 25: return "Normal"
    elif bmi < 30: return "Overweight"
    else: return "Obese"

# ------------------ DIET ------------------
def get_diet(calories, pref):
    if calories < 1800:
        base = [
            "Breakfast: Oats + Fruits",
            "Lunch: Dal + 2 Chapati + Salad",
            "Dinner: Soup + Light Khichdi"
        ]
    elif calories < 2500:
        base = [
            "Breakfast: Sandwich + Milk",
            "Lunch: Dal + Rice + Sabzi",
            "Dinner: Chapati + Veg + Curd"
        ]
    else:
        base = [
            "Breakfast: Shake + Peanut Butter Toast",
            "Lunch: Rice + Protein + Salad",
            "Dinner: Chapati + Protein + Veg"
        ]

    if pref == "Non-Vegetarian":
        base = [meal.replace("Protein", "Chicken/Egg") for meal in base]

    return base

# ------------------ EXERCISE ------------------
def get_exercise(bmi):
    if bmi < 18.5:
        return ["Light Yoga (20 min)", "Stretching", "Walking (15-20 min)"]
    elif bmi < 25:
        return ["Jogging (20-30 min)", "Push-ups + Squats", "Cycling"]
    elif bmi < 30:
        return ["Brisk Walking (30 min)", "Skipping", "Light Strength Training"]
    else:
        return ["Walking (45 min)", "Low-impact Cardio", "Basic Yoga"]

# ------------------ RESULT SCREEN ------------------
def show_result(data):
    result = tk.Tk()
    result.title("Health Dashboard")
    result.attributes("-fullscreen", True)
    result.configure(bg="#121212")

    result.bind("<Escape>", lambda e: result.attributes("-fullscreen", False))

    tk.Label(result, text="YOUR HEALTH REPORT",
             font=("Segoe UI", 38, "bold"),
             bg="#121212", fg="#00e676").pack(pady=30)

    tk.Label(result,
             text=f"BMR: {data['bmr']:.2f} | Calories: {data['cal']:.2f} kcal | BMI: {data['bmi']:.2f} ({data['cat']})",
             font=("Segoe UI", 20),
             bg="#121212", fg="white").pack(pady=20)

    frame = tk.Frame(result, bg="#121212")
    frame.pack(expand=True)

    diet_frame = tk.Frame(frame, bg="#1f1f2e")
    diet_frame.grid(row=0, column=0, padx=40, pady=20)

    tk.Label(diet_frame, text="🥗 DIET PLAN",
             font=("Segoe UI", 28, "bold"),
             bg="#1f1f2e", fg="#00e676").pack(pady=20)

    for d in data["diet"]:
        tk.Label(diet_frame, text=d,
                 font=("Segoe UI", 18),
                 bg="#1f1f2e", fg="white").pack(anchor="w", padx=20, pady=8)

    ex_frame = tk.Frame(frame, bg="#1f1f2e")
    ex_frame.grid(row=0, column=1, padx=40, pady=20)

    tk.Label(ex_frame, text="🏃 EXERCISE PLAN",
             font=("Segoe UI", 28, "bold"),
             bg="#1f1f2e", fg="#ffcc00").pack(pady=20)

    for ex in data["exercise"]:
        tk.Label(ex_frame, text=ex,
                 font=("Segoe UI", 18),
                 bg="#1f1f2e", fg="white").pack(anchor="w", padx=20, pady=8)

    tk.Button(result, text="⬅ BACK",
              command=result.destroy,
              font=("Segoe UI", 20, "bold"),
              bg="#ff5252", fg="white").pack(pady=20)

    result.mainloop()

# ------------------ MAIN APP ------------------
def open_main():
    welcome.destroy()

    root = tk.Tk()
    root.title("Diet App")
    root.attributes("-fullscreen", True)
    root.configure(bg="#1e1e2f")

    root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))

    tk.Label(root, text="DIET & FITNESS APP",
             font=("Segoe UI", 36, "bold"),
             bg="#1e1e2f", fg="#00e676").pack(pady=30)

    card = tk.Frame(root, bg="#2c2c3e")
    card.pack(pady=20, ipadx=40, ipady=40)

    def lbl(t, r):
        tk.Label(card, text=t,
                 font=("Segoe UI", 20, "bold"),
                 bg="#2c2c3e", fg="white").grid(row=r, column=0, pady=10)

    def ent(r):
        e = tk.Entry(card, font=("Segoe UI", 20))
        e.grid(row=r, column=1, pady=10)
        return e

    lbl("Age:", 0); age = ent(0)
    lbl("Height:", 1); height = ent(1)
    lbl("Weight:", 2); weight = ent(2)
    lbl("Gender (M/F):", 3); gender = ent(3)

    activity = tk.StringVar(value="Sedentary")
    tk.OptionMenu(card, activity, "Sedentary", "Light", "Moderate", "Active").grid(row=4, column=1)

    pref = tk.StringVar(value="Vegetarian")
    tk.OptionMenu(card, pref, "Vegetarian", "Non-Vegetarian").grid(row=5, column=1)

    def calculate():
        try:
            a = int(age.get())
            h = float(height.get())
            w = float(weight.get())
            g = normalize_input(gender.get())

            if g == "Invalid":
                messagebox.showerror("Error", "Enter valid gender (M/F only)")
                return

            bmr = calculate_bmr(a, h, w, g)
            cal = calorie_needs(bmr, activity.get())
            bmi = calculate_bmi(w, h)
            cat = bmi_category(bmi)

            data = {
                "bmr": bmr,
                "cal": cal,
                "bmi": bmi,
                "cat": cat,
                "diet": get_diet(cal, pref.get()),
                "exercise": get_exercise(bmi)
            }

            show_result(data)

        except:
            messagebox.showerror("Error", "Invalid input!")

    tk.Button(root, text="CALCULATE",
              command=calculate,
              font=("Segoe UI", 24, "bold"),
              bg="#00c853", fg="white").pack(pady=30)

    root.mainloop()

# ------------------ WELCOME ------------------
welcome = tk.Tk()
welcome.attributes("-fullscreen", True)
welcome.configure(bg="black")

# ✅ Background image FIX20
try:
    bg = tk.PhotoImage(file="welcome_bg.png")
    bg_label = tk.Label(welcome, image=bg)
    bg_label.place(relwidth=1, relheight=1)
except:
    pass

tk.Button(welcome, text="START APP",
          command=open_main,
          font=("Segoe UI", 36, "bold"),
          bg="#00c853", fg="white",
          padx=40, pady=20).pack(expand=True)

welcome.mainloop()