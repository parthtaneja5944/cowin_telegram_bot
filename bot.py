
import requests 
from datetime import datetime
import time
import schedule

base_cowin_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
now = datetime.now()
today_date = now.strftime("%d-%m-%Y")
api_url_telegram ="https://api.telegram.org/bot5078357040:AAE977X16FE4Y3864AIQ1o_bMIUPqE_Tf64/sendMessage?chat_id=@__groupid__&text="
group_id = "demo_telegram_cowin2"
delhi_district_ids = [140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150]


def fetch_data_from_cowin(district_id):
    query_params = "?district_id={}&date={}".format(district_id, today_date)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    final_url = base_cowin_url+query_params
    response = requests.get(final_url, headers=headers)
    extract_availability_data(response)
  
    
def fetch_data_for_state(district_ids):
    for district_id in district_ids:
        fetch_data_from_cowin(district_id)
        
def extract_availability_data(response):
    response_json = response.json()
    i = 0
    for center in response_json["centers"]:
        i = i + 1
        if i > 5:
            break
        message = ""
        for session in center["sessions"]:
            if session["available_capacity_dose1"] > 0 and session["min_age_limit"]==18:
                message += "Pincode: {} \nName: {} \nSlots: {} \nDate: {} \nVaccine: {} \nFee Type: {} \nMinimum Age: {} \n**********************\n".format(
                    center["pincode"], center["name"],
                    session["available_capacity_dose1"], 
                    session["date"],
                    session["vaccine"], 
                    center["fee_type"],
                    session["min_age_limit"]
                )
        print(message)
        send_message_telegram(message)


                    
def send_message_telegram(message):
    final_telegram_url = api_url_telegram.replace("__groupid__", group_id)
    final_telegram_url = final_telegram_url + message
    response = requests.get(final_telegram_url)
    print(response)
    
if __name__ == "__main__": 
    schedule.every(10).seconds.do(lambda: (fetch_data_for_state(delhi_district_ids)))
    while True:
        schedule.run_pending()
        time.sleep(1)
    