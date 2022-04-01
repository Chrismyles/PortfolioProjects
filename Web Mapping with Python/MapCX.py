# Import necessary libraries
import folium
import pandas
import webbrowser
import os
from geopy.geocoders import ArcGIS
webbrowser.open("file://" + os.path.realpath("MapCX.html"))

# Create the dataframe object, load the data, and create a list
data = pandas.read_csv("Covid_19_Tennessee.txt")
tc = list(data["TOTAL CASES"])
td = list(data["TOTAL DEATHS"])
ac = list(data["ACTIVE CASES"])
citycounty = list(data["CITY COUNTY"])
locator = ArcGIS()

# Create a map using Stamen Terrain, centered on study area with set zoom level
map = folium.Map(location=[35.72, -82.60], zoom_start=6, tiles="StamenTerrain")
folium.TileLayer('openstreetmap').add_to(map)
folium.TileLayer('cartodbpositron').add_to(map)

# Add a FeatureGroup to the map
fgc = folium.FeatureGroup(name="COVID_19")

# Interating through the list, using the zip function
for citycounty, tc, td, ac in zip(citycounty, tc, td, ac):
     location = locator.geocode(citycounty)
     address = location.address
     latitude = location.latitude
     longitude = location.longitude
     total_cases = (tc)
     total_deaths = (td)
     active_cases = (ac)
     popup = "%s (%s, %s) tc:%s, td:%s, ac:%s" % \
       (address, latitude, longitude, total_cases, total_deaths, active_cases)
     fgc.add_child(folium.Marker(location=[latitude, longitude],
         popup=popup, icon=folium.Icon(color='lightred')))

# Generate the map's legend
...

legend_html = '''
    <div style="position: fixed; bottom: 50px; left: 50px; width: 150px; height: 160px;
            border:2px solid grey; z-index:9999; font-size:14px;">
          COVID_19 Legend <br>
          tc = total cases   <i></i><br>
          td = total deaths  <i><br>
          ac = active cases  <i></i>
    </div>
'''

map.get_root().html.add_child(folium.Element(legend_html))
map

...

map.add_child(fgc)
map.add_child(folium.LayerControl())
map.save("MapCX.html")
