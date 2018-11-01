import time
import webbrowser
import selenium.webdriver as webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from credentials import *

from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import csv
dr = webdriver.Chrome()
dr.get('https://www.capitaliq.com/CIQDotNet/my/dashboard.aspx?favorite=true')
myElem = WebDriverWait(dr, 10).until(EC.presence_of_element_located((By.ID, 'username')))
print("Page is ready!")
dr.find_element_by_name("username").send_keys(username);
passw = dr.find_element_by_name("password")
passw.send_keys(password)
passw.send_keys(Keys.RETURN)
time.sleep(5)
with open('Earningscalls_USexchanges_all.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count != 0:
            num = row[1][4:]
            dr.get('https://www.capitaliq.com/CIQDotNet/Transcripts/Report.axd?keyDevId=' + str(
                num) + '&format=PDF&activityTypeId=9518&myContentType=6&myDocumentType=9')
            time.sleep(1)

        line_count = line_count + 1





#
# dr.get('http://stackoverflow.com/')
# dr.execute_script("$(window.open('https://www.capitaliq.com/CIQDotNet/Transcripts/Report.axd?keyDevId=583758909&format=PDF&activityTypeId=9518&myContentType=6&myDocumentType=9'))")
#dr.execute_script("$(window.open('https://www.capitaliq.com/CIQDotNet/Transcripts/Report.axd?keyDevId=2505751&format=PDF&activityTypeId=9518&myContentType=6&myDocumentType=9'))")
# initial_num = 583758909
# max_num = 100
# i = initial_num
# while i<initial_num+max_num:
#     url = 'https://www.capitaliq.com/CIQDotNet/Transcripts/Report.axd?keyDevId='+str(i)+'&format=PDF&activityTypeId=9518&myContentType=6&myDocumentType=9'
#     i = i+1
# # Open URL in a new tab, if a browser window is already open.
#     webbrowser.open_new_tab(url)


# Open URL in new window, raising the window if possible.
#webbrowser.open_new(url)
time.sleep(5)
dr.close()
# dr.switch_to.window(dr.window_handles[-1])
# dr.close()
# dr.switch_to.window(dr.window_handles[-1])
# dr.close()