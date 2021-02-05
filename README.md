# FHS Medical spot tracker

In order to get a shot one of the places that I'm going to be monitoring has a page to look for openings to schedule.  They ask to check back regularly, but won't actually notify you.

In order to not inconvenience myself having to manually check regularly, I've made a selenium script that can notify my home automation system [Home Assistant](https://www.home-assistant.io/) when a spot is available.

From there I can send notifications via my phone, Google Home, etc.

The script uses [Selenium](https://www.selenium.dev/) to look at the page.  Things like Scrapy and Beautiful Soup don't work because the Javascript needs to execute.
When a new result is found it's sent to my MQTT broker.

# Home Assistant changes


## Sensor
A sensor needs to be added to Home Assistant to monitor this MQTT topic. I have the script running once per hour, so I want to make sure that in case it stops running I don't have a false negative (or positive!).  That means this gets set to "Unavailable" when it expires and hasn't gotten an update.

```
sensor:
  - platform: mqtt
    name: "FHS Medical slots tracker"
    state_topic: "fhs_tracker/spot_available"
    expire_after: 3600 #make sure that we have this updated at least once per hour
```

## Automation
The automation just looks for the binary sensor change and notifies me.
```
- id: '1612508317136'
  alias: FHS Medical slots available
  description: ''
  trigger:
  - platform: state
    entity_id: sensor.fhs_medical_slots_tracker
    to: 'True'
  condition: []
  action:
  - service: notify.mobile_app_pixel_3xl
    data:
      message: FHS Medical slots appear available
  mode: single
```
