import mysql.connector
import csv
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    db="earnings_calls"
)
cursor = mydb.cursor()
with open('database_stats.csv', mode='w') as employee_file:
    stats = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    stats.writerow(
        ["ID", "company", "year", "quarter", "ticker", "stock", "date", "number_presentations", "number_questions", "number_answers"])
    sql = "Select * from earningcall"
    cursor.execute(sql)
    ecalls = cursor.fetchall()
    for ecall in ecalls:
        id = ecall[0]
        year = ecall[1]
        quarter = ecall[2]
        company = ecall[3]
        ticker = ecall[4]
        date = ecall[5]
        stock  = ecall[6]
        pres_sql = "Select count(*) from presentations where EarningCall_idtable1="+str(id)
        cursor.execute(pres_sql)
        npres = cursor.fetchall()
        number_presentations = 0
        for npre in npres:
            number_presentations = npre[0]
        ques_sql = "Select count(*) from questions where EarningCall_idtable1=" + str(id)
        cursor.execute(ques_sql)
        nquestions = cursor.fetchall()
        number_questions = 0
        for nques in nquestions:
            number_questions = nques[0]
        ans_sql = "SELECT EarningCall_idtable1,count(*) as cnt FROM earnings_calls.answer left join questions on idQuestions=Questions_idQuestions  where EarningCall_idtable1="+str(id)
        cursor.execute(ans_sql)
        nanswers = cursor.fetchall()
        number_answers = 0
        for npre in nanswers:
            number_answers = npre[1]
        stats.writerow([id,company,year,quarter,ticker,stock,date,number_presentations,number_questions,number_answers])

