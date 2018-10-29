import time
import webbrowser
import selenium.webdriver as webdriver


dr = webdriver.Chrome()
dr.get('https://www.capitaliq.com/CIQDotNet/my/dashboard.aspx?favorite=true')
#
# dr.get('http://stackoverflow.com/')
# dr.execute_script("$(window.open('https://www.capitaliq.com/CIQDotNet/Transcripts/Report.axd?keyDevId=583758909&format=PDF&activityTypeId=9518&myContentType=6&myDocumentType=9'))")
dr.execute_script("$(window.open('https://www.capitaliq.com/CIQDotNet/Transcripts/Report.axd?keyDevId=583758910&format=PDF&activityTypeId=9518&myContentType=6&myDocumentType=9'))")
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