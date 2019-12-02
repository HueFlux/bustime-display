import json
import urllib.request
import urllib.parse
from datetime import datetime
from os import getenv
from collections import namedtuple

BusTime = namedtuple('BusTime', 'line_name, destination_name, estimated_wait_time, stops_from_call, presentable_distance')

BUSTIME_API_KEY = getenv('BUSTIME_API_KEY')

def stop_monitor_data(stop_id, line_ref=''):
    """
    Gets stop monitor JSON data from the MTA Bus Time API.

    Args:
        stop_id (int): The bus stop id number.
        line_ref (str, optional): The bus line identifier.
            Defaults to empty string.

    Returns:
        dict: The deserialized stop monitor JSON data
    """

    params = urllib.parse.urlencode({'key' : BUSTIME_API_KEY,
                                     'OperatorRef' : 'MTA',
                                     'MonitoringRef' : stop_id})

    url = f"http://bustime.mta.info/api/siri/stop-monitoring.json?{params}"

    if line_ref:
        url = url + f"&LineRef={line_ref}"

    with urllib.request.urlopen(url) as response:
        source = response.read()

    return json.loads(source)

def extract_bus_times(stop_monitor_data):
    """
    Gets estimated wait times and distances for buses
    from stop monitor JSON data.

    Args:
        stop_monitor_data (dict): The deserialized stop monitor JSON data.

    Returns:
        list: A list of BusTime namedtuples contaning the wait times and
        distances for each bus.
    """

    fixtures = [] # List to hold BusTimes

    for bus in stop_monitor_data['Siri']['ServiceDelivery']['StopMonitoringDelivery'][0]['MonitoredStopVisit']:

        expected_arrival_time = bus['MonitoredVehicleJourney']['MonitoredCall'].get('ExpectedArrivalTime')

        if not expected_arrival_time:
            continue

        expected_arrival_time = datetime.fromisoformat(expected_arrival_time)
        current_time = datetime.now(expected_arrival_time.tzinfo)
        # Calculate wait time in minutes
        estimated_wait_time = (expected_arrival_time - current_time).seconds // 60

        stops_from_call = bus['MonitoredVehicleJourney']['MonitoredCall']['Extensions']['Distances']['StopsFromCall']

        line_name = bus['MonitoredVehicleJourney']['PublishedLineName']
        destination_name = bus['MonitoredVehicleJourney']['DestinationName']

        presentable_distance = bus['MonitoredVehicleJourney']['MonitoredCall']['Extensions']['Distances']['PresentableDistance']

        # Add BusTime to fixtures
        fixtures.append(BusTime(line_name, destination_name, estimated_wait_time, stops_from_call, presentable_distance))

    return fixtures

def bus_times(stop_id, line_ref='', dump_json=False):
    """
    Gets estimated wait times and distances for buses serving a stop.

    Args:
        stop_id (int): The bus stop id number.
        line_ref (str, optional): The bus line identifier.
            Defaults to empty string.
        dump_json (bool): Determines whether or not to dump the
            stop monitor JSON data into a file named 'stop_monitor.json'.
            Defaults to False.

    Returns:
        list: A list of BusTime namedtuples contaning the wait times and
        distances for each bus.
    """

    data = stop_monitor_data(stop_id, line_ref)

    if dump_json:
        with open('stop_monitor.json', 'w') as f:
            json.dump(data, f, indent=2)

    return extract_bus_times(data)

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
            print("%s to %s: %d %s, %d %s away, %s" % (bus_time.line_name,
                                                       bus_time.destination_name,
                                                       estimated_wait_time,
                                                       "minute" if estimated_wait_time == 1 else "minutes",
                                                       bus_time.stops_from_call,
                                                       "stop" if bus_time.stops_from_call == 1 else "stops",
                                                       bus_time.presentable_distance))
        else:
            print("%s to %s: %d %s away, %s" % (bus_time.line_name,
                                                bus_time.destination_name,
                                                bus_time.stops_from_call,
                                                "stop" if bus_time.stops_from_call == 1 else "stops",
                                                bus_time.presentable_distance))

if __name__ == '__main__':
    from operator import attrgetter
    q39_fixtures = bus_times(503991, dump_json=True)
    q67_fixtures = bus_times(505168, 'MTABC_Q67')
    fixtures = sorted(q39_fixtures + q67_fixtures, key=attrgetter('estimated_wait_time'))
    print_bus_times(fixtures)
