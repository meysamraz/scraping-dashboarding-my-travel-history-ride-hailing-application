"""
Created on  Sep 3  2022
@author: Meysam Raz
"""


from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from datetime import date
from time import sleep
import pandas as pd


class SnappTravelScrapper :
    def __init__(self,phone_number):
        chrome_options = Options()
        chrome_options.add_argument('--profile-directory=Default')
        self.drive =  webdriver.Chrome(executable_path='CHROMEDRIVE_PATH',chrome_options=chrome_options)
        
        # Snapp travel history 
        self.drive.get('https://app.snapp.taxi/ride-history')
        sleep(10)
        
        # verify account
        self.drive.find_element_by_xpath("/html/body/div[2]/div/main/div[4]/div/div[2]/div/main/form/div[1]/div/div/div/input").send_keys(phone_number)
        sleep(4)
        self.drive.find_element_by_xpath("/html/body/div[2]/div/main/div[4]/div/div[2]/div/main/form/div[2]/button").click()
        
        # Enter code  
        sleep(20)
        
        # travel hours 
        travel_hours  =   self.drive.find_element_by_xpath('/html/body/div[2]/div/main/div[4]/div/main/div[2]/div[2]/div[1]/p[1]').text
        
        # number of  travel
        travel_counts =   self.drive.find_element_by_xpath('/html/body/div[2]/div/main/div[4]/div/main/div[2]/div[2]/div[2]/p[1]').text
        
        #km travels
        travel_km     =   self.drive.find_element_by_xpath('/html/body/div[2]/div/main/div[4]/div/main/div[2]/div[2]/div[3]/p[1]').text
        
        # current date
        today = date.today()
        datenow = today.strftime("%d/%m/%Y")
        
        # creating a data frame with scraped data
        data_summrey = {'Travel Hours':travel_hours,'Travel Counts': travel_counts,'Travel Km':travel_km,'date':datenow}

        df_summrey = pd.DataFrame(data_summrey, index=[0]) 
        
        # save data into a csv file
        df_summrey.to_csv('snapp_summrey.csv',index=False)
        print('success')
        sleep(10)    
        
        # extract travel history links 
        l=[]
        for a in self.drive.find_elements_by_xpath('/html/body/div[2]/div/main/div[4]/div/main/div[2]/div[3]/a'):
            link = a.get_attribute('href')
            l.append(link)
        print('done')
        sleep(2)  
        
        # open each travel link   
        for b in range(len(l)):
            self.drive.execute_script("window.open('');")
            sleep(4)
            self.drive.switch_to.window(self.drive.window_handles[b+1]) 
            sleep(4)
            self.drive.get(l[b])
            sleep(4)
            
            # Extract travel star 
            stars = self.drive.find_elements_by_xpath('/html/body/div[2]/div/main/div[4]/div/main/div/div[1]/div[1]/div/button')
            stars_list = []
            for star in stars:
                stars_num = star.get_attribute("aria-checked")
                stars_list.append(stars_num)
           
           
            # count on stars
            star = stars_list.count('on')
            
            # travel day title 
            day_title = self.drive.find_element_by_xpath('/html/body/div[2]/div/main/div[4]/div/header/div/div[2]/div').text
            
            # car
            car = self.drive.find_element_by_xpath('/html/body/div[2]/div/main/div[4]/div/main/div/div[2]/div[1]/p[1]').text
            
            # travel cost
            price = self.drive.find_element_by_xpath('/html/body/div[2]/div/main/div[4]/div/main/div/div[4]/div[1]/div[2]').text
            
            # travel date 
            datet = self.drive.find_element_by_xpath('/html/body/div[2]/div/main/div[4]/div/main/div/div[4]/div[2]/div[2]').text
            
            # trave time
            date_time = self.drive.find_element_by_xpath('/html/body/div[2]/div/main/div[4]/div/main/div/div[4]/div[3]/div[2]').text
            
            # origin travel
            origin = self.drive.find_element_by_xpath('/html/body/div[2]/div/main/div[4]/div/main/div/div[3]/div/div[1]/div[2]/p').text
            
            # destination travel
            destination = self.drive.find_element_by_xpath('/html/body/div[2]/div/main/div[4]/div/main/div/div[3]/div/div[2]/div[2]/p').text
            
            df = pd.read_csv('travel_history.csv')
            df2 = pd.DataFrame([[day_title,car,price,datet,date_time,origin,destination,star]], columns=['day_title','car','price','date','date_time','origin','destination','star'])
            df = df.append(df2, ignore_index = True)
            df.to_csv('travel_history.csv',index=False)
            
        sleep(2)        
        print('done2')    
        self.drive.quit()


SnappTravelScrapper()