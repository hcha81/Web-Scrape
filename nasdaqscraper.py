from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import re
import pandas as pd
from numpy import nan



def get_elements(xpath):
    elements = driver.find_elements_by_xpath(xpath) # find the elements
    text = []
    for e in elements:
            text.append(e.text)
            #print(e.text)
    return text




driver = webdriver.Chrome()


url_form = "https://www.nasdaq.com/symbol/{}/short-interest"
url_form2 = "https://www.nasdaq.com/symbol/{}/ownership-summary"

shorts_xpath = "//tbody/tr/td[{}]"
ownership_xpath = "//tbody/tr/th[text() = '{}']/../td"
iholdings_xpath = "//*[@class='floatL']//a"
iholdvalue_xpath = "//*[@class='floatL']//td[2]"


## company ticker symbols
symbols = ["fb","amzn", "aapl","nflx","goog"]
dfshortinterest = pd.DataFrame()
dfholders = pd.DataFrame()
dfinsts = pd.DataFrame()
dfinsider = pd.DataFrame()

for i, symbol in enumerate(symbols):

    ## navigate to short interest page
    url = url_form.format(symbol)
    driver.get(url)
    

    company_xpath = "//h1[contains(text(), 'Short Interest')]"
    company = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, company_xpath))).text
    print(company)
    

    date = get_elements(shorts_xpath.format("1"))
    short_interest = get_elements(shorts_xpath.format("2"))
    volume = get_elements(shorts_xpath.format("3"))
    daystocover = get_elements(shorts_xpath.format("4"))
    
    cpy = []
    cpy.append(company)
    cpy = cpy * 23

    sym = []
    sym.append(str(symbol))
    sym = sym * 23

    #print(company)
    date = date[3:26]
    #print(date)
    short_interest = short_interest[0:23]
    #print(short_interest)
    volume = volume[0:23]
    #print(volume)
    #print(daystocover)

    
    df1=pd.DataFrame(cpy,columns=['Company'])
    df2=pd.DataFrame(sym, columns=['Symbol'])
    df3=pd.DataFrame(date, columns=['Date'])
    df4=pd.DataFrame(short_interest, columns=['ShortInterest'])
    df5=pd.DataFrame(volume, columns=['Volume'])
    df6=pd.DataFrame(daystocover, columns=['DaysToCover'])

    dftemp=pd.concat([df1,df2,df3,df4,df5,df6], axis = 1)
    
    dfshortinterest=dfshortinterest.append(dftemp)

    #Ownership Summary Section
    url = url_form2.format(symbol)
    driver.get(url)


    holdings = get_elements(ownership_xpath.format("Institutional Holdings"))
    numholders = get_elements(ownership_xpath.format("Total Number of Holders"))
    numshares = get_elements(ownership_xpath.format("Total Shares Held"))
    value = get_elements(ownership_xpath.format("Total Value of Holdings"))


    symi = []
    symi.append(str(symbol))

    df10=pd.DataFrame(symi, columns=['Symbol'])
    df11=pd.DataFrame(holdings,columns=['InstHoldings'])
    df12=pd.DataFrame(numholders, columns=['NumberOfHolders'])
    df13=pd.DataFrame(numshares, columns=['NumberOfShares'])
    df14=pd.DataFrame(value, columns=['ValueOfHoldings'])


    dftempi=pd.concat([df10,df11,df12,df13,df14], axis = 1)
    dfinsts=dfinsts.append(dftempi)


    #print(holdings)
    #print(holders)
    #print(shares)
    #print(value)

    #net activity includes insider activity
    activity = get_elements(ownership_xpath.format("Net Activity"))
    allactivity = activity[0]
    monthactivity = activity[1:3]

    #print(allactivity)
    #print(monthactivity)


    #Institutional Holders positions
    iholdername = get_elements(iholdings_xpath)
    iholdername = iholdername[0:5]
    iholdervalue = get_elements(iholdvalue_xpath)
    iholdervalue = iholdervalue[0:5]
    #print(iholdername)
    #print(iholdervalue)

    symh = []
    symh.append(str(symbol))
    symh = symh * 5

    df7=pd.DataFrame(symh, columns=['Symbol'])
    df8=pd.DataFrame(iholdername, columns=['HolderName'])
    df9=pd.DataFrame(iholdervalue, columns=['HolderValue'])
    
    dftemph=pd.concat([df7,df8,df9], axis = 1)
    
    dfholders=dfholders.append(dftemph)


    buys = get_elements(ownership_xpath.format("Number of Buys"))
    sells = get_elements(ownership_xpath.format("Number of Sells"))
    totalinsider = get_elements(ownership_xpath.format("Total Insider Trades"))


    syma = []
    syma.append(str(symbol))
    print(syma)

    buys3m = buys[:1]
    buys12m = buys[1:]
    #print(buys3m)
    #print(buys12m)
    
    sellsthrm = []
    sellsthrm.append(sells[:1])
    #print(sellsthrm)
    
    sellstwlm = []
    sellstwlm.append(sells[1:])
    #print(sellstwlm)

    activitythrm = []
    activitythrm.append(monthactivity[:1])
    #print(activitythrm)

    activitytwlm = []
    activitytwlm.append(monthactivity[1:])
    #print(activitytwlm)

    allactivitylst = activity[:1]
    #print(allactivitylst)

    df15=pd.DataFrame(syma, columns=['Symbol'])
    df16=pd.DataFrame(buys3m,columns=['Buys3m'])
    df18=pd.DataFrame(sellsthrm, columns=['Sells3m'])
    df20=pd.DataFrame(activitythrm, columns=['NetActvity3mInsiders'])
    df17=pd.DataFrame(buys12m, columns=['Buys12m'])
    df19=pd.DataFrame(sellstwlm, columns=['Sells12m'])
    df21=pd.DataFrame(activitytwlm, columns=['NetActivity12mInsiders'])
    df22=pd.DataFrame(allactivitylst, columns=['NetActivityAll'])

    dftempa=pd.concat([df15,df16,df18, df20, df17, df19, df21, df22], axis = 1)
    dfinsider=dfinsider.append(dftempa)

    #print(buys)
    #print(sells)
    #print(totalinsider)

driver.quit()
 
## create a csv file in our working directory with our scraped data
dfshortinterest.to_csv("nasdaq.csv", index=False)
dfholders.to_csv("holder.csv", index=False)
dfinsts.to_csv("institution.csv", index=False)
dfinsider.to_csv("insider.csv", index=False)

