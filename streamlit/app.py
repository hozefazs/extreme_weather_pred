import streamlit as st

def main():
    st.title("Weather Data Input")

    # First line of inputs
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        dew = st.text_input("Dew")
    with col2:
        humidity = st.text_input("Humidity")
    with col3:
        cloudcover = st.text_input("Cloud Cover")
    with col4:
        precipcover = st.text_input("Precipitation Cover")
    with col5:
        sealevelpressure = st.text_input("Sea Level Pressure")

    # Second line of inputs
    col6, col7, col8, col9, col10 = st.columns(5)

    with col9:
        solarenergy = st.text_input("Solar Energy")
    with col10:
        solarradiation = st.text_input("Solar Radiation")
    with col6:
        sunrise = st.text_input("Sunrise")
    with col7:
        sunset = st.text_input("Sunset")
    with col8:
        uvindex = st.text_input("UV Index")

    # Third line of inputs
    col11, col12, col13, col14 = st.columns(4)

    with col11:
        visibility = st.text_input("Visibility")
    with col12:
        winddir = st.text_input("Wind Direction")
    with col13:
        windgust = st.text_input("Wind Gust")
    with col14:
        windspeed = st.text_input("Wind Speed")

    st.write("Dew:", dew)
    st.write("Humidity:", humidity)
    st.write("Cloud Cover:", cloudcover)
    st.write("Precipitation Cover:", precipcover)
    st.write("Sea Level Pressure:", sealevelpressure)
    st.write("Solar Energy:", solarenergy)
    st.write("Solar Radiation:", solarradiation)
    st.write("Sunrise:", sunrise)
    st.write("Sunset:", sunset)
    st.write("UV Index:", uvindex)
    st.write("Visibility:", visibility)
    st.write("Wind Direction:", winddir)
    st.write("Wind Gust:", windgust)
    st.write("Wind Speed:", windspeed)

if __name__ == "__main__":
    main()
