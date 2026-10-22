from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "school_meal_secret_2026"

# Database Setup
def init_db():

    conn = sqlite3.connect("meal.db")
    cur = conn.cursor()

    

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT UNIQUE,
        name TEXT,
        class TEXT,
        phone TEXT,
        phone_type TEXT,
        gender TEXT,
        password TEXT
    )
    """)
    try:
        cur.execute("""
        ALTER TABLE students
        ADD COLUMN password TEXT
        """)
    except:
       pass

    cur.execute("""
    CREATE TABLE IF NOT EXISTS attendance(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT,
        type TEXT,
        date TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS feedback(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        rating TEXT,
        message TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS sms_logs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        phone TEXT,
        student_id TEXT,
        message TEXT,
        response TEXT,
        date TEXT
    )
    """) 
    cur.execute("""
    UPDATE students
    SET password = student_id
    WHERE password IS NULL
   """)

    conn.commit()
    conn.close()


init_db()


@app.route("/")
def home():
    return redirect("/student_login")


@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        fullname = request.form["fullname"]
        phone = request.form["phone"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        # Password check
        if password != confirm_password:
            return render_template(
                "signup.html",
                message="❌ Password and Confirm Password not matching"
            )

        # Student role automatically
        role = "student"

        hashed_password = generate_password_hash(password)

        conn = sqlite3.connect("meal.db")
        cur = conn.cursor()

        try:

            cur.execute("""
                INSERT INTO users(fullname, phone, email, password, role)
                VALUES(?,?,?,?,?)
            """,
            (
                fullname,
                phone,
                email,
                hashed_password,
                role
            ))

            conn.commit()
            conn.close()

            return render_template(
                "signup.html",
                message="✅ Student Registration Successful"
            )

        except sqlite3.IntegrityError:

            conn.close()

            return render_template(
                "signup.html",
                message="❌ Email Already Registered"
            )

    return render_template("signup.html")


@app.route("/admin_signup", methods=["GET", "POST"])
def admin_signup():

    if request.method == "POST":

        fullname = request.form["fullname"]
        phone = request.form["phone"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        admin_code = request.form["admin_code"]

        # Password check
        if password != confirm_password:

            return render_template(
                "admin_signup.html",
                message="❌ Password and Confirm Password not matching"
            )

        # Admin Secret Code
        if admin_code != "SCHOOL2026":

            return render_template(
                "admin_signup.html",
                message="❌ Invalid Admin Secret Code"
            )

        hashed_password = generate_password_hash(password)

        conn = sqlite3.connect("meal.db")
        cur = conn.cursor()

        try:

            cur.execute("""
                INSERT INTO users
                (fullname, phone, email, password, role)
                VALUES (?, ?, ?, ?, ?)
            """,
            (
                fullname,
                phone,
                email,
                hashed_password,
                "admin"
            ))

            conn.commit()
            conn.close()

            return render_template(
                "admin_signup.html",
                message="✅ Admin Registration Successful"
            )

        except sqlite3.IntegrityError:

            conn.close()

            return render_template(
                "admin_signup.html",
                message="❌ Email Already Registered"
            )

    return render_template("admin_signup.html")



@app.route("/forgot_password", methods=["GET","POST"])
def forgot_password():

    if request.method == "POST":

        email = request.form["email"]

        conn = sqlite3.connect("meal.db")
        cur = conn.cursor()

        cur.execute("""
        SELECT * FROM users
        WHERE email=?
        """,(email,))

        user = cur.fetchone()

        conn.close()

        if user:
            return render_template(
                "reset_password.html",
                email=email
            )

        else:
            return "❌ Email Not Registered"


    return render_template("forgot_password.html")
    
@app.route("/reset_password", methods=["POST"])
def reset_password():

    email = request.args.get("email")

    new_password = request.form["new_password"]
    confirm_password = request.form["confirm_password"]

    if new_password != confirm_password:
        return "❌ Password Not Matching"


    hashed_password = generate_password_hash(new_password)


    conn = sqlite3.connect("meal.db")
    cur = conn.cursor()

    cur.execute("""
    UPDATE users
    SET password=?
    WHERE email=?
    """,(hashed_password,email))


    conn.commit()
    conn.close()


    return "✅ Password Updated Successfully"


# Breakfast Attendance
@app.route("/breakfast", methods=["GET", "POST"])
def breakfast():

    if "student_id" not in session:
        return redirect("/student_login")

    student_id = session["student_id"]

    if request.method == "POST":

        today = str(date.today())

        conn = sqlite3.connect("meal.db")
        cur = conn.cursor()

        cur.execute("""
        SELECT * FROM attendance
        WHERE student_id=? AND type=? AND date=?
        """, (student_id, "Breakfast", today))

        existing = cur.fetchone()

        if existing:
            conn.close()

            return render_template(
                "error.html",
                title="Already Marked!",
                message="Breakfast attendance already marked for today 🍳",
                icon="⚠️"
            )

        cur.execute("""
        INSERT INTO attendance(student_id,type,date)
        VALUES(?,?,?)
        """, (student_id, "Breakfast", today))

        conn.commit()
        conn.close()

        return render_template(
            "success.html",
            title="Breakfast Attendance",
            message="Breakfast Marked Successfully 🍳",
            icon="✅"
        )

    return render_template(
        "breakfast.html",
        student_id=student_id
    )
# Lunch Attendance
@app.route("/lunch", methods=["GET", "POST"])
def lunch():

    if "student_id" not in session:
        return redirect("/student_login")

    student_id = session["student_id"]

    if request.method == "POST":

        today = str(date.today())

        conn = sqlite3.connect("meal.db")
        cur = conn.cursor()

        cur.execute("""
        SELECT * FROM attendance
        WHERE student_id=? AND type=? AND date=?
        """, (student_id, "Lunch", today))

        existing = cur.fetchone()

        if existing:
            conn.close()

            return render_template(
                "error.html",
                title="Already Marked!",
                message="Lunch attendance already marked for today 🍛",
                icon="⚠️"
            )

        cur.execute("""
        INSERT INTO attendance(student_id,type,date)
        VALUES(?,?,?)
        """, (student_id, "Lunch", today))

        conn.commit()
        conn.close()

        return render_template(
            "success.html",
            title="Lunch Attendance",
            message="Lunch Marked Successfully 🍛",
            icon="✅"
        )

    return render_template(
        "lunch.html",
        student_id=student_id
    )


# Feedback
@app.route("/feedback", methods=["GET","POST"])
def feedback():

    if request.method == "POST":

        name = request.form["name"]
        rating = request.form["rating"]
        message = request.form["message"]
           
        if not name or not rating or not message:
            return "Please fill all fields"   

        conn = sqlite3.connect("meal.db")
        cur = conn.cursor()


        cur.execute("""
        INSERT INTO feedback(name,rating,message)
        VALUES(?,?,?)
        """, (name,rating,message))


        conn.commit()
        conn.close()

        return render_template(
             "success.html",
             title="Feedback Submitted",
             message="Your feedback saved successfully ⭐",
             icon="⭐"
        )


    return render_template("feedback.html")
# Add Students
@app.route("/add_students", methods=["GET","POST"])
def add_students():

    if request.method == "POST":

        student_id = request.form["student_id"]
        name = request.form["name"]
        class_name = request.form["class"]
        phone = request.form["phone"]
        gender = request.form["gender"]
        phone_type = request.form["phone_type"]

        conn = sqlite3.connect("meal.db")
        cur = conn.cursor()

        cur.execute(
            "SELECT student_id FROM students WHERE student_id=?",
            (student_id,)
        )

        check = cur.fetchone()

        if check:
            conn.close()
            return render_template(
                "add_students.html",
                message="Student ID Already Exists"
            )

        conn.execute("""
        INSERT INTO students(student_id,name,class,phone,gender,phone_type)
        VALUES(?,?,?,?,?,?)
        """, (student_id,name,class_name,phone,gender,phone_type))

        conn.commit()
        conn.close()

        return render_template("add_students.html",
                               message="Student Added Successfully")


    return render_template("add_students.html")
# Student Login
@app.route("/student_login", methods=["GET", "POST"])

def student_login():

    if request.method == "POST":

        student_id = request.form["student_id"].strip()
        password = request.form["password"]

        conn = sqlite3.connect("meal.db")
        cur = conn.cursor()

        # Find student using Student ID
        cur.execute("""
            SELECT student_id, name, password
            FROM students
            WHERE student_id=?
        """, (student_id,))

        student = cur.fetchone()

        conn.close()

        # Student ID not found
        if not student:
            return render_template(
                "error.html",
                title="Login Failed",
                message="Invalid Student ID or Password",
                icon="❌",
                back_url="/student_login"
            )

        db_student_id = student[0]
        student_name = student[1]
        stored_password = student[2]

        
        # Check password
        password_valid = False

        try:
            password_valid = check_password_hash(stored_password, password)
        except:
            password_valid = False

        # If old password is plain text (example: S004)
        if not password_valid and stored_password == password:

            # Convert old plain password into hashed password
            new_hashed_password = generate_password_hash(password)

            conn = sqlite3.connect("meal.db")
            cur = conn.cursor()

            cur.execute("""
                UPDATE students
                SET password=?
                WHERE student_id=?
            """, (new_hashed_password, db_student_id))

            conn.commit()
            conn.close()

            password_valid = True


        if password_valid:

            # Save actual Student ID
            session["student_id"] = db_student_id
            session["student_name"] = student_name

            return redirect("/student_dashboard")

        # Wrong password
        return render_template(
            "error.html",
            title="Login Failed",
            message="Invalid Student ID or Password",
            icon="❌",
            back_url="/student_login"
        )

    return render_template("student_login.html")

@app.route("/student_dashboard")
def student_dashboard():

    if "student_name" not in session:
        return redirect("/student_login")

    return render_template(
        "student_dashboard.html",
        name=session["student_name"],
        student_id=session["student_id"],
        class_name="Student"
    )
@app.route("/admin_login", methods=["GET","POST"])
def admin_login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("meal.db")
        cur = conn.cursor()

        cur.execute("""
            SELECT password, role 
            FROM users 
            WHERE email=?
        """, (username,))

        user = cur.fetchone()

        conn.close()

        if user:

            stored_password = user[0]
            role = user[1]

            if role == "admin" and check_password_hash(stored_password, password):
                return render_template("admin_dashboard.html")

        return render_template(
            "error.html",
            title="Login Failed",
            message="Invalid Username or Password",
            icon="❌"
        )

    return render_template("admin_login.html")
# Dashboard
@app.route("/dashboard")
def dashboard():

    conn = sqlite3.connect("meal.db")
    cur = conn.cursor()


    today = str(date.today())
    display_date = date.today().strftime("%d-%m-%Y")


    cur.execute("""
    SELECT COUNT(*) FROM attendance
    WHERE type=? AND date=?
    """, ("Breakfast",today))

    breakfast = cur.fetchone()[0]


    cur.execute("""
    SELECT COUNT(*) FROM attendance
    WHERE type=? AND date=?
    """, ("Lunch",today))

    lunch = cur.fetchone()[0]

    total_meals = breakfast + lunch
    # Student Details Count

    cur.execute("SELECT COUNT(*) FROM students")
    total_students = cur.fetchone()[0]


    cur.execute("""
    SELECT COUNT(*) FROM students
    WHERE gender='Boy'
    """)
    boys = cur.fetchone()[0]


    cur.execute("""
    SELECT COUNT(*) FROM students
    WHERE gender='Girl'
    """)
    girls = cur.fetchone()[0]


    cur.execute("""
    SELECT COUNT(*) FROM students
    WHERE phone_type='Smartphone'
    """)
    smartphone = cur.fetchone()[0]


    cur.execute("""
    SELECT COUNT(*) FROM students
    WHERE phone_type='Button Phone'
    """)
    button_phone = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM students")
    total_students = cur.fetchone()[0]

    cur.execute("""
    SELECT COUNT(*) FROM students
    WHERE phone_type='Smartphone'
    """)
    smartphone_count = cur.fetchone()[0]

    cur.execute("""
    SELECT COUNT(*) FROM students
    WHERE phone_type='Button Phone'
    """)
    button_phone_count = cur.fetchone()[0]


    cur.execute("""
    SELECT name,rating,message 
    FROM feedback
    ORDER BY id DESC
    LIMIT 10
    """)

    feedbacks = cur.fetchall()


    ratings=[]

    for f in feedbacks:
        try:
            ratings.append(int(f[1]))
        except:
            pass


    if len(ratings)>0:

        avg=sum(ratings)/len(ratings)

        if avg>=4:
            analysis="😊 Students Satisfied"
        else:
            analysis="⚠️ Improve Food Quality"

    else:
        analysis="No Feedback Yet"



    conn.close()

    return render_template(
        "dashboard.html",
        breakfast=breakfast,
        lunch=lunch,
        total_meals=total_meals,
        today=display_date,
        feedbacks=feedbacks,
        analysis=analysis,
        total_students=total_students,
        boys=boys,
        girls=girls,
        smartphone=smartphone,
        button_phone=button_phone
    )

# Menu
@app.route("/menu")
def menu():

    return render_template("menu.html")

# Report
@app.route("/report")
def report():

    conn = sqlite3.connect("meal.db")
    cur = conn.cursor()


    today = str(date.today())
    report_date = date.today().strftime("%d-%m-%Y")

    cur.execute("""
    SELECT COUNT(*) FROM attendance
    WHERE type=? AND date=?
    """, ("Breakfast",today))

    breakfast = cur.fetchone()[0]

    cur.execute("""
    SELECT COUNT(*) FROM attendance
    WHERE type=? AND date=?
    """, ("Lunch",today))

    lunch = cur.fetchone()[0]
    today_day = date.today().strftime("%A")
    week_no = date.today().isocalendar().week


    if today_day == "Monday":
       breakfast_menu = "அரிசி பொங்கல் + காய்கறி சாம்பார்"
       lunch_menu = "சாதம் + சாம்பார் + மிளகு முட்டை"

    elif today_day == "Tuesday":
        breakfast_menu = "ரவா உப்புமா + காய்கறி சாம்பார்"
        lunch_menu = "சாதம் + கருப்பு கொண்டைக்கடலை குழம்பு + தக்காளி முட்டை"

    elif today_day == "Wednesday":
        breakfast_menu = "வெண்பொங்கல் + காய்கறி சாம்பார்"
        lunch_menu = "தக்காளி சாதம் + மிளகு முட்டை"

    elif today_day == "Thursday":
        breakfast_menu = "சேமியா காய்கறி கிச்சடி + காய்கறி சாம்பார்"

        if week_no % 2 == 0:
          lunch_menu = "எலுமிச்சை சாதம் + பாசிப்பயறு + சுண்டல் + தக்காளி முட்டை"
        else:
             lunch_menu = "சாதம் + காய்கறி சாம்பார் + வேகவைத்த முட்டை"

    elif today_day == "Friday":
        breakfast_menu = "கோதுமை ரவா காய்கறி கிச்சடி + காய்கறி சாம்பார்"

        if week_no % 2 == 0:
          lunch_menu = "சாதம் + காய்கறி சாம்பார் + வேகவைத்த முட்டை + வறுத்த உருளைக்கிழங்கு"
        else:
            lunch_menu = "சாதம் + பருப்பு + கீரை கூட்டு + மசாலா முட்டை + மிளகாய் பொடி தூவி வறுத்த உருளைக்கிழங்கு"
    elif today_day == "Saturday":
        breakfast_menu = "வெண்பொங்கல் + காய்கறி சாம்பார்"
        lunch_menu = "பருப்பு சாதம்"

    else:
         breakfast_menu = "Holiday"
         lunch_menu = "Holiday"


    analysis="😊 Students Satisfied"
    conn.close()
    return render_template(
        "report.html",
        breakfast=breakfast,
        lunch=lunch,
        breakfast_menu=breakfast_menu,
        lunch_menu=lunch_menu,
        analysis=analysis,
        report_date=report_date
    )

# Button Phone Simple YES / NO SMS Attendance

@app.route("/sms_attendance", methods=["GET","POST"])
def sms_attendance():

    if request.method == "POST":

        phone = request.form["phone"]

        action = request.form["action"].upper()

        parts = action.split()

        meal_type = parts[0].capitalize()
        response = parts[1]

        message = action


        

        conn = sqlite3.connect("meal.db")
        cur = conn.cursor()


        cur.execute("""
        SELECT student_id,name
        FROM students
        WHERE phone=?
        """,(phone,))


        student = cur.fetchone()


        if student is None:
            conn.close()
            return render_template(
                "sms_attendance.html",
                message="❌ Phone Number Not Registered"
            )


        student_id = student[0]
        name = student[1]


        if response == "YES":

            today = str(date.today())


            cur.execute("""
            SELECT * FROM attendance
            WHERE student_id=? AND type=? AND date=?
            """,
            (student_id, meal_type, today))


            already = cur.fetchone()
            if already:
                conn.close()
                return render_template(
                    "sms_attendance.html",
                    message=f"⚠️ {name} Attendance Already Marked Today"
                )

            cur.execute("""
            SELECT * FROM attendance
            WHERE student_id=? AND type=? AND date=?
            """,
            (student_id, meal_type, today))

            already = cur.fetchone()

            if already:
                conn.close()
                return render_template(
                    "sms_attendance.html",
                     message=f"⚠️ {name} {meal_type} Already Marked Today"
                )

            cur.execute("""
            INSERT INTO attendance(student_id,type,date)
            VALUES(?,?,?)
            """,
            (student_id,meal_type,today))

            cur.execute("""
            INSERT INTO sms_logs(phone,student_id,message,response,date)
            VALUES(?,?,?,?,?)
            """,
            (phone,student_id,message,response,today))


            conn.commit()
            conn.close()

            return render_template(
                 "sms_attendance.html",
                 message=f"✅ {name} Attendance Marked"
            )


        elif response == "NO":
            
            today = str(date.today())

            cur.execute("""
            INSERT INTO sms_logs(phone,student_id,message,response,date)
            VALUES(?,?,?,?,?)
            """,
            (phone,student_id,message,"NO",today))
            conn.close()
            return render_template(
                "sms_attendance.html",
                message=f"❌ {name} Not Attending"
            )


        else:

            conn.close()
            return render_template(
                "sms_attendance.html",
                message="⚠️ Reply only YES or NO"
            )


    return render_template("sms_attendance.html")

# SMS History

@app.route("/sms_history")
def sms_history():

    conn = sqlite3.connect("meal.db")
    cur = conn.cursor()

    cur.execute("""
    SELECT * FROM sms_logs
    """)

    logs = cur.fetchall()

    conn.close()

    return render_template(
        "sms_history.html",
        logs=logs
    )
@app.route("/delete_sms/<int:id>")
def delete_sms(id):

    conn = sqlite3.connect("meal.db")
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM sms_logs WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/sms_history")

# View Students
@app.route("/view_students")
def view_students():

    conn = sqlite3.connect("meal.db")
    cur = conn.cursor()


    cur.execute("SELECT * FROM students")

    students = cur.fetchall()


    conn.close()


    return render_template(
        "view_students.html",
        students=students
    )

@app.route("/delete_student/<student_id>")
def delete_student(student_id):

    conn = sqlite3.connect("meal.db")
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM students WHERE student_id=?",
        (student_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/view_students")
@app.route("/edit_student/<student_id>", methods=["GET", "POST"])
def edit_student(student_id):

    conn = sqlite3.connect("meal.db")
    cur = conn.cursor()

    if request.method == "POST":

        name = request.form["name"]
        class_name = request.form["class"]
        phone = request.form["phone"]
        phone_type = request.form["phone_type"]
        gender = request.form["gender"]

        cur.execute("""
        UPDATE students
        SET name=?, class=?, phone=?, phone_type=?, gender=?
        WHERE student_id=?
        """, (name, class_name, phone, phone_type, gender, student_id))

        conn.commit()
        conn.close()

        return redirect("/view_students")

    cur.execute("""
    SELECT * FROM students
    WHERE student_id=?
    """, (student_id,))

    student = cur.fetchone()

    conn.close()

    return render_template("edit_student.html", student=student)
@app.route("/check_users")
def check_users():

    conn = sqlite3.connect("meal.db")
    cur = conn.cursor()

    cur.execute("SELECT id, fullname, email FROM users")
    users = cur.fetchall()

    conn.close()

    return str(users)     
@app.route("/check_students")
def check_students():

    conn = sqlite3.connect("meal.db")
    cur = conn.cursor()

    cur.execute("PRAGMA table_info(students)")
    columns = cur.fetchall()

    conn.close()

    return str(columns)

@app.route("/students_data")
def students_data():

    conn = sqlite3.connect("meal.db")
    cur = conn.cursor()

    cur.execute("SELECT student_id, name, password FROM students")
    data = cur.fetchall()

    conn.close()

    return str(data)

@app.route("/internet_error")
def internet_error():

    return render_template("internet_error.html")

@app.route("/student_logout")
def student_logout():

    session.clear()

    return redirect("/student_login")


@app.route("/admin_logout")
def admin_logout():

    session.clear()

    return redirect("/admin_login")

if __name__ == "__main__":
    app.run(debug=True)