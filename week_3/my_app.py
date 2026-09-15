import streamlit as st
st.title ("Hello, streamit!")
st.write("This is my first streamlit app.")


if st.button("Click me!"):
    st.write("🎉 You clicked the button! Nice work! 🚀")
else:
    st.write("Click the button to see what happens...")

import pandas as pd

st.subheader ("Exploring Our Dataset")

df = pd.read_csv("data/sample_data.csv")

    # if in week_2
    

st.write ("Here's out data")
st.dataframe(df)

city = st.selectbox("Select a city", df["City"].unique())
st.write(f"People in {city}")
st.dataframe(df[df["City"] == city])

st.bar_chart(df["Salary"])