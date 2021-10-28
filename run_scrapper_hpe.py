#program to get all the EOL HPE devices in readable form (table) and easy to download
# HPE Networking End of Sale Products | Hewlett Packard Enterprise


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import openpyxl

#hebe

# locating chrome driver
PATH = "C:\\Users\\mradosovsky2\\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("https://techlibrary.hpe.com/us/en/networking/products/eos/index.aspx")
print(driver.title)

# selecting radio buttons on the first page
select_r_button_announcment = driver.find_element_by_xpath("//*[@id='type2_id']")
select_r_button_announcment.click()
# second button
select_r_button_hw_type = driver.find_element_by_xpath("//*[@id='category1_id']")
select_r_button_hw_type.click()


# take all tables from the body elemt of the webpage - all tables are in the <html body>
tables = driver.find_element_by_id("body")
# table volume contains webdriver object that is having all tables ("divTable") stored as separate entry
# len() can be used to find how many tables "divTable is in the html body"
table_volume = tables.find_elements_by_class_name("divTable")
total_row_volume = tables.find_elements_by_tag_name("tr")


print("##########")
print("####")
print("##")
print("#")
# print(type(table_volume))

# this one counts all the rows in the body
print(f' Total row wolume:',len(total_row_volume))
print("#")
print("##")
print("####")
print("##########")



final_table = []
final_rows = []
all_elements = []
all_pub_dates = []
all_row_sequence = []

# for table in range (1,5):
for table in range (1,len(table_volume)+1):

    #locating lements tahat are requited for final prodcut
    table_prerequisite = tables.find_element_by_xpath('//*[@id="table' + str(table) + '"]')
    pub_date = table_prerequisite.find_element_by_xpath('//*[@id="pubDate' + str(table) + '"]')
    element_volume = table_prerequisite.find_elements_by_tag_name("td")
    table_row_volume = table_prerequisite.find_elements_by_tag_name("tr")
    
    # creating list that contains all table row lenght
    all_row_sequence.append(len(table_row_volume))
    # . text method function below retrun expected result in text form, instead of webdriver class/object
    all_pub_dates.append(pub_date.text)    


    [all_elements.append(column.text) for column in element_volume]

# cleaning unwanted symbols from text - "\n"
all_ell_edited = []
[all_ell_edited.append(x.replace("\n", " ")) for x in all_elements]
# end

# all data is stored you can quit browser
driver.quit()




#changing list to array
result=[]
start = 0
end = 4
for i in total_row_volume: 
# for i in range(17):
    # array stored in variable "result" 
    result.append(all_ell_edited[start:end])
    start +=4
    end += 4

# cummulative value - counts number of rows
intermediate_value = [0]
cummulative_row_list = []
for i in range(len(all_row_sequence)):
    intermediate_value[0] = intermediate_value[0] + all_row_sequence[i]
    cummulative_row_list.append(intermediate_value[0])
print(cummulative_row_list)

# index for all_pub_date and cummulative_row_list
n=0

# go trough every line (row)
for i in range(len(result)):
    # result[i].insert(0, "date")
    # if its not header of table add date value corresponding to the table
    if i < cummulative_row_list[n] and i != 0:
        result[i].insert(0, all_pub_dates[n])
    # if its start of table create frist column with header "--Published--"
    elif i == 0 or i == cummulative_row_list[n]:
        result[i].insert(0, "--Published--")
        # i == 0 cant be found in the cummulative row table, therofre this if
        # statment help add 1 to [n] once needed
        if i == cummulative_row_list[n]:
            n += 1
    else:
        # this one might not be needed and whole for loop could be rewritten 
        # into more simple loop but its working as it should and script is finished
        # no reason/time to rewrite the loop at the moment
        n += 1
    # print(i)


# print(result)
# print(all_pub_dates)
# print(all_row_sequence)

##______________________________________________________###

df = pd.DataFrame(result)

pd.options.display.max_columns = 5
print(df)

df.to_excel(r'C:\Users\mradosovsky2\Documents\Python39\HPE_scrapper\HPE_EOS.xlsx', index = False)

time.sleep(1)

# search.send_keys("test")
# search.send_keys(Keys.RETURN)



# finally: