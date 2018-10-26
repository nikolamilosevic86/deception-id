import time
import webbrowser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


dr = webdriver.Chrome()

dr.get('https://www.capitaliq.com')
#dr.execute_script("$(window.open('https://www.capitaliq.com/CIQDotNet/Transcripts/Report.axd?keyDevId=583758909&format=PDF&activityTypeId=9518&myContentType=6&myDocumentType=9'))")
#dr.execute_script("$(window.open('https://www.capitaliq.com/CIQDotNet/Transcripts/Report.axd?keyDevId=583758910&format=PDF&activityTypeId=9518&myContentType=6&myDocumentType=9'))")
time.sleep(10)
element = WebDriverWait(dr, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
element = dr.find_elements_by_name("username")[0]
element.send_keys('Uml.bds2@manchester.ac.uk')
time.sleep(1)
inputElement = dr.find_elements_by_name("password")[0]
inputElement.send_keys('L2brary2')
time.sleep(1)
inputElement.send_keys(Keys.ENTER)
time.sleep(4)
j = 0
for i in range(583758909, 583759099):
    dr.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
    dr.get('https://www.capitaliq.com/CIQDotNet/Transcripts/Report.axd?keyDevId='+str(i)+'&format=PDF&activityTypeId=9518&myContentType=6&myDocumentType=9')
    # time.sleep(1)
    # j = j+1
    # if j==10:
    #     time.sleep(5)
    #     j = 0
# max_num = 100
# i = initial_num
# while i<initial_num+max_num:
#     url = 'https://www.capitaliq.com/CIQDotNet/Transcripts/Report.axd?keyDevId='+str(i)+'&format=PDF&activityTypeId=9518&myContentType=6&myDocumentType=9'
#     i = i+1
# # Open URL in a new tab, if a browser window is already open.
#     webbrowser.open_new_tab(url)


# Open URL in new window, raising the window if possible.
#webbrowser.open_new(url)
# time.sleep(5)
# dr.close()
# dr.switch_to.window(dr.window_handles[-1])
# dr.close()
# dr.switch_to.window(dr.window_handles[-1])
# dr.close()