import json
import urllib.request
import urllib.parse
from datetime import datetime
from os import getenv
from collections import namedtuple

BusTime = namedtuple('BusTime', 'estimated_wait_time, stops_from_call, presentable_distance')

BUSTIME_API_KEY = getenv("BUSTIME_API_KEY")

def stop_monitor_data(stop_id, line_ref):
    """
    Gets stop monitor JSON data from the MTA Bus Time API.

    Args:
        stop_id (int): The bus stop id number.
        line_ref (str): The bus line identifier.

    Returns:
        dict: The deserialized stop monitor JSON data
    """

    params = urllib.parse.urlencode({'key' : BUSTIME_API_KEY,
                                     'OperatorRef' : 'MTA',
                                     'MonitoringRef' : stop_id,
                                     'LineRef' : line_ref})

    url = "http://bustime.mta.info/api/siri/stop-monitoring.json?%s" % params

    with urllib.request.urlopen(url) as response:
        source = response.read()

    return json.loads(source)

def dump_json_to_file(json_data, filename):
    with open(filename, 'w') as f:
        json.dump(json_data, f, indent=2)

def bus_times(stop_monitor_data):
    """
    Gets estimated wait times and distances for buses serving a stop.

    Args:
        stop_monitor_data (dict): The deserialized stop monitor JSON data.

    Returns:
        list: A list of BusTime namedtuples contaning the wait times and
        distances for each bus.
    """

    fixtures = []
    for bus in stop_monitor_data['Siri']['ServiceDelivery']['StopMonitoringDelivery'][0]['MonitoredStopVisit']:
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

            fixtures.append(BusTime(estimated_wait_time, stops_from_call, presentable_distance))

        else:
            fixtures.append(BusTime(None, stops_from_call, presentable_distance))

    return fixtures

def print_bus_times(bus_times):
    """
    Prints estimated wait times and distances for buses.

    Args:
        bus_times ([BusTime]): The list of BusTime namedtuples contaning
        the wait times and distances of each bus.

    Returns:
        None.
    """

    for bus_time in  bus_times:
        estimated_wait_time = bus_time.estimated_wait_time
        if estimated_wait_time is not None:
            print("%d %s, %d %s away, %s" % (estimated_wait_time,
                                             "minute" if estimated_wait_time == 1 else "minutes",
                                             bus_time.stops_from_call,
                                             "stop" if bus_time.stops_from_call == 1 else "stops",
                                             bus_time.presentable_distance))
        else:
            print("%d %s away" % (bus_time.stops_from_call,
                                  "stop" if bus_time.stops_from_call == 1 else "stops",
                                  bus_time.presentable_distance))

if __name__ == '__main__':
    data = stop_monitor_data(503991, 'MTABC_Q39')
    dump_json_to_file(data, 'stop_monitor.json')

    # with open("sample_stop_monitor.json", 'r') as f:
    #     data = json.load(f)

    fixtures = bus_times(data)
    print_bus_times(fixtures)
