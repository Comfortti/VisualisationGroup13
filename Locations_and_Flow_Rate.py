import folium
import requests
import pandas as pd

# Load the CSV file
demand_data = pd.read_csv("demanddata2009_2024_A.csv")

# Filter data for the year 2024
demand_data_2024 = demand_data[demand_data["SETTLEMENT_DATETIME"].str.startswith("2024")]

# Convert values to numeric and replace non-convertible values with NaN
demand_data_2024 = demand_data_2024.apply(pd.to_numeric, errors='coerce')

# Calculate the mean using absolute numbers 
route_averages_2024 = demand_data_2024.abs().mean(axis=0)

# Co-ordinates for the Interconnectors
routes = [
    ("IFA_FLOW", (50.696667, 1.639167), (51.105833, 0.975556)),
    ("IFA2_FLOW", (50.818056, -1.193889), (49.110806, -0.261444)),
    ("BRITNED_FLOW", (51.440000, 0.716667), (51.957500, 4.021389)),
    ("MOYLE_FLOW", (55.446944, -4.431111), (54.842778, -5.769722)),
    ("EAST_WEST_FLOW", (53.227222, -3.072778), (53.471111, -6.567500)),
    ("NEMO_FLOW", (51.31, 1.346111), (51.3189, 3.2069)),
    ("NSL_FLOW", (59.5166, 6.6358), (55.1270, -1.5103)),
    ("ELECLINK_FLOW", (51.098389, 1.144694), (50.920194, 1.780611)),
    ("VIKING_FLOW", (55.523056, 8.709722), (52.930278, -0.220556))
]

# Create a Folium map centered on Western Europe 
m = folium.Map(location=[51.1657, 10.4515], zoom_start=5, tiles=None)

# Get GeoJSON data
url = "http://geojson.xyz/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson"
map_units_geojson = requests.get(url).json()

# Plot the map units on the map
folium.GeoJson(map_units_geojson).add_to(m)

# Add revelant markers 
folium.Marker(location=[53.978439, -2.205004], icon=folium.DivIcon(html='<div style="font-size: 12; color: black;">United Kingdom</div>')).add_to(m) # London, United Kingdom
folium.Marker(location=[53.211575, -8.044749], icon=folium.DivIcon(html='<div style="font-size: 12; color: black;">Ireland</div>')).add_to(m) # Dublin, Ireland
folium.Marker(location=[47.501189, 2.458180], icon=folium.DivIcon(html='<div style="font-size: 12; color: black;">France</div>')).add_to(m) # Paris, France
folium.Marker(location=[56.0257765, 8.495680], icon=folium.DivIcon(html='<div style="font-size: 12; color: black;">Denmark</div>')).add_to(m) # Copenhagen, Denmark
folium.Marker(location=[60.472, 8.4689], icon=folium.DivIcon(html='<div style="font-size: 12; color: black;">Norway</div>')).add_to(m) # Oslo, Norway
folium.Marker(location=[50.665775, 4.215993], icon=folium.DivIcon(html='<div style="font-size: 12; color: black;">Belgium</div>')).add_to(m) # Brussels, Belgium
folium.Marker(location=[52.182884, 4.631239], icon=folium.DivIcon(html='<div style="font-size: 12; color: black;">Netherlands</div>')).add_to(m) # Amsterdam, Netherlands

# Create a dictionary to store route averages for 2024
route_avg_dict_2024 = {label: route_averages_2024[label] for label, _, _ in routes}

# Sort the routes based on desc average for 2024
sorted_routes_2024 = sorted(routes, key=lambda x: route_avg_dict_2024[x[0]], reverse=True)

# Plot the thickness of routtes according to mean data 
for label, start, end in sorted_routes_2024:
    route_avg_2024 = route_avg_dict_2024[label]
    line_weight_2024 = 1 + 0.5 * (sorted(routes, key=lambda x: route_avg_dict_2024[x[0]]).index((label, start, end)) + 1)
    popup_text_2024 = f'<b>{label}</b><br>Average Electricity Generated (MW): {route_avg_2024:.2f}'
    folium.PolyLine(locations=[start, end], color='red', weight=line_weight_2024, popup=folium.Popup(popup_text_2024, sticky=True)).add_to(m)

# Save the map to an HTML file
m.save('interconnector_flow_2024.html')