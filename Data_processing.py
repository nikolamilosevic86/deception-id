import Earning_calls_PDF_reader
import sys
from os import listdir
from os.path import isfile, join
import mysql.connector

if __name__ == "__main__":
    if len(sys.argv)<1:
        print("Call Data_processing.py path_to_data_folder")
        exit(0)
    dirpath = sys.argv[1]
    print(dirpath)
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        db = "earnings_calls"
    )
    cursor = mydb.cursor()

    onlyfiles = [f for f in listdir(dirpath) if isfile(join(dirpath, f))]
    error_files_name = 0
    for files in onlyfiles:
        mixedup = False
        print(files)
        sp = files.split(',')
        company = sp[0]
        try:
            q_data = sp[1].split(' ')
            if "Inc." in q_data:
                q_data = sp[2].split(' ')
                mixedup = True
            quarter = q_data[1]
            year = q_data[2]
            if mixedup:
                date = sp[3].replace('.pdf','')
            else:
                date = sp[2].replace('.pdf','')
        except:
            print("Error")
            error_files_name = error_files_name + 1

        doc = Earning_calls_PDF_reader.ProcessDocuments(dirpath+"/"+files)
        ticker = doc.ticker
        stock_exchange = doc.stock_exchange
        add_doc_sql = "Insert into earningcall (company,year,quarter,date,ticker,stockexchange) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(add_doc_sql, (company, year, quarter, date,ticker,stock_exchange))
        mydb.commit()
        earning_call_id = cursor.lastrowid
        for pres in doc.presentations:
            if pres[0] == "Related":
                continue
            if pres[0] == "spglobal.com/marketintelligence":
                continue
            add_presentation = "Insert into presentations(EarningCall_idtable1,Presenter,Position,Presentation) Values (%s,%s,%s,%s)"
            cursor.execute(add_presentation,(earning_call_id,pres[0],pres[1],pres[2]))
            mydb.commit()
        analysts = []
        executives = []
        question = True
        answer = False
        follow_up = False
        was_analyst = False
        prev_analyst = ''
        for question_block in doc.questions_answers:
            if question and question_block[0]=="Operator":
                continue
            if question_block[0] == "spglobal.com/marketintelligence":
                continue
            is_analyst = False
            for analyst in doc.analysts:
                if question_block[0]==analyst['Name']:
                    is_analyst = True
            if is_analyst:
                if prev_analyst==question_block[0]:
                    analysts.append(question_block[0])
                    analyst_name = question_block[0]
                    analyst_role = question_block[1]
                    if analyst_role =='':
                        for ana in doc.analysts:
                            if ana['Name']==question_block[0]:
                                analyst_role = ana['Role']
                    sql_add_question = "Insert into questions (Analyst,Analyst_affiliation,Question,isFollowUp,idQuestionToWhichItFollows,EarningCall_idtable1,hasFollowUps)" \
                                       "Values (%s,%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sql_add_question,
                                   (analyst_name, analyst_role, question_block[2], 0, question_id, earning_call_id, 0))
                    mydb.commit()
                    prev_analyst = question_block[0]
                    was_analyst = True
                    is_analyst = False
                    follow_up_question_id = cursor.lastrowid
                    update_question = "Update questions set hasFollowUps=1 where idQuestions="+str(question_id)
                    cursor.execute(update_question)
                    mydb.commit()
                    question_id = follow_up_question_id
                    continue
                else:
                    analysts.append(question_block[0])
                    analyst_name = question_block[0]
                    analyst_role = question_block[1]
                    if analyst_role == '':
                        for ana in doc.analysts:
                            if ana['Name'] == question_block[0]:
                                analyst_role = ana['Role']
                    sql_add_question = "Insert into questions (Analyst,Analyst_affiliation,Question,isFollowUp,idQuestionToWhichItFollows,EarningCall_idtable1,hasFollowUps)" \
                                       "Values (%s,%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sql_add_question,(analyst_name,analyst_role,question_block[2],0,-1,earning_call_id,0))
                    mydb.commit()
                    question_id = cursor.lastrowid
                    prev_analyst = question_block[0]
                    was_analyst = True
                    is_analyst = False
                    continue
                    # question = False
                    # answer = True
            is_exec = False
            for executive in doc.executives:
                if question_block[0]==executive['Name']:
                    is_exec = True
            if is_exec:
                if was_analyst == False:
                    continue
                # this is follow up question
                sql_add_answer = "Insert into answer (Questions_idQuestions,Answerer,AnswererAffiliation,Answer)" \
                                 "Values (%s,%s,%s,%s)"
                cursor.execute(sql_add_answer,(question_id,question_block[0],question_block[1],question_block[2]))
                mydb.commit()
                is_exec = False
                    # question = False
                    # answer = True
            elif question_block[0] == "Operator":
                # answer = False
                # question = True
                continue
            # else:
            #     sql_add_answer = "Insert into answer (Questions_idQuestions,Answerer,AnswererAffiliation,Answer)" \
            #                      "Values (%s,%s,%s,%s)"
            #     cursor.execute(sql_add_answer,(question_id,question_block[0],question_block[1],question_block[2]))
            #     mydb.commit()
    print("Error processing file name: "+str(error_files_name))

