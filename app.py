from flask import Config, Flask, flash, render_template, request, redirect, session, url_for
from database_manager import DatabaseManager
import secrets
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = secrets.token_hex(16)

@app.before_request
def check_login():
    if 'username' not in session and request.endpoint != 'login':
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))
    
@app.route('/')
def index():
    try:
        rec=0
        pay=0
        balance=0
        incr=0
        db = DatabaseManager('expense.db')
        expenses = db.fetch_expenses()

        rows, cols = len(expenses), 5
        array = [[0 for _ in range(cols)] for _ in range(rows)]

        for exp in expenses:
            exp_id = int(exp[0])
            trandisplay=db.fetch_homedisplay(exp_id)
            if trandisplay and len(trandisplay) > 0:
                pay = trandisplay[0][1] if len(trandisplay[0]) > 1 else 0
                rec = trandisplay[1][1] if len(trandisplay) > 1 and len(trandisplay[1]) > 1 else 0
            else:
                pay, rec = 0, 0
            balance=rec-pay
            array[incr][0]=exp[1]
            array[incr][1]=pay
            array[incr][2]=rec
            array[incr][3]=balance
            array[incr][4]=exp_id
            incr+=1
        for row in array:
            print(row)
        return render_template('index.html', arrdisplay=array)
    except Exception as e:
        print(f"Unexpected error: {e}") 

@app.route('/add_expense')
def add_expense():
    db = DatabaseManager('expense.db')
    expenses = db.fetch_expenses()
    db.close()
    return render_template('add_expense.html', expenses=expenses)

@app.route('/changepassword')
def changepassword():
    return render_template('changepassword.html')

@app.route('/updatepass', methods=['POST'])
def updatepass():
    try:
        if request.method == 'POST':
            oldpass = request.form['oldpassword']
            newpass = request.form['newpassword']
            cpass = request.form['cpassword']
            if newpass==cpass:
                print(oldpass,newpass,session['username'])
                db = DatabaseManager('expense.db')
                result = db.update_changepassword(session['username'],oldpass,newpass)
                if result:
                    flash("Changed successfully!", "success")
                else:
                    flash("No record found!", "warning")
            else:
                flash("Password does not match!", "warning")
            db.close()
        return redirect(url_for('changepassword'))
    except Exception as e:
        print(f"Unexpected error: {e}") 

@app.route('/report')
def report():
    expid=request.args.get('expid')
    db = DatabaseManager('expense.db')
    report_data = db.fetch_report(expid)
    db.close()
    return render_template('report.html', data=report_data)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    try:
        db = DatabaseManager("expense.db")
        if request.method == 'POST':
            expense_type = request.form['expense_type']
            amount = 0
            transaction_type = ''
            description = request.form['description']
        
            db.insert_expense(expense_type,amount,transaction_type,description, session['username'])
            expenses = db.fetch_expenses()
            print("Users in database:", expenses)   
        return redirect(url_for('add_expense'))
    except Exception as e:
        print(f"Unexpected error: {e}") 
        # Process form data as needed
        
@app.route('/transaction')
def exptransaction():
    db = None  # Initialize db to ensure it's accessible in the finally block
    try:
        db = DatabaseManager('expense.db')
        trans = db.fetch_transaction()
        expenses = db.fetch_expenses()
    except Exception as e:
        print(f"Error fetching transactions: {e}")
        trans = []  # Provide a fallback value in case of an error
        expenses=[]
    finally:
        if db:  # Only close the connection if db was successfully initialized
            db.close()

    return render_template('transaction.html', transaction=trans,expenses=expenses)

@app.route('/add_expense')
def contact():
    return render_template('add_expense.html')

@app.route('/submittran', methods=['GET', 'POST'])
def submittran():
    try:
        db = DatabaseManager("expense.db")
        if request.method == 'POST':
            expensetypeid=request.form.get('expense_type')
            expense_type=db.fetch_expensetypebyId(expensetypeid)
            amount = request.form['amount']
            transaction_type = request.form['transaction_type']
            description = request.form['description']
        
            db.insert_transaction(expensetypeid,expense_type[0],amount,transaction_type,description, session['username'])
            trans = db.fetch_transaction()
            print("Users in database:", trans)   
        return redirect(url_for('exptransaction'))
    except Exception as e:
        print(f"Unexpected error: {e}") 
        # Process form data as needed


@app.route('/delete_expense', methods=['GET', 'POST'])
def delete_expense():
    try:
        db = DatabaseManager("expense.db")
        if request.method == 'POST':
            expense_id = request.args.get('expense_id')  # Get the query parameter
            if expense_id:
                db.delete_expenses(expense_id)
                db.alter_table()
                #db.insert_login("ash","allok123")
                expenses = db.fetch_expenses()
                print("Users in database:", expenses)   
            return redirect(url_for('add_expense'))
    except Exception as e:
        print(f"Unexpected error: {e}") 

@app.route('/delete_trans', methods=['GET', 'POST'])
def delete_trans():
    try:
        db = DatabaseManager("expense.db")
        if request.method == 'POST':
            trans_id = request.args.get('trans_id')  # Get the query parameter
            if trans_id:
                db.delete_expenses_trans(trans_id)
                # db.alter_table()
                
                expenses = db.fetch_transaction()
                print("Users in database:", expenses)   
            return redirect(url_for('exptransaction'))
    except Exception as e:
        print(f"Unexpected error: {e}") 
@app.route('/login', methods=['GET', 'POST'])
def login():
    
    
    db = DatabaseManager("expense.db")
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        usernamereturn=db.fetch_login(username,password)
        print(usernamereturn)
        # Validate credentials
        if usernamereturn is not None and usernamereturn[0] != "":
            session['username'] = username  # Store username in session
            # flash("Login successful!", "success")
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password.", "danger")
    
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
