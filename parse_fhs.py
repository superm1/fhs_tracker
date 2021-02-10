#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from secrets import uri
import paho.mqtt.client as mqttClient
import time
import datetime


def send_mqtt(value):
    from secrets import user, password, broker_address, port


    client = mqttClient.Client("FHS Tracker")
    client.username_pw_set(user, password=password)
    client.connect(broker_address, port=port)
    client.publish("fhs_tracker/spot_available", value)
    client.disconnect()


def get_page_alert(driver):
    element = driver.find_element_by_tag_name("iframe")
    driver.switch_to.frame(element)
    time.sleep(10)  # wait 10 seconds for page to finish the load
    spots_available=True
    alert = None
    try:
        alert = driver.find_element_by_class_name("alert")
    except NoSuchElementException:
        print("No alert found")
    if alert and alert.is_displayed():
        if 'No services were set up' in alert.text or\
           'No services in this location' in alert.text:
            spots_available=False
        else:
            print(alert.text)
    return spots_available


chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

driver.get(uri)
while True:
    value = get_page_alert(driver)
    send_mqtt(value)
    print("Sent %d at %s" % (value, datetime.datetime.now()))
    time.sleep(58 * 60)  # 58 minutes
    driver.refresh()
