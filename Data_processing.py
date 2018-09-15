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
    for files in onlyfiles:
        mixedup = False
        sp = files.split(',')
        company = sp[0]
        q_data = sp[1].split(' ')
        if "Inc." in q_data:
            q_data = sp[2].split(' ')
            mixedup = True
        quarter = q_data[1]
        year = q_data[2]
        if mixedup:
            date = sp[3]
        else:
            date = sp[2]
        add_doc_sql = "Insert into earningcall (company,year,quarter,date) VALUES (%s,%s,%s,%s)"
        cursor.execute(add_doc_sql, (company, year,quarter,date))
        mydb.commit()
        doc = Earning_calls_PDF_reader.ProcessDocuments(dirpath+"/"+files)
        # for pres in doc.presentations:
        #     print(pres[0])
        #     print(pres[1])
        #     print(pres[2])
