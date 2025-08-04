import streamlit as st
import pandas as pd

# Load the results table
file_path = "results_table.csv"
data = pd.read_csv(file_path)

# Simplify the 'Result' column to show only hotel names
data['Result'] = ["Quality Inn", "Relax Inn", "Motel M"]

# Drop 'Script' column
data = data.drop(columns=['Script'])

# Streamlit app
#st.title("Competitor Prices and Recommendations")

# Add scrolling functionality to the title
st.markdown("<marquee style='font-size:48px; color:white;'>Competitor Prices and Recommendations</marquee>", unsafe_allow_html=True)

# Display the table
st.dataframe(data)

st.write("")

# Update the recommendation text to "CHANGE MOTEL M PRICE TO"
recommended_price = data.loc[data['Result'] == "Motel M", 'Recommendation'].values[0]
recommended_price = recommended_price.replace("Adjust to", "CHANGE MOTEL M PRICE TO")

#st.write(")
st.markdown(f"<h1 style='text-align: center; color: red;'>{recommended_price}</h1>", unsafe_allow_html=True)
