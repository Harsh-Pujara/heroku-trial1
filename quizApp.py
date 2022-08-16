from atexit import register
from tokenize import String
from flask import Flask, render_template, request, jsonify
import mysql.connector
import json
import sys

app=Flask(__name__)

Qid = 0

@app.route('/',methods=['GET','POST'])
def openQuePage():
    return render_template('addQuestion.html')

@app.route('/insertQueData',methods=['GET','POST'])
def queData():
    global Qid

    que = request.form['que']
    op1 = request.form['option1']
    op2 = request.form['option2']
    op3 = request.form['option3']
    op4 = request.form['option4']
    radio = request.form['ans']

    Qid = Qid+1

    mydb = mysql.connector.connect(
                host="localhost", database='quizProject', user="root", passwd="Jv43_/Lar*rne6", use_pure=True)
    cur = mydb.cursor()
    cur.execute("""INSERT INTO qanda(Qid,Question,Option1,Option2,Option3,Option4,CorrectID) VALUES (%s, %s, %s, %s, %s, %s, %s) """, (str(Qid), que, op1, op2, op3, op4,radio))

    mydb.commit()
    cur.close()
    mydb.close()

    return render_template('addQuestion.html')

@app.route('/ab',methods=['GET','POST'])
def dbData():

    mydb = mysql.connector.connect(
                host="localhost", database='quizProject', user="root", passwd="Jv43_/Lar*rne6", use_pure=True)
    cur = mydb.cursor()
    cur.execute("SELECT * FROM qanda")
    data = cur.fetchall()
    i = 0
    j = 0
    count = 1
    listlen = len(data)
    dict = {}
    # mainDict = {}
    datalist = []
    str = ""
    
    while i<listlen:
        dict.update({"numb": count})
        dict.update({"question": (data[i])[j+1]})
        dict.update({"option1":(data[i])[j+2]})
        dict.update({"option2":(data[i])[j+3]})
        dict.update({"option3":(data[i])[j+4]})
        dict.update({"option4":(data[i])[j+5]})

        if (data[i])[j+6] == 'option1':
            dict.update({"answer":(data[i])[j+2]})
        elif (data[i])[j+6] == 'option2':
            dict.update({"answer":(data[i])[j+3]})
        elif (data[i])[j+6] == 'option3':
            dict.update({"answer":(data[i])[j+4]})
        elif (data[i])[j+6] == 'option4':
            dict.update({"answer":(data[i])[j+5]})

        str=str+json.dumps(dict)+","
        # datalist.append(str(dict.copy())) 
        # mainDict.update({str(i+1):dict.copy()})
        # dict.clear()       
        count = count + 1
        i=i+1

    # sys.stdout = open('declare.js','w')
    # jsonobj =json.dumps(datalist)
    # print("var jsonstr = '{}'".format(jsonobj))
    
    cur.close()
    mydb.close()
    # return render_template('dbQuestions.html',parameters=json.dumps(mainDict))
    # return render_template('dbQuestions.html',data=mainDict)
    return json.dumps(dict)
    # return render_template('dbQuestions.html',data=str)
    # return "hello their"

# @app.route('/ab',methods=['GET','POST'])
# def dbData():

#     mydb = mysql.connector.connect(
#                 host="localhost", database='quizProject', user="root", passwd="Jv43_/Lar*rne6", use_pure=True)
#     cur = mydb.cursor()
#     cur.execute("SELECT * FROM qanda")
#     data = cur.fetchall()
#     i = 0
#     j = 0
#     count = 1
#     listlen = len(data)
#     # dict = {}
#     # mainDict = {}
#     # datalist = []
#     mainStr = ""
    
#     while i<1: #listlen

#         if i==0:
#             mainStr = mainStr+"'"+'{"numb":'+ str(count)
#         else:
#             mainStr = mainStr +', '+'{"numb":'+ str(count)

#         mainStr = mainStr +', '+'"question":'+str((data[i])[j+1])
#         mainStr = mainStr +', '+'"option1":'+str((data[i])[j+2])
#         mainStr = mainStr +', '+'"option2":'+str((data[i])[j+3])
#         mainStr = mainStr +', '+'"option3":'+str((data[i])[j+4])
#         mainStr = mainStr +', '+'"option4":'+str((data[i])[j+5])

#         if (data[i])[j+6] == 'option1':
#             mainStr = mainStr +', '+'"answer":'+str((data[i])[j+2])+'}'
#         elif (data[i])[j+6] == 'option2':
#             mainStr = mainStr +', '+'"answer":'+str((data[i])[j+3])+'}'
#         elif (data[i])[j+6] == 'option3':
#             mainStr = mainStr +', '+'"answer":'+str((data[i])[j+4])+'}'
#         elif (data[i])[j+6] == 'option4':
#             if i == (listlen-1):
#                 mainStr = mainStr +', '+'"answer":'+str((data[i])[j+5])+'}'+"'"
#             else:
#                 mainStr = mainStr +', '+'"answer":'+str((data[i])[j+5])+'}'+"'"

#         # datalist.append() 
#         # mainDict.update({str(i+1):dict.copy()})
#         # dict.clear()       
#         count = count + 1
#         i=i+1

#     # sys.stdout = open('declare.js','w')
#     # jsonobj =json.dumps(datalist)
#     # print("var jsonstr = '{}'".format(jsonobj))

#     str1 = '{"name":"John", "age":30, "city":"New York"}'
    
#     cur.close()
#     mydb.close()
#     # return render_template('dbQuestions.html',parameters=json.dumps(mainDict))
#     # return render_template('dbQuestions.html',data=mainDict)
#     return render_template('dbQuestions.html',data = mainStr)
#     # return "hello their"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=84)
