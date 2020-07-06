# bustime-display

A GUI stop monitoring app using the [MTA's Bus Time API](https://bustime.mta.info/wiki/Developers/Index) and [Twilio's SMS API](https://www.twilio.com/sms/api)

## How it works
![bustime-display_demo](https://user-images.githubusercontent.com/46148388/86545132-b5d5a380-befa-11ea-93ed-4ac2e0558dd1.gif) *2x Speed*

The app takes visual inspiration from the Public Address Customer Information Screens or "countdown clocks" commonly found in New York City Subway stations.

### Display
There are two panels, each displaying real-time Bus Time information for two different buses. The top panel always displays the closest bus while the lower panel cycles through the remaining buses. When a bus is approaching the monitored stop, the text color for its information will turn purple and once it is at the stop, the text color will turn red orange. The app updates its Bus Time information every 5 seconds.

### Notifications
To set a notification, simply click on the panel containing the information for the bus of which you wish to be notified near its arrival. Once the bus is 5 minutes away or less, an SMS message will be sent to your phone notifying you of your bus's arrival time.

## Running

You need:
- Python 3.8.3
- [MTA Bus Time API Key](https://bustime.mta.info/wiki/Developers/Index)
- [Twilio account](https://www.twilio.com/try-twilio) credentials and phone number
- Phone number capable of receiving SMS messages

You must have these environment variables set up first:
- **BUSTIME_API_KEY** – your MTA Bus Time API Key
- **TWILIO_ACCOUNT_SID** – your Twilio account SID
- **TWILIO_AUTH_TOKEN** – your Twilio account auth token
- **TWILIO_PHONE_NUMBER** – your Twilio phone number
- **MY_PHONE_NUMBER** – your SMS capable phone number

To start the app, simply run the `bustime_display/bustime_display.py` file using Python:

```fish
~/bustime-display $ python bustime_display/bustime_display.py
```
