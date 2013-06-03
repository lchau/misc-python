#!/usr/bin/env python

from datetime import datetime
import math
import time

def main():
  get_option = ""
  while (get_option != 'q'):
    get_option = raw_input("""
    1. Top 100 Magnitude Earthquakes
    2. Top 50 Shallowest Earthquakes
    3. Top 50 Earthquakes closest to Cheney,WA
    4. Mean, Midpoint, Median and Standard Deviation of Earthquake Magnitude
    5. Top 50 Earthquakes by Impact
    Q. Exit

Select an option: """)
    if get_option.lower() == 'q':
      return
    elif get_option == "1":
      print "Top 100 Magnitude Earthquakes (date, magnitude, depth)"
      for x in sort("magnitude", count=100):
        print "%s %.2f %d" % (x["date"], x["magnitude"], x["depth"])
    elif get_option == "2":
      print "Top 50 Shallowest Earthquakes (date, magnitude, depth)"
      for x in sort("depth", count=50, asc=True):
        print "%s %.2f %d" % (x["date"], x["magnitude"], x["depth"])
    elif get_option == "3":
      print "Top 50 Earthquakes closest to Cheney, WA (date, coordinates, distance from Cheney)"
      for x in sort("distance_from_cheney", count=50, asc=True):
        print "%s %s %.2f" % (x["date"], str(x["coordinates"]), x["distance_from_cheney"])
    elif get_option == "4":
      print """
      mean: %.2f
    median: %.2f
  std. dev: %.2f""" % statistics(all_magnitudes)
    elif get_option == "5":
      print "Top 50 Earthquakes by Impact (date, magnitude, depth, impact"
      for x in sort("impact", count=50):
        print "%s %.2f %d %.2f" % (x["date"], x["magnitude"], x["depth"], x["impact"])

def to_record(s, all_magnitudes):

  def date(s):
    s[3] = s[3].zfill(6)
    date_str = "%s,%s,%s,%s" % (s[0], s[1], s[2], s[3])

    if "." in date_str:
      date_str = time.strptime(date_str, "%Y,%m,%d,%H%M%S.%f")
    else:
      date_str = time.strptime(date_str, "%Y,%m,%d,%H%M%S")
    return datetime.fromtimestamp(time.mktime(date_str))

  def getDistanceFromLatLonInKm(lat1,lon1,lat2,lon2):
    R = 6371
    dLat = deg2rad(lat2-lat1)
    dLon = deg2rad(lon2-lon1)
    a = \
        math.sin(dLat/2) * math.sin(dLat/2) + \
        math.cos(deg2rad(lat1)) * math.cos(deg2rad(lat2)) * \
        math.sin(dLon/2) * math.sin(dLon/2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d

  def deg2rad(deg):
    return deg * (math.pi/180)

  s = s.strip().split(",")
  if len(s) != 9:
    return None

  x1, y1 = (47.4875, 117.5747)
  x2, y2 = (float(s[4]), float(s[5]))

  depth = int(s[7]) if len(s[7]) > 0 else 0
  magnitude = float(s[6])
  all_magnitudes.append(magnitude)

  impact = max(0, (1000 - depth) * magnitude)

  return {
    "date" : str(date(s)),
    "coordinates" : (x2, y2),
    "magnitude" : magnitude,
    "depth" : depth,
    "source" : s[8],
    "distance_from_cheney" : getDistanceFromLatLonInKm(x1, x2, y1, y2),
    "impact" : impact
  }

def sort(key_name, count=50, asc=False):
  # desc = False, asc = True
  direction = False if asc else True
  key_name = key_name.lower()
  data.sort(key=lambda x: x[key_name], reverse=direction)
  return data[:count]

def statistics(elements):
  elements = sorted(elements)
  size = len(elements)

  def mean(elements):
    return sum(elements) / size

  def median(elements):
    midpoint = int((1 + (size - 1)) / 2)
    if len(elements) % 2 == 0:
      return (elements[midpoint] + elements[midpoint - 1]) / 2.0
    return elements[midpoint / 2]

  def sd(elements):
    diff = 0.0
    average = mean(elements)
    for x in elements:
      v = math.pow(x - average, 2)
      diff += (x - average)**2
    return math.sqrt(diff / size)
  return (mean(elements), median(elements), sd(elements))

data = []
all_magnitudes = []
with open("eqdata.csv", "r") as f:
  f.readline() # skip headers
  for index, line in enumerate(f):
    #for testing
    # if index > 100:
    #   break
    record = to_record(line, all_magnitudes)
    if record:
      data.append(record)

if __name__ == '__main__':
    main()