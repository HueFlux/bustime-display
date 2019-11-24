import json
import urllib.request
import urllib.parse
from datetime import datetime
from os import getenv

BUSTIME_API_KEY = getenv("BUSTIME_API_KEY")

params = urllib.parse.urlencode({'key' : BUSTIME_API_KEY,
                                 'OperatorRef' : 'MTA',
                                 'MonitoringRef' : 503991,
                                 'LineRef' : 'MTABC_Q39'})

url = "http://bustime.mta.info/api/siri/stop-monitoring.json?%s" % params

with urllib.request.urlopen(url) as response:
    source = response.read()

data = json.loads(source)

with open("stop_monitor.json", 'w') as f:
    json.dump(data, f, indent=2)

# with open("sample_stop_monitor.json", 'r') as f:
#    data = json.load(f)

for bus in data['Siri']['ServiceDelivery']['StopMonitoringDelivery'][0]['MonitoredStopVisit']:
    stops_from_call = bus['MonitoredVehicleJourney']['MonitoredCall']['Extensions']['Distances']['StopsFromCall']

    if stops_from_call > 25:
        continue

    presentable_distance = bus['MonitoredVehicleJourney']['MonitoredCall']['Extensions']['Distances']['PresentableDistance']

    expected_arrival_time = bus['MonitoredVehicleJourney']['MonitoredCall'].get('ExpectedArrivalTime')

    if expected_arrival_time is not None:

        expected_arrival_time = datetime.fromisoformat(expected_arrival_time)
        current_time = datetime.now(expected_arrival_time.tzinfo)
        # Get wait time in minutes
        estimated_wait_time = (expected_arrival_time - current_time).seconds // 60

        print("%d %s, %d %s away, %s" % (estimated_wait_time,
                                         "minute" if estimated_wait_time == 1 else "minutes",
                                         stops_from_call,
                                         "stop" if stops_from_call == 1 else "stops",
                                         presentable_distance))
    else:
        print("%d %s away" % (stops_from_call,
                              "stop" if stops_from_call == 1 else "stops"))
