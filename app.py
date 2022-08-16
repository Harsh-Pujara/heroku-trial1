from tokenize import String
from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST']) # To render Homepage
def home_page():
    return render_template('index.html')

@app.route('/math', methods=['POST'])  # This will be called from UI
def math_operation():
    if (request.method=='POST'):
        operation=request.form['operation']
        num1=int(request.form['num1'])
        num2 = int(request.form['num2'])
        if(operation=='add'):
            r=num1+num2
            result= 'the sum of '+str(num1)+' and '+str(num2) +' is '+str(r)
        if (operation == 'subtract'):
            r = num1 - num2
            result = 'the difference of ' + str(num1) + ' and ' + str(num2) + ' is ' + str(r)
        if (operation == 'multiply'):
            r = num1 * num2
            result = 'the product of ' + str(num1) + ' and ' + str(num2) + ' is ' + str(r)
        if (operation == 'divide'):
            r = num1 / num2
            result = 'the quotient when ' + str(num1) + ' is divided by ' + str(num2) + ' is ' + str(r)
        return render_template('results.html',result=result)

@app.route('/via_postman', methods=['POST']) # for calling the API from Postman/SOAPUI
def math_operation_via_postman():
    if (request.method=='POST'):
        operation=request.json['operation']
        num1=int(request.json['num1'])
        num2 = int(request.json['num2'])
        if(operation=='add'):
            r=num1+num2
            result= 'the sum of '+str(num1)+' and '+str(num2) +' is '+str(r)
        if (operation == 'subtract'):
            r = num1 - num2
            result = 'the difference of ' + str(num1) + ' and ' + str(num2) + ' is ' + str(r)
        if (operation == 'multiply'):
            r = num1 * num2
            result = 'the product of ' + str(num1) + ' and ' + str(num2) + ' is ' + str(r)
        if (operation == 'divide'):
            r = num1 / num2
            result = 'the quotient when ' + str(num1) + ' is divided by ' + str(num2) + ' is ' + str(r)
        return jsonify(result)

@app.route('/harsh',methods=['POST'])
def math_operation_harsh():
    name = request.json['name']
    vsp = request.json['lastname']
    # data = {
    #     "First name" : "Harsh",
    #     "Last name" : "Pujara"
    # }
    return name+vsp

@app.route('/return') #search http://127.0.0.1:5000/return?method=sum&a=19&b=65  in browser
def url():
    op = request.args.get('method')
    ab = int(request.args.get('a'))
    sa = int(request.args.get('b'))

    if op == "sum":
        res = ab+sa
    if op == "mul":
        res = ab*sa
    return render_template('results.html',Total=op+" = "+str(res))

@app.route('/test',methods=['POST'])
def js():
    ab = request.json['name']
    bc = request.json['lastname']
    return ab+bc+"hello"

@app.route('/dataInsert',methods=['POST'])
def data():

    fname = request.json['name']
    lname = request.json['lname']
    mail = request.json['email']
    pword = request.json['pass']

    insert_varibles_into_table(fname, lname, mail, pword)

    return "done, data entry successful"

#http://127.0.0.1:5000/dataFromUrl?fname=mihir&lname=bsdk&email=kite@gmail.com&pass=nice
@app.route('/dataFromUrl') 
def urldata():

    fname = request.args.get('fname')
    lname = request.args.get('lname')
    mail = request.args.get('email')
    pword = request.args.get('pass')

    mydb = mysql.connector.connect(host="localhost" , database = 'table1',user="root", passwd="Jv43_/Lar*rne6",use_pure=True)
    cur = mydb.cursor()
    cur.execute("""INSERT INTO logindata(first_name,last_name,email,password) 
                                VALUES (%s, %s, %s, %s) """,(fname, lname, mail, pword))

    # cur.execute("INSERT INTO logindata(first_name,last_name,email,password) VALUES (fname, lname, mail, pword)")
    mydb.commit()
    cur.close()
    mydb.close()

    return "done"

def insert_varibles_into_table(name, lname, email, pword):
    try:   
        mydb = mysql.connector.connect(host="localhost" , database = 'table1',user="root", passwd="Jv43_/Lar*rne6",use_pure=True)

        cur = mydb.cursor()
        mySql_insert_query = """INSERT INTO logindata(first_name,last_name,email,password) 
                                VALUES (%s, %s, %s, %s) """

        record = (name, lname, email, pword)
        cur.execute(mySql_insert_query, record)
        mydb.commit()
        print("Record inserted successfully into Laptop table")

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

    finally:
        if mydb.is_connected():
            cur.close()
            mydb.close()
            print("MySQL connection is closed")


    
if __name__ == '__main__':
    app.run()




