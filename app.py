from flask import Flask, render_template, request, session, flash, url_for, redirect , jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, PasswordField, RadioField , SelectField
from wtforms.validators import DataRequired, Length , Regexp , Optional , Email
from datetime import datetime, date, timedelta
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os
from mysql.connector import IntegrityError

from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


from flask_mail import Mail, Message

app.config['MAIL_SERVER'] = ' smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'abhinavsinghjohar1112@gmail.com'
app.config['MAIL_PASSWORD'] =  os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = 'abhinavsinghjohar1112@gmail.com'

mail = Mail(app)
 


 

class signupform(FlaskForm):
    position = RadioField('Position', choices=[
        ('employee', 'employee'),
        ('manager', 'manager'),
        ('hr', 'hr'),
        ('supermanager','supermanager')
    ], validators=[DataRequired()])
    
    name = StringField('Name',render_kw={"placeholder": "Enter your full name"}, validators=[DataRequired()])
    employeeid = StringField('Employee ID', render_kw={"placeholder": "Enter your employeeid"},validators=[DataRequired()])
    emailid = StringField('Email',render_kw={"placeholder": "Enter your emailid"}, validators=[DataRequired()  , Email(message="Invalid email address")])
    password = PasswordField('Password',render_kw={"placeholder": "generate password"}, validators=[DataRequired()])
    confirmpassword = PasswordField('confirm Password',render_kw={"placeholder": "confirm password"}, validators=[DataRequired()])
    country_code = SelectField(
        "Country Code",
        choices=[
            ("+91", "🇮🇳 +91 (India)"),
            ("+1", "🇺🇸 +1 (USA)"),
            ("+44", "🇬🇧 +44 (UK)"),
            ("+61", "🇦🇺 +61 (Australia)")
        ],
        validators=[DataRequired()]

    )

    phone = StringField(
        "Phone Number",render_kw={"placeholder": "Enter mobile number"},
        validators=[
            DataRequired(),
            Regexp(r'^[0-9]+$', message="Only digits allowed"),
            Length(min=9, max=13, message="Invalid phone length")
        ]
    )


    
    department = SelectField(
        "Department",
        choices=[
            ("dev", "Software Development"),
            ("qa", "Quality Assurance (QA)"),
            ("devops", "DevOps"),
            ("data", "Data Science / AI"),
            ("product", "Product Management"),
            ("design", "UI/UX Design"),
            ("hr", "Human Resources (HR)"),
            ("sales", "Sales & Marketing"),
            ("support", "Customer Support"),
            ("it", "IT Support")
        ],
        validators=[DataRequired()]
    )
    submit = SubmitField('Signup')




class add_employee_form(FlaskForm):
    position = RadioField('Position', choices=[
        ('employee', 'employee'),
        ('manager', 'manager')
         
        
    ], validators=[DataRequired()])
    
    name = StringField('Name',render_kw={"placeholder": "Enter your full name"}, validators=[DataRequired()])
    employeeid = StringField('Employee ID', render_kw={"placeholder": "Enter your employeeid"},validators=[DataRequired()])
    emailid = StringField('Email',render_kw={"placeholder": "Enter your emailid"}, validators=[DataRequired()  , Email(message="Invalid email address")])
    password = PasswordField('Password',render_kw={"placeholder": "generate password"}, validators=[DataRequired()])
    confirmpassword = PasswordField('confirm Password',render_kw={"placeholder": "confirm password"}, validators=[DataRequired()])
    country_code = SelectField(
        "Country Code",
        choices=[
            ("+91", "🇮🇳 +91 (India)"),
            ("+1", "🇺🇸 +1 (USA)"),
            ("+44", "🇬🇧 +44 (UK)"),
            ("+61", "🇦🇺 +61 (Australia)")
        ],
        validators=[DataRequired()]

    )

    phone = StringField(
        "Phone Number",render_kw={"placeholder": "Enter mobile number"},
        validators=[
            DataRequired(),
            Regexp(r'^[0-9]+$', message="Only digits allowed"),
            Length(min=9, max=13, message="Invalid phone length")
        ]
    )


    
    department = SelectField(
        "Department",
        choices=[
            ("dev", "Software Development"),
            ("qa", "Quality Assurance (QA)"),
            ("devops", "DevOps"),
            ("data", "Data Science / AI"),
            ("product", "Product Management"),
            ("design", "UI/UX Design"),
            ("hr", "Human Resources (HR)"),
            ("sales", "Sales & Marketing"),
            ("support", "Customer Support"),
            ("it", "IT Support")
        ],
        validators=[DataRequired()]
    )
    submit = SubmitField('add employee')    


class loginform(FlaskForm):
    login = StringField('Employee ID or Email', validators=[DataRequired()])
    position = RadioField('Position', choices=[
        ('employee', 'employee'),
        ('manager', 'manager'),
        ('hr', 'hr'),
        ('supermanager','supermanager')
    ], validators=[DataRequired()])
    

    
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')




class change_employee_info(FlaskForm):
    emailid = StringField('Employee ID or Email', validators=[DataRequired()])
    country_code = SelectField(
             "Country Code",
             choices=[
                 ("+91", "🇮🇳 +91 (India)"),
                 ("+1", "🇺🇸 +1 (USA)"),
                 ("+44", "🇬🇧 +44 (UK)"),
                 ("+61", "🇦🇺 +61 (Australia)")
             ],
             validators=[DataRequired()]
     
         )
     
    phone = StringField(
             "Phone Number",render_kw={"placeholder": "Enter mobile number"},
             validators=[
                 DataRequired(),
                 Regexp(r'^[0-9]+$', message="Only digits allowed"),
                 Length(min=9, max=13, message="Invalid phone length")
             ]
         )
   

    
     
    submit = SubmitField('save')


class applyleaveform(FlaskForm):
     
 


    leave_type = RadioField('Leave Type', choices=[
        ('casual leave', 'casual leave'),
        ('sick leave', 'sick leave'),
        ('earned leave', 'earned leave'),
         
    ], validators=[DataRequired()])

   
  



    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    halfofstart=SelectField('Session',choices=[('session 1','session 1'),('session 2','session 2')])
    halfofend=SelectField('Session',choices=[('session 1','session 1'),('session 2','session 2')])
    
 
     
    submit = SubmitField('Apply')



def send_email(to, subject, body):
    try:
        msg = Message(subject, recipients=[to])
        msg.body = body
        mail.send(msg)
    except Exception as e:
        print("Email error:", e)    


 
def connect_to_db():
    try:
        return mysql.connector.connect(
            host=os.environ.get("DB_HOST", "localhost"),
            user=os.environ.get("DB_USER", "root"),
            password=os.environ.get("DB_PASSWORD"),
            database=os.environ.get("DB_NAME", "leaveapp")
        )
    except mysql.connector.Error as e:
        app.logger.error(f"DB connection failed: {e}")
        return None

#functions required...

def get_holidays(cursor):
    cursor.execute("SELECT holiday_date FROM holidays")
    return {row[0] for row in cursor.fetchall()}

def get_approved_leaves_for_year(employee_id,leave_type,cursor):
    today = date.today()
     
    year = today.year
    
    start_of_year = date(year, 1,1)       
    end_of_year = date(year,  12 ,31) 
    query = """
SELECT start_date, end_date, halfofstart, halfofend
FROM leaves
WHERE employeeid=%s
AND leave_type=%s
AND status='approved'
AND (start_date <= %s AND end_date >= %s)
"""

    cursor.execute(query, (employee_id, leave_type, end_of_year, start_of_year))
    
    
    return cursor.fetchall()

def get_approved_leaves_for_month(employee_id, leave_type, cursor):
    today = date.today()
    month = today.month
    year = today.year

    start_of_month = date(year, month, 1)
    end_of_month = date(year, month + 1, 1) if month < 12 else date(year + 1, 1, 1)
    query = """
SELECT start_date, end_date, halfofstart, halfofend
FROM leaves
WHERE employeeid=%s
AND leave_type=%s
AND status='approved'
AND (start_date <= %s AND end_date >= %s)
"""

    cursor.execute(query, (employee_id, leave_type, end_of_month, start_of_month))
    return cursor.fetchall()


 

def count_leave_days(leaves, holidays, exclude_weekends, exclude_holidays):
    total = 0

    for start, end, halfofstart, halfofend in leaves:
        current = start

        while current <= end:
            # skip excluded days entirely (no partial credit)
            if exclude_weekends and current.weekday() >= 5:
                current += timedelta(days=1)
                continue

            if exclude_holidays and current in holidays:
                current += timedelta(days=1)
                continue

            is_first_day = (current == start)
            is_last_day = (current == end)

            if is_first_day and is_last_day:
                # single-day leave: full day only if it spans session 1 -> session 2
                if halfofstart == 'session 1' and halfofend == 'session 2':
                    day_value = 1.0
                else:
                    day_value = 0.5   # session1-only (morning) or session2-only (afternoon)

            elif is_first_day:
                # starting on session 2 means the morning of day 1 wasn't taken
                day_value = 0.5 if halfofstart == 'session 2' else 1.0

            elif is_last_day:
                # ending on session 1 means the afternoon of the last day wasn't taken
                day_value = 0.5 if halfofend == 'session 1' else 1.0

            else:
                day_value = 1.0  # middle days are always full days

            total += day_value
            current += timedelta(days=1)

    return total


def check_department_limit(employeeid, start_date, end_date):
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute("SELECT department FROM signupdata WHERE employeeid=%s", (employeeid,))
    row = cursor.fetchone()

    if not row:
        cursor.close()
        conn.close()
        return False
    dept = row[0]

    cursor.execute("SELECT COUNT(*) FROM signupdata WHERE department=%s", (dept,))
    total = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(DISTINCT employeeid)
    FROM leaves
    WHERE department=%s
    AND status='approved'
    AND (start_date <= %s AND end_date >= %s)
    """, (dept, end_date, start_date))
    on_leave = cursor.fetchone()[0]

    cursor.execute("SELECT max_department_leave_percent FROM system_rules LIMIT 1")
    percent = cursor.fetchone()[0] or 30
    cursor.close()
    conn.close()

    if total == 0:
        return False
    return (on_leave / total) < (percent / 100)




def hr_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('position') != 'hr':    
            return "Access Denied"
        return func(*args, **kwargs)
    return wrapper


@app.after_request
def add_no_cache_headers(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


#all routes




@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully")
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = signupform()

    if form.validate_on_submit():
        if form.password.data!=form.confirmpassword.data:
            form.confirmpassword.errors.append("password doesnt match")
            return render_template("signup.html",form=form)
        
        phone_no=f"{form.country_code.data}{form.phone.data}"
        conn = connect_to_db()
        cursor = conn.cursor(dictionary=True)

        hashed = generate_password_hash(form.password.data)
        

 
       
        cursor.execute("SELECT employeeid FROM signupdata WHERE employeeid=%s",
                     (form.employeeid.data,))
        emp = cursor.fetchone()

    
        cursor.execute("SELECT emailid FROM signupdata WHERE emailid=%s",
                     (form.emailid.data,))
        email = cursor.fetchone()

 
        if emp or email:
            if emp:
             form.employeeid.errors.append("Employee ID already exists ❌")
            if email:
             form.emailid.errors.append("Email already exists ❌")

            return render_template('signup.html', form=form)



        
        cursor.execute("""
        INSERT INTO signupdata (position, employeeid, emailid, password,phone , name, department)
        VALUES (%s, %s, %s, %s, %s,%s,%s)
        """, (
            form.position.data,
            form.employeeid.data,
            form.emailid.data,
            hashed,
            phone_no,
            form.name.data,
            form.department.data
        ))

        conn.commit()
        cursor.close()
        conn.close()
        flash ("siggned up successfully")
        return redirect(url_for('login'))
       


    return render_template('signup.html', form=form)

@app.route('/', methods=['GET', 'POST'])
def login():
    if 'employeeid' in session:
        pos = session.get('position')
        if pos == 'employee':
            return redirect(url_for('employee_dashboard'))
        elif pos == 'manager':
            return redirect(url_for('manager_dashboard'))
        elif pos == 'hr':
            return redirect(url_for('hr_dashboard'))
        elif pos == 'supermanager':
            return redirect(url_for('supermanager_dashboard'))
    

    form = loginform()

    if form.validate_on_submit():
        
        conn = connect_to_db()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
        SELECT * FROM signupdata
        WHERE emailid=%s OR employeeid=%s
        """, (form.login.data, form.login.data))

        user = cursor.fetchone()

        cursor.close()
        conn.close()
        if user:
           if not user.get('is_active', 1):
               form.login.errors.append("This account has been deactivated. Contact HR.")
           elif not check_password_hash(user['password'], form.password.data):
              form.password.errors.append("Invalid password")

           elif form.position.data != user['position']:
               form.position.errors.append("Wrong role selected")

           else:
              session['employeeid'] = user['employeeid']
              session['position'] = user['position']
              session['fresh_login'] = True
 
              if user['position'] == "employee":
                     flash ("logged in successfully")
                     return redirect(url_for('employee_dashboard'))
              elif user['position'] == "manager":
                     return redirect(url_for('manager_dashboard'))
              elif user['position'] == "hr":
                        return redirect(url_for('hr_dashboard'))
              elif user['position'] == "supermanager":
                        return redirect(url_for('supermanager_dashboard'))

        else:
           form.login.errors.append("Invalid email or employee ID")
            

         

    return render_template('login.html', form=form)




@app.context_processor
def inject_user():
    if 'employeeid' in session:
        conn = connect_to_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT name, employeeid, emailid, position FROM signupdata WHERE employeeid=%s",
            (session['employeeid'],)
        )
        u = cursor.fetchone()
        cursor.close()
        conn.close()
        return dict(user=u)
    return dict(user=None)





@app.route('/employee_dashboard')

def employee_dashboard():
    if 'employeeid' not in session:
        flash("please login first")
        return redirect(url_for('login'))

    fresh_login = session.pop('fresh_login', False) 

    employeeid = session['employeeid']

    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT name, employeeid, emailid, position
    FROM signupdata
    WHERE employeeid=%s
    """, (employeeid,))

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template('employee_home.html', user=user , fresh_login=fresh_login)


@app.route('/applyleave', methods=['GET', 'POST'])
def applyleave():
    print("METHOD:", request.method)
    if 'employeeid' not in session:
        flash("please login first")
        return redirect(url_for('login'))

    position=session['position']
    form = applyleaveform()
  

    if form.validate_on_submit():
        employeeid = session['employeeid']
        leave_type = form.leave_type.data.lower()
        start = form.start_date.data
        halfofstart=form.halfofstart.data
        end = form.end_date.data
        halfofend=form.halfofend.data

         
        status = "pending"
        

        conn = connect_to_db()
        
        dict_cursor = conn.cursor(dictionary=True)
        cursor = conn.cursor()   # plain tuple cursor for holidays/leaves helpers
        cursor.execute("SELECT  department FROM signupdata WHERE employeeid=%s" , (employeeid,))
        department = cursor.fetchone()

        

        department = department[0] 
        dict_cursor.execute(
            "SELECT * FROM leave_policy WHERE leave_type=%s",
            (leave_type,)
        )
        policy = dict_cursor.fetchone()

        

        if start > end:
            form.end_date.errors.append("end date is preceding start date")
            return render_template("applyleave.html", form=form)
             
             

        if not check_department_limit(employeeid, start, end):
            flash (" can not grant you leave more than 30 percent of the department on leave ")
            return render_template("applyleave.html",form=form)
             
       

        holidays = get_holidays(cursor)
        old_leaves = get_approved_leaves_for_month(employeeid, leave_type, cursor)
        old_leaves1=get_approved_leaves_for_year(employeeid,leave_type,cursor)

        used = count_leave_days(old_leaves, holidays, True, True)
        new = count_leave_days([(start, end, halfofstart,halfofend)], holidays, True, True)
        used1=count_leave_days(old_leaves1,holidays,True,True)
        if new == 0:
            flash("Selected dates fall entirely on weekends or holidays — no working days requested ❌")
            return render_template("applyleave.html", form=form)

        totaldays = used + new
        totaldaysforinput= new + used1

        if policy and policy['max_per_month']:
            if totaldays > policy['max_per_month']:
                flash("Monthly limit exceeded ❌")
                return render_template("applyleave.html",form=form)
        if policy and policy['total_leaves']:
            if totaldaysforinput > policy['total_leaves']:
                flash("Annual leave limit exceeded ❌")
                return render_template("applyleave.html", form=form)    

        if policy and policy['min_notice_days']:
            if (start - date.today()).days < policy['min_notice_days']:
                flash(f"Apply {policy['min_notice_days']} days before ❌")
                return render_template("applyleave.html",form=form)
                

        leave_id = f"{employeeid}_{datetime.now().timestamp()}"

        cursor.execute("""
            INSERT INTO leaves (employeeid, leave_type , start_date , end_date , halfofstart , halfofend , leave_id , status , totaldays)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s , %s)
        """, (employeeid, leave_type, start, end, halfofstart , halfofend ,  leave_id,  status , new))

        conn.commit()
        cursor.close()
        dict_cursor.close()
        conn.close()

        flash("Leave applied ✅")
        # get employee email
        conn = connect_to_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT emailid, name FROM signupdata WHERE employeeid=%s", (employeeid,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        # send email
        if user:
          send_email(
              user['emailid'],
              "Leave Application Submitted",
              f"Hello {user['name']},\n\nYour leave request from {start} to {end} has been submitted successfully.\n\nStatus: Pending\n\n- Leave Management System"
            )
        if position=="employee":
                 return redirect(url_for('employee_leaves'))
        if position=="manager":
                 return redirect(url_for('manager_leaves'))
        if position=="hr":
                 return redirect(url_for('hr_leaves'))

    return render_template('applyleave.html', form=form)




@app.route('/cancel_leave/<leave_id>')
def cancel_leave(leave_id):
    if 'employeeid' not in session:
        flash("Please login first")
        return redirect(url_for('login'))

    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM leaves
        WHERE id=%s AND employeeid=%s AND status='pending'
    """, (leave_id, session['employeeid']))

    conn.commit()
    cursor.close()
    conn.close()

    flash("Leave cancelled ✅")

    # Redirect according to position
    position = session.get('position')

    if position == 'employee':
        return redirect(url_for('employee_leaves'))

    elif position == 'manager':
        return redirect(url_for('manager_leaves'))

    elif position == 'hr':
        return redirect(url_for('hr_leaves'))

     


@app.route('/employee_leaves')
def employee_leaves():
    if 'employeeid' not in session:
        flash("please login first")
        return redirect(url_for('login'))
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT * FROM leaves
    WHERE employeeid=%s
    ORDER BY id DESC
    """, (session['employeeid'],))

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('employee_leaves.html', data=data ,role=session.get("position"))



@app.route('/hr_leaves')
def hr_leaves():
    if 'employeeid' not in session:
        flash("please login first")
        return redirect(url_for('login'))
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT * FROM leaves
    WHERE employeeid=%s
    ORDER BY id DESC
    """, (session['employeeid'],))

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('hr_leaves.html', data=data ,role=session.get("position"))



@app.route('/manager_leaves')
def manager_leaves():
    if 'employeeid' not in session:
        flash("please login first")
        return redirect(url_for('login'))
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT * FROM leaves
    WHERE employeeid=%s
    ORDER BY id DESC
    """, (session['employeeid'],))

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('manager_leaves.html', data=data ,role=session.get("position"))


 

@app.route('/manager_dashboard')
def manager_dashboard():
    if 'employeeid' not in session:
     return redirect(url_for('login')) 
    if session.get('position') != 'manager':
            return "Access Denied"
    
    fresh_login = session.pop('fresh_login', False)
    conn=connect_to_db()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("""
            SELECT * FROM signupdata
            WHERE  manager_id=%s
            """, (session['employeeid'],))
    
    user = cursor.fetchall()
    print(user)
    cursor.execute("""
        SELECT name FROM signupdata WHERE employeeid=%s 
        
        """ ,(session['employeeid'],))
    result1 = cursor.fetchone()
    name = result1['name']
    
   
 

    return render_template('manager_home.html',user=user, fresh_login=fresh_login, name=name)


@app.route('/update_leave_request', methods=['GET', 'POST'])
def update_leave_request():
    if 'employeeid' not in session:
        return redirect(url_for('login'))
    if session.get('position') not in ('manager', 'supermanager'):
        return "Access Denied"

    reviewer_id = session['employeeid']
    reviewer_position = session['position']

    if request.method == 'POST':
        leave_id = request.form.get('leave_id')
        decision = request.form.get('decision')
        comment = request.form.get('comment')

        if decision not in ('approved', 'rejected'):
            flash("Invalid decision")
            return redirect(url_for('update_leave_request'))

        conn = connect_to_db()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT employeeid FROM leaves WHERE leave_id=%s", (leave_id,))
        row = cursor.fetchone()

        if not row:
            flash("Leave not found")
            cursor.close()
            conn.close()
            return redirect(url_for('update_leave_request'))

        if row['employeeid'] == reviewer_id:
            flash("cannot approve own leave")
            cursor.close()
            conn.close()
            return redirect(url_for('update_leave_request'))

        cursor.execute("""
            UPDATE leaves
            SET status=%s, manager_comment=%s, manager_id=%s
            WHERE leave_id=%s
        """, (decision, comment, reviewer_id, leave_id))

        cursor.execute("""
                      SELECT s.emailid, s.name, l.leave_type, l.start_date, l.end_date, l.status
                      FROM leaves l
                      JOIN signupdata s ON l.employeeid = s.employeeid
                      WHERE l.leave_id=%s
                      """, (leave_id,)
                      )
        data = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()

        flash("Updated ✅")


        if data:
            send_email(
                 data['emailid'],
                  f"Leave {data['status'].capitalize()}",
                  f"Hello {data['name']},\n\nYour {data['leave_type']} from {data['start_date']} to {data['end_date']} has been {data['status']}.\n\n- Leave Management System"
                )
        return redirect(url_for('update_leave_request'))

    # GET — fetch pending leaves scoped to this reviewer
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT l.*, s.position AS applicant_position, s.manager_id AS applicant_manager_id
        FROM leaves l
        JOIN signupdata s ON l.employeeid = s.employeeid
        WHERE l.status = 'pending'
    """)
    all_pending = cursor.fetchall()
    cursor.close()
    conn.close()

    if reviewer_position == 'manager':
        data = [
            r for r in all_pending
            if r['applicant_position'] == 'employee' and r['applicant_manager_id'] == reviewer_id
        ]
    else:  # supermanager
        data = [
            r for r in all_pending
            if r['applicant_position'] in ('manager', 'hr')
        ]

    return render_template('update_leave_request.html', data=data)



 
     

 
    


@app.route('/hr_default_page')
def hr_dashboard():
    if 'employeeid' not in session:
            return redirect(url_for('login'))
    if session.get('position') != 'hr':
            return "Access Denied"
    employeeid=session['employeeid']
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
       SELECT COUNT(*) as total_employees FROM signupdata WHERE position='employee';
        
        """)
    result = cursor.fetchone()
    number=result['total_employees']

    cursor.execute("""
    SELECT name FROM signupdata WHERE employeeid=%s 
    
    """ ,(employeeid,))
    result1 = cursor.fetchone()
    name = result1['name']

    return render_template(
        'hr_home.html',
         number=number,
          name=name
    )



 
@app.route('/supermanager_dashboard')
def supermanager_dashboard():
    if 'employeeid' not in session:
     return redirect(url_for('login')) 
    if session.get('position') != 'supermanager':
            return "Access Denied"
    
    fresh_login = session.pop('fresh_login', False)
    conn=connect_to_db()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("""
            SELECT * FROM signupdata
            WHERE  employeeid=%s
            """, (session['employeeid'],))
    
    user = cursor.fetchone()
    
   
 

    return render_template('supermanager_home.html',user=user, fresh_login=fresh_login)  
    
     

 
 




@app.route('/add_employee', methods=['GET', 'POST'])
@hr_required
def add_employee():
    form = add_employee_form()

    if form.validate_on_submit():
        if form.position.data != 'employee':
            flash("HR can only create employee accounts", "error")
            return render_template('add_employee.html', form=form)
        conn = connect_to_db()
        cursor = conn.cursor()

        hashed = generate_password_hash(form.password.data)

        cursor.execute("""
        INSERT INTO signupdata (position, employeeid, emailid, password, phone, name, department)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            form.position.data,
            form.employeeid.data,
            form.emailid.data,
            hashed,
            form.phone.data,
            form.name.data,
            form.department.data
        ))

        conn.commit()
        cursor.close()
        conn.close()

        flash("Employee added successfully")
        return redirect(url_for('hr_dashboard'))

    return render_template('add_employee.html', form=form)


@app.route('/manage_employees')
@hr_required
def manage_employees():
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
    SELECT 
        employeeid,
        name,
        emailid,
        phone,
        is_active,
        manager_id
    FROM signupdata
""")
    employees = cursor.fetchall()

    cursor.execute("""
    SELECT 
        employeeid,
        name
    FROM signupdata
    WHERE position = 'manager'
""")
    managers = cursor.fetchall()

# Build a dictionary: {manager_id: manager_name}
    manager_lookup = {m['employeeid']: m['name'] for m in managers}
    for emp in employees:
     emp['manager_name'] = manager_lookup.get(emp['manager_id'], 'Not Assigned')
    cursor.close()
    conn.close()

    return render_template("manage_employees.html", employees=employees)


@app.route('/edit_employee/<employeeid>')
@hr_required
def edit_employee_page(employeeid):
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)

    # 🔹 Get selected employee
    cursor.execute("SELECT * FROM signupdata WHERE employeeid=%s", (employeeid,))
    emp = cursor.fetchone()

    # 🔹 Get all managers
    cursor.execute("""
        SELECT employeeid, name 
        FROM signupdata 
        WHERE position='manager'
    """)
    managers = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "edit_employees_details.html",
        emp=emp,
        managers=managers
    )

@app.route('/update_employee_details', methods=['POST'])
def update_employee_details ():
    emp_id = request.form['employee_id']
    phone = request.form['phone']
    email = request.form['email']
    manager_id = request.form['manager_id']
    is_active = request.form['is_active']

    # ✅ CREATE CONNECTION (IMPORTANT)
    conn = connect_to_db()
    

    cursor = conn.cursor()

    cursor.execute("""
        UPDATE signupdata
        SET phone=%s, emailid=%s, manager_id=%s, is_active=%s
        WHERE employeeid=%s
    """, (phone, email, manager_id, is_active, emp_id))

    conn.commit()

    cursor.close()
    conn.close()

    flash("Employee updated successfully", "success")
    return redirect(url_for('manage_employees'))
 

    


    



@app.route('/assign_manager', methods=['POST'])
@hr_required
def assign_manager():
    emp_id = request.form['employee_id']
    manager_id = request.form['manager_id']

    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE signupdata
    SET manager_id=%s
    WHERE employeeid=%s
    """, (manager_id, emp_id))

    conn.commit()
    cursor.close()
    conn.close()

    flash("Manager assigned successfully")
    return redirect(url_for('hr_dashboard'))




 

@app.route('/leave_policy')
@hr_required
def leave_policy():


 conn = connect_to_db()
 cursor = conn.cursor(dictionary=True)

# Get all leave policies
 cursor.execute("""
    SELECT
        leave_type,
        total_leaves,
        max_per_month,
        min_notice_days,
        allow_half_day
    FROM leave_policy
    ORDER BY leave_type
""")

 policies = cursor.fetchall()


# Get system rules
 cursor.execute("""
    SELECT
        id,
        max_department_leave_percent,
        exclude_weekends,
        exclude_holidays
    FROM system_rules
    ORDER BY id
    LIMIT 1
""")

 system_rules = cursor.fetchone()


# If no system rule exists yet
 if system_rules is None:
    system_rules = {
        'id': None,
        'max_department_leave_percent': 30,
        'exclude_weekends': 1,
        'exclude_holidays': 1
    }


 cursor.close()
 conn.close()

 return render_template(
    'leave_policy.html',
    policies=policies,
    system_rules=system_rules
)
 

@app.route('/save_leave_policy', methods=['POST'])
@hr_required
def save_leave_policy():


 leave_type = request.form.get('leave_type')
 total_leaves = request.form.get('total_leaves')
 max_per_month = request.form.get('max_per_month') or None
 min_notice_days = request.form.get('min_notice_days') or 0

# Checkbox
 allow_half_day = 1 if request.form.get('allow_half_day') else 0


 conn = connect_to_db()
 cursor = conn.cursor()


# Because leave_type is PRIMARY KEY,
# check whether this leave type already exists.
 cursor.execute("""
    SELECT leave_type
    FROM leave_policy
    WHERE leave_type = %s
""", (leave_type,))

 existing = cursor.fetchone()


 if existing:

    # -------------------------
    # UPDATE EXISTING POLICY
    # -------------------------

    cursor.execute("""
        UPDATE leave_policy
        SET
            total_leaves = %s,
            max_per_month = %s,
            min_notice_days = %s,
            allow_half_day = %s
        WHERE leave_type = %s
    """, (
        total_leaves,
        max_per_month,
        min_notice_days,
        allow_half_day,
        leave_type
    ))

    flash(
        f"{leave_type.title()} policy updated successfully.",
        "success"
    )

 else:

    # -------------------------
    # INSERT NEW POLICY
    # -------------------------

    cursor.execute("""
        INSERT INTO leave_policy
        (
            leave_type,
            total_leaves,
            max_per_month,
            min_notice_days,
            allow_half_day
        )
        VALUES (%s, %s, %s, %s, %s)
    """, (
        leave_type,
        total_leaves,
        max_per_month,
        min_notice_days,
        allow_half_day
    ))

    flash(
        f"{leave_type.title()} policy added successfully.",
        "success"
    )


 conn.commit()

 cursor.close()
 conn.close()

 return redirect(url_for('leave_policy'))


 
@app.route('/save_system_rules', methods=['POST'])
@hr_required
def save_system_rules():


 max_department_leave_percent = request.form.get(
    'max_department_leave_percent'
)

# Checkbox values
 exclude_weekends = (
    1 if request.form.get('exclude_weekends') else 0
)

 exclude_holidays = (
    1 if request.form.get('exclude_holidays') else 0
)


 conn = connect_to_db()
 cursor = conn.cursor()


# Get existing system rule
 cursor.execute("""
    SELECT id
    FROM system_rules
    ORDER BY id
    LIMIT 1
""")

 existing = cursor.fetchone()


 if existing:

    # -------------------------
    # UPDATE SYSTEM RULES
    # -------------------------

    cursor.execute("""
        UPDATE system_rules
        SET
            max_department_leave_percent = %s,
            exclude_weekends = %s,
            exclude_holidays = %s
        WHERE id = %s
    """, (
        max_department_leave_percent,
        exclude_weekends,
        exclude_holidays,
        existing[0]
    ))

 else:

    # -------------------------
    # INSERT SYSTEM RULES
    # -------------------------

    cursor.execute("""
        INSERT INTO system_rules
        (
            max_department_leave_percent,
            exclude_weekends,
            exclude_holidays
        )
        VALUES (%s, %s, %s)
    """, (
        max_department_leave_percent,
        exclude_weekends,
        exclude_holidays
    ))


 conn.commit()

 cursor.close()
 conn.close()

 flash(
    "System rules updated successfully.",
    "success"
)

 return redirect(url_for('leave_policy'))


 



 


@app.route('/monthly_report')
def monthly_report():
    if session.get('position') not in ('manager', 'hr'):
        return "Access Denied"

    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT s.employeeid, s.name, SUM(l.totaldays) AS total_days
    FROM leaves l
    JOIN signupdata s ON l.employeeid = s.employeeid
    WHERE MONTH(l.start_date) = MONTH(CURRENT_DATE())
    AND YEAR(l.start_date) = YEAR(CURRENT_DATE())
    AND l.status = 'approved'
    GROUP BY s.employeeid, s.name
    ORDER BY total_days DESC
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    print("DEBUG monthly_report data:", data)   # temporary
     

    return render_template('report.html', data=data)





@app.route('/department_report')
def department_report():
    if session.get('position') not in ('manager', 'hr'):
        return "Access Denied"

    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)
    role=session['position']

    cursor.execute("""
        SELECT s.department, COUNT(l.leave_id) AS total_leaves
        FROM leaves l
        JOIN signupdata s ON l.employeeid = s.employeeid
        WHERE l.status = 'approved'
        AND MONTH(l.start_date) = MONTH(CURRENT_DATE())
        AND YEAR(l.start_date) = YEAR(CURRENT_DATE())
        GROUP BY s.department
    """)
    data = cursor.fetchall()

    cursor.close()
    conn.close()
    parent_template = "manager_dashboard.html" if role == "manager" else "hr_dashboard.html"
    return render_template('department_report.html',parent_template=parent_template, data=data)


@app.route("/department_details/<department>")
def department_details(department):
    if session.get('position') not in ('manager', 'hr'):
        return jsonify({"error": "Access Denied"}), 403

    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            s.employeeid, 
            s.name, 
            COUNT(l.leave_id) AS total_leaves
        FROM signupdata s
        JOIN leaves l ON s.employeeid = l.employeeid
        WHERE s.department = %s 
        AND l.status = 'approved'
        AND MONTH(l.start_date) = MONTH(CURRENT_DATE())
        AND YEAR(l.start_date) = YEAR(CURRENT_DATE())
        GROUP BY s.employeeid, s.name
    """, (department,))

    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)
         




@app.route('/most_absent')

def most_absent():
    if session.get('position') not in ('manager', 'hr' , 'supermanager'):
            return "Access Denied"
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
SELECT s.employeeid, s.name, COUNT(*) AS total_leaves
FROM leaves l
JOIN signupdata s ON l.employeeid = s.employeeid
WHERE l.status = 'approved'
  AND MONTH(l.start_date) = MONTH(CURDATE())
  AND YEAR(l.start_date) = YEAR(CURDATE())
GROUP BY l.employeeid
HAVING total_leaves > 2
ORDER BY total_leaves DESC
""")

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('most_absent.html', data=data)
@app.route('/remaining_leaves')
def remaining_leaves():
    if 'employeeid' not in session:
        return redirect(url_for('login'))

    role = session.get('position')
    employeeid = session['employeeid']

    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)

    # -------- STEP 1: total leaves allowed per type (from leave_policy) --------
    cursor.execute("SELECT leave_type, total_leaves FROM leave_policy")
    policy_rows = cursor.fetchall()
    totals = {row['leave_type']: (row['total_leaves'] or 0) for row in policy_rows}

    casual_total = totals.get('casual leave', 0)
    sick_total = totals.get('sick leave', 0)
    earned_total = totals.get('earned leave', 0)

    # -------- STEP 2: figure out which employees to show --------
    if role == 'employee':
        cursor.execute("""
            SELECT employeeid, name, department
            FROM signupdata WHERE employeeid=%s
        """, (employeeid,))
    elif role == 'manager':
        cursor.execute("""
            SELECT employeeid, name, department
            FROM signupdata WHERE employeeid=%s OR manager_id=%s
        """, (employeeid, employeeid))
    elif role in ('hr', 'supermanager'):
        cursor.execute("SELECT employeeid, name, department FROM signupdata")
    else:
        cursor.close()
        conn.close()
        return "Access Denied"

    employees = cursor.fetchall()

    # -------- STEP 3: for each employee, pull used leaves this year and subtract --------
    data = []
    for emp in employees:
        cursor.execute("""
    SELECT leave_type, COALESCE(SUM(totaldays), 0) AS used
    FROM leaves
    WHERE employeeid=%s
    AND status='approved'
    AND start_date <= '2026-12-31'
    AND end_date >= '2026-01-01'
    GROUP BY leave_type
""", (emp['employeeid'],))
        used_rows = cursor.fetchall()
        used = {row['leave_type']: row['used'] for row in used_rows}

        casual_used = used.get('casual leave', 0)
        sick_used = used.get('sick leave', 0)
        earned_used = used.get('earned leave', 0)

        data.append({
            'employeeid': emp['employeeid'],
            'name': emp['name'],
            'department': emp['department'],
            'casual_total': casual_total,
            'sick_total': sick_total,
            'earned_total': earned_total,
            'casual_used': casual_used,
            'sick_used': sick_used,
            'earned_used': earned_used,
            'casual_remaining': casual_total - casual_used,
            'sick_remaining': sick_total - sick_used,
            'earned_remaining': earned_total - earned_used,
        })

    cursor.close()
    conn.close()

    return render_template('remaining_leaves.html', data=data, role=role)


@app.route('/remaining_employee_leaves')
def remaining_employee_leaves():
    if 'employeeid' not in session:
        return redirect(url_for('login'))

    role = session.get('position')
    employeeid = session['employeeid']

    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)

    # -------- STEP 1: total leaves allowed per type (from leave_policy) --------
    cursor.execute("SELECT leave_type, total_leaves FROM leave_policy")
    policy_rows = cursor.fetchall()
    totals = {row['leave_type']: (row['total_leaves'] or 0) for row in policy_rows}

    casual_total = totals.get('casual leave', 0)
    sick_total = totals.get('sick leave', 0)
    earned_total = totals.get('earned leave', 0)

    # -------- STEP 2: figure out which employees to show --------
   
    cursor.execute("""
            SELECT employeeid, name, department
            FROM signupdata WHERE employeeid=%s
        """, (employeeid,))
 

    employees = cursor.fetchall()

    # -------- STEP 3: for each employee, pull used leaves this year and subtract --------
    data = []
    for emp in employees:
        cursor.execute("""
    SELECT leave_type, COALESCE(SUM(totaldays), 0) AS used
    FROM leaves
    WHERE employeeid=%s
    AND status='approved'
    AND start_date <= '2026-12-31'
    AND end_date >= '2026-01-01'
    GROUP BY leave_type
""", (emp['employeeid'],))
        used_rows = cursor.fetchall()
        used = {row['leave_type']: row['used'] for row in used_rows}

        casual_used = used.get('casual leave', 0)
        sick_used = used.get('sick leave', 0)
        earned_used = used.get('earned leave', 0)

        data.append({
            'employeeid': emp['employeeid'],
            'name': emp['name'],
            'department': emp['department'],
            'casual_total': casual_total,
            'sick_total': sick_total,
            'earned_total': earned_total,
            'casual_used': casual_used,
            'sick_used': sick_used,
            'earned_used': earned_used,
            'casual_remaining': casual_total - casual_used,
            'sick_remaining': sick_total - sick_used,
            'earned_remaining': earned_total - earned_used,
        })

    cursor.close()
    conn.close()

    return render_template('employee_remaining_leaves.html', data=data, role=role)




@app.route('/remaining_manager_leaves')
def remaining_manager_leaves():
    if 'employeeid' not in session:
        return redirect(url_for('login'))

    role = session.get('position')
    employeeid = session['employeeid']

    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)

    # -------- STEP 1: total leaves allowed per type (from leave_policy) --------
    cursor.execute("SELECT leave_type, total_leaves FROM leave_policy")
    policy_rows = cursor.fetchall()
    totals = {row['leave_type']: (row['total_leaves'] or 0) for row in policy_rows}

    casual_total = totals.get('casual leave', 0)
    sick_total = totals.get('sick leave', 0)
    earned_total = totals.get('earned leave', 0)

    # -------- STEP 2: figure out which employees to show --------
   
    cursor.execute("""
            SELECT employeeid, name, department
            FROM signupdata WHERE manager_id=%s
        """, (employeeid,))
 

    employees = cursor.fetchall()

    # -------- STEP 3: for each employee, pull used leaves this year and subtract --------
    data = []
    for emp in employees:
        cursor.execute("""
    SELECT leave_type, COALESCE(SUM(totaldays), 0) AS used
    FROM leaves
    WHERE employeeid=%s
    AND status='approved'
    AND start_date <= '2026-12-31'
    AND end_date >= '2026-01-01'
    GROUP BY leave_type
""", (emp['employeeid'],))
        used_rows = cursor.fetchall()
        used = {row['leave_type']: row['used'] for row in used_rows}

        casual_used = used.get('casual leave', 0)
        sick_used = used.get('sick leave', 0)
        earned_used = used.get('earned leave', 0)

        data.append({
            'employeeid': emp['employeeid'],
            'name': emp['name'],
            'department': emp['department'],
            'casual_total': casual_total,
            'sick_total': sick_total,
            'earned_total': earned_total,
            'casual_used': casual_used,
            'sick_used': sick_used,
            'earned_used': earned_used,
            'casual_remaining': casual_total - casual_used,
            'sick_remaining': sick_total - sick_used,
            'earned_remaining': earned_total - earned_used,
        })

    cursor.close()
    conn.close()

    return render_template('manager_remaining_leaves.html', data=data, role=role)


 

if __name__ == "__main__":
    app.run(debug=False)