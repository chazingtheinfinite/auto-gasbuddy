from selenium import webdriver
import os

BASE_QUERY  = 'https://www.allgasstations.com/'
CURR_PATH    = os.path.abspath(os.path.dirname(__file__))
DRIVER_PATH = os.path.join(CURR_PATH, '../drivers/chromedriver/chromedriver.exe')
OUT_FILE    = os.path.join(CURR_PATH, '../data/station-coords/allgas-coords.csv')
STATES      = os.path.join(CURR_PATH, '../data/states.csv')
SLEEP       = 3
VERBOSE     = True

def selenium_based_check(url):
    """ selenium_based_check
        Input:  
            <str> url, iterated AllGasStations website

        Output: 
            <list> res, list of station name and station address in each entry 
    """
    res = []

    # set up driver
    driver = webdriver.Chrome(DRIVER_PATH)
    driver.get(BASE_QUERY + url)
    
    if 'Oops...' in driver.page_source:
        if VERBOSE: print('FAIL')
    else:
        # grab content
        station_count = len(driver.find_elements_by_xpath("//div[@class='wide']//i"))
        addr_list = driver.find_element_by_xpath("//div[@class='wide']").text.split('\n')
        
        if station_count != 0:
            if VERBOSE: print('Exists!')
        
        # extract station name and address
        for i in range(station_count):
            station_name = addr_list[(3*i)].split(":")[1].strip()
            station_addr = addr_list[(3*i+1)].replace(",", " ")
            res.append(station_name + "," + station_addr)
    driver.quit()

    return res

# set current state if resuming progress
curr_state = 'AL'

if os.path.exists(OUT_FILE):
    if VERBOSE: print("Appending...") 
else:
    if VERBOSE: print("Generating file...")
    os.system('touch {}'.format(OUT_FILE))

# grab list of state abbreviations
with open(STATES, 'r') as f:
    state_list = f.read().split('\n')
curr_index = state_list.index(curr_state)

# query data
for i in range(curr_index, len(state_list)):   
    curr_state = state_list[i]
    station_data = selenium_based_check(state_list[i] + "/all/")

    if VERBOSE: print("Current State: {}".format(curr_state + " " + str(i)))

    # write to file
    with open(OUT_FILE, 'a', encoding= 'UTF-8') as f:
        for i in range(len(station_data)):
            f.write("{}\n".format(station_data[i]))

    

