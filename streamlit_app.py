import streamlit as st

st.title("Environmental Justice Index Visualization (NM)")
st.write("The EJI is a value representing a percentile ranking relative to communities nationwide.")
st.write("The value shows the percentage of the nation which this")
# perameter1 is to view the eji of that, so EJI of County or EJI of New Mexico

counties = [
"Bernalillo County", "Chaves County", "Cibola County", "Curry County",
"Doña Ana County", "Eddy County", "Grant County", "Lincoln County",
"Luna County", "McKinley County", "Mora County", "Otero County",
"Rio Arriba County", "Sandoval County", "San Juan County", "San Miguel County",
"Santa Fe County", "Sierra County", "Taos County", "Valencia County",
"Catron County", "Hidalgo County", "Los Alamos County", "Colfax County",
"Lea County", "Socorro County", "Torrance County", "Guadalupe County",
"Harding County", "Roosevelt County", "De Baca County", "Quay County",
"Union County"
]

states = [
"Alabama",    "Arizona",    "Alaska",    "Arkansas",
"California",    "Colorado",    "Florida",    "Connecticut",
"Delaware",    "Texas",    "Washington",    "West Virginia",
"Wisconsin",    "District of Columbia",    "Georgia",    "Virginia",
"Illinois",    "Hawaii",    "Indiana",    "Idaho",
"Kentucky",    "Iowa",    "Maine",    "Maryland",
"Wyoming",    "American Samoa",    "Guam",    "Commonwealth of the Northern Mariana Islands",
"Kansas",    "Puerto Rico",    "Louisiana",    "Massachusetts",
"Michigan",    "Minnesota",    "Mississippi",    "Missouri",
"Nevada",    "New Hampshire",    "Montana",    "Nebraska",
"New Jersey",    "New Mexico",    "New York",    "North Carolina",
"Ohio",    "Pennsylvania",    "North Dakota",    "Oklahoma",
"Oregon",    "Rhode Island",    "South Carolina",    "Tennessee",
"South Dakota",    "Utah",    "Vermont",    "United States Virgin Islands"
]

perameter1 = ["County", "New Mexico"]
selected_perameter1 = st.selectbox("View EJI Dataset of:", perameter1)
st.write(f"You selected {selected_perameter1} vs United States")
if selected_perameter1 == "County":
	selected_County1 = st.selectbox("Select a New Mexico County:", counties)

elif selected_parameter1 == "New Mexico":
	

	
	
else: selected_parameter1 == "Nothin"

	
