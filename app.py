# import libraries 
import yahoo_fin.stock_info as si
import streamlit as st
import pandas as pd 
import base64
from datetime import datetime, timedelta
from app_functions import convert_df

st.title("US Stock Market Historical Data")

# ask user which stock they would like to pull historical data for
ticker = st.text_input("Enter the stock ticker symbol (e.g. AAPL for Apple Inc.)")

# add user input for selecting historical timeframe 
end_date = st.date_input("Select the end date:", value=datetime.now())

st.info('If you want to include the current day prices in the dataset, you will need to enter tomorrows date! (Example: Todays date is 3/27/2023 and I want the prices of today to be included in my dataset. Enter 3/28/2023 in the "end date" section)', icon="💡")

start_date = st.date_input("Select the start date:", value=end_date - timedelta(days=365*10))

if st.button("Submit"):
    data = si.get_data(ticker, start_date=start_date, end_date=end_date)
  
    # Data Cleaning
    data = data.reset_index()
    data = data.drop(columns=['ticker'], axis=1)
    data = data.rename(columns={'index': 'Date', 'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'adjclose': 'Adj Close', 'volume': 'Volume'})
    
    data = data.set_index('Date')

    # Print the column names in the data frame :: TEST
    print(f"Column names for {ticker}: {data.columns}")

    # Specify the column order
    columns = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    
    # Print line chart
    st.markdown(f"##### {ticker.upper()} Historical Closing Prices")
    st.line_chart(data['Close'])

    df = pd.DataFrame(data)

    #converting the sample dataframe
    csv, json = convert_df(df)

    # adding a download button to download csv file
    st.download_button( 
        label="Download data as CSV",
        data=csv,
        file_name= ticker.upper() + '_historical_data.csv',
        mime='text/csv',
    )

    st.download_button(
        label="Download data as JSON",
        data=json,
        file_name= ticker.upper() + '_historical_data.json',
        mime='application/json',
    )

