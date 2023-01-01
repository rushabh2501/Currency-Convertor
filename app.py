import streamlit as st
from rates_extract import RealTimeCurrencyConverter
import numpy as np
from streamlit_folium import folium_static
import folium

@st.cache(hash_funcs={folium.folium.Map: lambda _: None}, allow_output_mutation=True)
def make_map(df):
	main_map = folium.Map(location=(39, 77), zoom_start=2)
	for row in df:
		folium.Marker(location=[float(row[-2]), float(row[-1])],
            tooltip=f"{row[-4]} - {row[-3]}: 1USD={str(row[-6])}{row[0]}",
            fill=True,
            fill_color="blue",
            color=None,
            fill_opacity=0.7,
            radius=5,
        ).add_to(main_map)
	return main_map

def app():
	rtcc = RealTimeCurrencyConverter()
	st.title("Real Time Currency Converter")
	main_map = make_map(rtcc.country_rates)
	folium_static(main_map)
	st.write('''
		Welcome to Real Time Currency Converter, here you can convert between all major currencies.
		''')
	option_from = st.selectbox("Select Country which you wish to convert:", rtcc.country_rates.T[3])
	option_to = st.selectbox("Select Country to which you wish to convert the original currency:", rtcc.country_rates.T[3])
	price = st.text_input("Enter Value Here:")
	if st.button("Convert"):
		st.write("Option From: "+option_from)
		st.write('Option To: '+option_to)
		code_from = rtcc.country_rates[np.argwhere(rtcc.country_rates.T[3]==option_from)[0][0]][0]
		index_to = np.argwhere(rtcc.country_rates.T[3]==option_to)[0][0]
		code_to = rtcc.country_rates[index_to][0]
		try:
			final_price = rtcc.convert(code_from, code_to, float(price))
			st.write("Converted Price: "+str(final_price)+" "+code_to)
		except:
			st.write("ERROR: Enter float value in price please.")
	if st.button("Refresh Rates"):
		rtcc.refresh()
	if st.button("Save Current State"):
		rtcc.save_state()
		

if __name__ == '__main__':
	app()