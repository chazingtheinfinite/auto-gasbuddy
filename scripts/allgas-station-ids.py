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
        # determine number of subdivisions of city list
        section_count = len(driver.find_elements_by_xpath("//div[@class='wide']"))
        section_list = []

        for i in range(1, section_count + 1):
            # subdivisions of city list
            section_list.append(driver.find_element_by_xpath("//div[@class='wide'][{}]".format(i)).text.split('\n'))
        
        for i in range(len(section_list)):
            for j in range(len(section_list[i])):
                driver.get(BASE_QUERY + url + "/" + section_list[i][j].replace(' ', '_'))
                
                if VERBOSE: print("Current city: {}".format(section_list[i][j]))
                
                # station list and count of current city
                station_list = driver.find_element_by_xpath("//div[@class='wide']").text.split('\n')
                station_count = len(driver.find_elements_by_xpath("//div[@class='wide']//i"))
                
                for k in range(station_count):
                    station_name = station_list[(3*k)].split(":")[1].strip()
                    station_addr = station_list[(3*k+1)].replace(",", " ")

                    if VERBOSE: print("Station Name: {}, Station Address: {}".format(station_name, station_addr))

                    res.append(station_name + "," + station_addr)
                    driver.back()
    driver.quit()
    return res

# set current state if resuming progress
curr_state = 'MI'

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
    station_data = selenium_based_check(state_list[i])

    if VERBOSE: print("Current State: {}".format(curr_state + " " + str(i)))

    # write to file
    with open(OUT_FILE, 'a', encoding= 'UTF-8') as f:
        for i in range(len(station_data)):
            f.write("{}\n".format(station_data[i]))

    

