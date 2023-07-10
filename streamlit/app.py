import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def main():
    st.title("Changing Lives - Predicting Extreme Weather")
    st.markdown("""Please select the date for which you would like to predict extreme weather.
                   \nIt will autofill the values below. 
                   \nIf you would like to choose a date not in the list, 
                   you may custom fill the values below""" )
    # Generate a range of dates
    start_date = datetime(2023, 2, 5).date()
    end_date = datetime(2023, 7, 22).date()
    delta = timedelta(days=1)
    date_range = []
    current_date = start_date
    while current_date <= end_date:
        date_range.append(current_date)
        current_date += delta

    # Dropdown selector for date
    selected_date = st.selectbox("Select Date", date_range)
    
    # First line of inputs
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        dew_placeholder = st.empty()
        dew = dew_placeholder.text_input("Dew")
    with col2:
        humidity_placeholder = st.empty()
        humidity = humidity_placeholder.text_input("Humidity")
    with col3:
        cloudcover_placeholder = st.empty()
        cloudcover = cloudcover_placeholder.text_input("Cloud Cover")
    with col4:
        precipcover_placeholder = st.empty()
        precipcover = precipcover_placeholder.text_input("Precipitation Cover")
    with col5:
        sealevelpressure_placeholder = st.empty()
        sealevelpressure = sealevelpressure_placeholder.text_input("Sea Level Pressure")

    # Second line of inputs
    col6, col7, col8, col9, col10 = st.columns(5)

    with col9:
        solarenergy_placeholder = st.empty()
        solarenergy = solarenergy_placeholder.text_input("Solar Energy")
    with col10:
        solarradiation_placeholder = st.empty()
        solarradiation = solarradiation_placeholder.text_input("Solar Radiation")
    with col6:
        sunrise_placeholder = st.empty()
        sunrise = sunrise_placeholder.text_input("Sunrise")
    with col7:
        sunset_placeholder = st.empty()
        sunset = sunset_placeholder.text_input("Sunset")
    with col8:
        uvindex_placeholder = st.empty()
        uvindex = uvindex_placeholder.text_input("UV Index")

    # Third line of inputs
    col11, col12, col13, col14 = st.columns(4)

    with col11:
        visibility_placeholder = st.empty()
        visibility = visibility_placeholder.text_input("Visibility")
    with col12:
        winddir_placeholder = st.empty()
        winddir = winddir_placeholder.text_input("Wind Direction")
    with col13:
        windgust_placeholder = st.empty()
        windgust = windgust_placeholder.text_input("Wind Gust")
    with col14:
        windspeed_placeholder = st.empty()
        windspeed = windspeed_placeholder.text_input("Wind Speed")

    name_of_file = 'Dallas_Texas_2019-01-01_to_2023-07-22'
    test_dates_df = pd.read_csv(f"data/test_{name_of_file}_w_index.csv")
    if selected_date:
        value_df = test_dates_df.query(f"datetime == '{selected_date}'")
        dew = dew_placeholder.text_input("Dew", value =list(value_df['dew'].loc[:])[0])
        humidity = humidity_placeholder.text_input("Humidity", value =list(value_df['humidity'].loc[:])[0])
        cloudcover = cloudcover_placeholder.text_input("Cloud Cover", value =list(value_df['cloudcover'].loc[:])[0])
        precipcover = precipcover_placeholder.text_input("Precipitation Cover", value =list(value_df['precipcover'].loc[:])[0])
        sealevelpressure = sealevelpressure_placeholder.text_input("Sea Level Pressure", value =list(value_df['sealevelpressure'].loc[:])[0])
        solarenergy = solarenergy_placeholder.text_input("Solar Energy", value =list(value_df['solarenergy'].loc[:])[0])
        solarradiation = solarradiation_placeholder.text_input("Solar Radiation", value =list(value_df['solarradiation'].loc[:])[0])
        sunrise = sunrise_placeholder.text_input("Sunrise", value =list(value_df['sunrise'].loc[:])[0])
        sunset = sunset_placeholder.text_input("Sunset", value =list(value_df['sunset'].loc[:])[0])
        uvindex = uvindex_placeholder.text_input("UV Index", value =list(value_df['uvindex'].loc[:])[0])
        visibility = visibility_placeholder.text_input("Visibility", value =list(value_df['visibility'].loc[:])[0])
        winddir = winddir_placeholder.text_input("Wind Direction", value =list(value_df['winddir'].loc[:])[0])
        windgust = windgust_placeholder.text_input("Wind Gust", value =list(value_df['windgust'].loc[:])[0])
        windspeed = windspeed_placeholder.text_input("Wind Speed", value =list(value_df['windspeed'].loc[:])[0])

    if st.button("Predict Temperatures"):
        import urllib
        import google.cloud.aiplatform as aiplatform
        from google.cloud import bigquery
        import os
        PROJECT_ID = "tidal-plasma-387718"
        REGION = "europe-west1"
        BUCKET_URI = f"gs://vertex_ai_ackathon_staging"
        aiplatform.init(project=PROJECT_ID, staging_bucket=BUCKET_URI)
        MODEL_TEMPMAX = "4304429693068640256"
        MODEL_TEMPMIN = "5224852866912485376"
        model_max = aiplatform.Model(
                model_name = MODEL_TEMPMAX ,
                project= PROJECT_ID,
                location= REGION)
        model_min = aiplatform.Model(
                model_name = MODEL_TEMPMIN ,
                project= PROJECT_ID,
                location= REGION)
        model_evaluations_max = model_max.list_model_evaluations()
        model_evaluations_min = model_min.list_model_evaluations()
        for model_evaluation in model_evaluations_max:
            print(model_evaluation.to_dict())
        for model_evaluation in model_evaluations_min:
            print(model_evaluation.to_dict())
            
        batch_predict_bq_output_dataset_name_max = f"hackathon_vertex_ai_predictions_{MODEL_TEMPMAX}"
        batch_predict_bq_output_dataset_path_max = "{}.{}".format(
            PROJECT_ID, batch_predict_bq_output_dataset_name_max
        )
        batch_predict_bq_output_uri_prefix_max = "bq://{}.{}".format(
            PROJECT_ID, batch_predict_bq_output_dataset_name_max
        )
        # Must be the same region as batch_predict_bq_input_uri
        client_max = bigquery.Client(project=PROJECT_ID)
        bq_dataset_max = bigquery.Dataset(batch_predict_bq_output_dataset_path_max)
        dataset_region_max = REGION  # @param {type : "string"}
        bq_dataset_max.location = dataset_region_max
        client_max.delete_dataset(bq_dataset_max, delete_contents=True, not_found_ok=True)
        bq_dataset_max = client_max.create_dataset(bq_dataset_max)
        print(
            "Created bigquery dataset {} in {}".format(
                batch_predict_bq_output_dataset_path_max, dataset_region_max
            )
        ) 
        
        batch_predict_bq_output_dataset_name_min = f"hackathon_vertex_ai_predictions_{MODEL_TEMPMIN}"
        batch_predict_bq_output_dataset_path_min = "{}.{}".format(
            PROJECT_ID, batch_predict_bq_output_dataset_name_min
        )
        batch_predict_bq_output_uri_prefix_min = "bq://{}.{}".format(
            PROJECT_ID, batch_predict_bq_output_dataset_name_min
        )
        # Must be the same region as batch_predict_bq_input_uri
        client_min = bigquery.Client(project=PROJECT_ID)
        bq_dataset_min = bigquery.Dataset(batch_predict_bq_output_dataset_path_min)
        dataset_region_min = REGION  # @param {type : "string"}
        bq_dataset_min.location = dataset_region_min
        client_min.delete_dataset(bq_dataset_min, delete_contents=True, not_found_ok=True)
        bq_dataset_min = client_min.create_dataset(bq_dataset_min)
        print(
            "Created bigquery dataset {} in {}".format(
                batch_predict_bq_output_dataset_path_min, dataset_region_min
            )
        ) 
        
        import pandas_gbq
        sql_max = f"""
            SELECT * FROM 
            `tidal-plasma-387718.hackathon_vertex_ai.automl_3_hor_sel_fea_Dallas_Texas_2019-01-01_to_2023-07-22_test1` 
            WHERE datetime = '{selected_date}'
            """
        sql_min = f"""
            SELECT * FROM 
            `tidal-plasma-387718.hackathon_vertex_ai.test_s2s_3_hor_sel_fea_tempmin_Dallas` 
            WHERE datetime = '{selected_date}'
            """
        temp_max_df = pandas_gbq.read_gbq(sql_max, project_id=PROJECT_ID)
        temp_min_df = pandas_gbq.read_gbq(sql_min, project_id=PROJECT_ID)

        col15, col16 = st.columns(2)

        with col15:
            actual_max_placeholder = st.empty()
            actual_max = actual_max_placeholder.text_input("Actual Max Temperature", value =list(temp_max_df['tempmax'].loc[:])[0])
        with col16:
            actual_min_placeholder = st.empty()
            actual_min = actual_min_placeholder.text_input("Actual Min Temperature", value =list(temp_min_df['tempmin'].loc[:])[0]) 
            
        col17, col18 = st.columns(2)

        with col17:
            pred_max_placeholder = st.empty()
            pred_max = pred_max_placeholder.text_input("Predicted Max Temperature", value =round(list(temp_max_df["predicted_tempmax"].loc[:])[0]['value'],2))
        with col18:
            pred_min_placeholder = st.empty()
            pred_min = pred_min_placeholder.text_input("Predicted Min Temperature", value =round(list(temp_min_df["predicted_tempmin"].loc[:])[0]['value'],2))     
            
        prompt = f"""Below are going to be pasted for a given area, the temperatures t_max and t_min for a given prediction.

        With these temperatures that are continuous values, the agent is going to provide with recommendations and warnings.

        For these warnings and recommendations, the agent should remember the following general rules:
        1. t_min below 0 Fahrenheit is considered as cold and is going to cause the water to freeze
        2. t_min below -10 Fahrenheit and lower is considered extreme
        3. t_max above 75 Fahrenheit is considered above average
        4. t_max above 100 Fahrenheit is considered extremely hot 

        The agent should mention the temperatures as well.
        The predicted t_max is {round(list(temp_max_df["predicted_tempmax"].loc[:])[0]['value'],2)} and predicted t_min is {round(list(temp_min_df["predicted_tempmin"].loc[:])[0]['value'],2)}"""
        url = "http://10.132.0.3:8507/chat?human_msg=" + prompt
        print(prompt)
        # try:
        import requests
        response = requests.post(url)
        print(response.json())
        # except:
        #     print('error occurred')
        st.markdown("Google PALM suggests")
        st.markdown(response.json()["response"])
            
if __name__ == "__main__":
    main()
