'''
this script loads an html file 'web.html' and searches all alexa utterance 
voice to text translations, and prints them.

This script should be modified to access the website automatcally and keep jumping page to page downloading and parsing the website.
So this code could be all found inside a function tat is called very time a new website is opened and parsed
'''

import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait as wait
import datetime
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
import urllib.request
import re
import json
import sys

# Create a new instance of the Google driver
driver = webdriver.Firefox(executable_path="C:\\Users\\k1772492\\Downloads\\chromedriver_win32\\geckodriver.exe")
    
def Url():      
    #driver.maximize_window()
       
    # go to the Amazon login URL
    driver.get("https://www.amazon.com/ap/signin?_encoding=UTF8&ignoreAuthState=1&openid.assoc_handle=usflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3Fref_%3Dnav_custrec_signin&switch_account=")

    # filling the login in form
    driver.find_element_by_id('ap_email').send_keys('')
    driver.find_element_by_id('ap_password').send_keys('')
    driver.find_element_by_id('signInSubmit').click()

    driver.get('https://www.amazon.com/s/ref=nb_sb_ss_c_2_6?url=search-alias%3Dalexa-skills&field-keywords=skills&sprefix=skills%2Caps%2C199&crid=3OLJG17YRDLNJ')

    #clicking the 90days skills link
    #driver.find_element_by_xpath('//*[@id="leftNav"]/ul[1]/div/li[3]/span/a/span').click()
    
    for i in range(1000):
        print('*****LOADING PAGE {}'.format(i))
        time.sleep(5)
        page = driver.page_source
        #print(page)
        soup = bs(page, "html.parser")

        #maximising window
        #driver.maximize_window()

        #GET CURRENT url
        x = driver.current_url

        #refreshing browser
        driver.get(x)
        
        for a in soup.findAll("a", attrs={"class": "s-access-detail-page"}):
            Skill_Url = (a['href'])
            SkillDetails(Skill_Url)      

        #Get next page
        driver.get(x)
        driver.find_element_by_id('pagnNextString').click()    

def SkillDetails(a):
    f = open ('Skills_link', 'a+')
    f.write('{}\n' .format(a))
    driver.get(a)
    
    #getting the permission
    #enabling the skill
    #driver.find_element_by_class_name('a-button a-button-span12 a-button-primary a2s-button').click()
    #time.sleep(2)
      
    page = driver.page_source
    soup = bs(page, "html.parser")

    #disabling the skill
    #driver.find_element_by_class_name('a-button a-button-span12 a-button-primary a2s-button').click()

    skills_details= dict()

    #getting the permission
    try:
        
        skill_permission = soup.find("li", attrs={"class": "a2s-permissions-list-item"})
        skill_permission= skill_permission.get_text().strip()
    except:
        skill_permission= "No skill_permission required"

    #Checking if account linking required
    try:
        account_linking = soup.find("span", attrs={"id": "a2s-skill-account-link-msg"})
        account_linking = account_linking.get_text().strip()
    except:
        account_linking = "No account linking required"
    
        
    #get the skill name    		
    skill_name= soup.find("h1", attrs={"class": "a2s-title-content"})
    skill_name = skill_name.get_text().strip()
    #print(skill_name)

    #get the skill_developer    		
    skill_developer= soup.find("span", attrs={"class": "a-size-base a-color-secondary"})
    skill_developer = skill_developer.get_text().strip()
    #print(skill_developer)
      
    #get the skill review
    try:
        skill_review= soup.find("h2", attrs={"data-hook": "total-review-count"})
        skill_review = skill_review.get_text().strip()

    except:
        skill_review= soup.find("span", attrs={"data-hook": "total-review-count"})
        skill_review = skill_review.get_text()     

    #take the firststring from skill_review
    splitted = skill_review.split()
    actual_reviews = splitted[0]
    print(actual_reviews)

    #replace the comma in the total number of reviews
    actual_reviews = int(actual_reviews.replace(",", ""))
    print(actual_reviews)

    #getting the skills category
    cat= soup.findAll("a", attrs={"class": "a-link-normal a-color-tertiary"})
    
    if len(cat)>0:
        try:
            #cat1 = cat[0].get_text().strip()
            cat2 = cat[1].get_text().strip()
            skills_details['Category']= cat2
            #print(cat2)
            #print(cat1)        
        except:
            skills_details['Category']= "No Category"
                   
    #get the skill rating
    try:   
        skill_rating= soup.find("h2", attrs={"data-hook": "total-rating-count"})
        skill_rating = skill_rating.get_text().strip()
        #print(skill_rating)
    except:
        #print("No customer Ratings")
        skill_rating = "No customer Ratings"
                
    #get the Total_Customers_Reviews
    try:
        Total_Customers_Reviews= soup.find("span", attrs={"class": "arp-rating-out-of-text a-color-base"})
        Total_Customers_Reviews = Total_Customers_Reviews.get_text().strip()
        #print(Total_Customers_Reviews)
    except:
        #print("No Customers Reviews")
        Total_Customers_Reviews = "No Customers Reviews"

    #get the cost
    try:     
        cost_of_skill = soup.find("p", attrs={"class": "a-spacing-none a-text-left a-size-medium a-color-price"})
        cost_of_skill = cost_of_skill.get_text().strip()
    except:
        cost_of_skill = soup.find("p", attrs={"class": "a-spacing-none a-text-left a-size-medium a-color-price"})
        cost_of_skill = cost_of_skill

    #get the skill description
    skill_description = soup.find("div", attrs={"id": "a2s-description"})
    skill_description= skill_description.get_text("\n").strip()
        
    #GET  INVOCATION NAMES
    invocation_names= soup.findAll("div", attrs={"class": "a2s-utterance-box a2s-bubble"})
    b =list()
    for a in invocation_names:
        #print('{}\n'.format(a.get_text().strip()))
        b.append(a.get_text().strip())
        #mymy.write('{}\n'.format(a.get_text().strip()))
    skills_details['invocation_names']= b        
    skills_details['name']=skill_name
    skills_details['Developer']= skill_developer
    skills_details['skill_permission'] = skill_permission
    skills_details['account_linking'] = account_linking
    skills_details['Review']= skill_review
    skills_details['Rating']= skill_rating
    skills_details['Total_Customers_Reviews']= Total_Customers_Reviews
    skills_details['Cost']= cost_of_skill
    skills_details['skill_description']=skill_description

    #GET DYNAMIC CONTENT
    a=list()
    a = soup.findAll("a", attrs={"rel": "noopener"})
    
    #writing privacy link and developer link seperate 
    mymy = open('privacy_developer','a+',encoding='utf8')

    #Checking to see if privacy_link and developer_link exist
    if len(a)>0:
        try:
            a1 = a[0]
            a2 = a[1]
            privacy_policy = (a1['href'])
            Terms_of_use = (a2['href'])
            skills_details['privacy_policy']= privacy_policy
            skills_details['Terms_of_use']= Terms_of_use
            mymy.write('\nprivacy_policy: {}\nTerms_of_use: {}\n'.format(privacy_policy, Terms_of_use))
            
        except:
            a1 = a[0]
            privacy_policy = (a1['href'])
            skills_details['privacy_policy']= privacy_policy
            mymy.write('privacy_policy:{}\n'.format(privacy_policy))
    else:
        skills_details['privacy_policy and Terms_of_use specified']= "No privacy_policy and Terms_of_use specified"
        mymy.write("No privacy_policy and Terms_of_use specified")


    #Loading the all Review Page
    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div/div[2]/div/div[2]/span[3]/div/div/div[4]/div[2]/a').click()

    for i in range(int(actual_reviews/10)):
        
        print('*****LOADING PAGE {} Review'.format(i+1))
        time.sleep(5)
        page2 = driver.page_source
        soup2 = bs(page2, "html.parser")
        #print(soup2)

        #GET COURRENT url
        x = driver.current_url
        
        review={}
        d=list()
        b=list()
        c=list()
        c = soup2.findAll("span", attrs={"class":"a-profile-name"})
        b = soup2.findAll("span", attrs={"data-hook":"review-body"})
        
        for i in range(10):
            abi = c[i].get_text().strip()
            dio = b[i].get_text().strip()
            review[abi]= dio
            d.append(review)
            
    
        #Get Next Review Page
        driver.get(x)
        try:        
            #driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[2]/div/div[1]/div[3]/div[3]/div[11]/span/div/ul/li[8]').click()
            driver.find_element_by_class_name('a-last').click()    
        except:
            driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[2]/div/div[1]/div[3]/div[3]/div[12]/span/div/ul/li[7]').click()

    skills_details['review'] = d
    #print(d)
    print("done")
    
    #dump all what you have to a file
    with open('file.json', 'a+', encoding='utf8') as fp:
        json.dump(skills_details, fp)
        fp.write('\n')
        
data = Url()
