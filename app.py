import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px 

#Load dataset 
def load_dataset():
    return pd.read_csv('output.csv')

df = load_dataset()

#Title
st.title('Analysis of Indian Movies')

# Search Movie by Name 
st.subheader('Search Movie by Name')
search_name = st.text_input('Enter Movie Name either full or partial')

if search_name:
    results = df[df['Movie Name'].str.contains(search_name, case = False)]
    if not results.empty:
        st.write(f'found {len(results)} movies')
        st.dataframe(results[['Movie Name','Year','Timing(min)','Rating(10)','Votes','Genre','Language']])
    else:
        st.write("No Movies Found based on Query")

## Filters
st.sidebar.header("Filters")

## Filters By Genre
genre_filter = st.sidebar.multiselect("Select Genre", df['Genre'].unique(), default=[])

## Apply Filters:
if genre_filter:
    df = df[df["Genre"].isin(genre_filter)]

## Filters By Language
language_filter = st.sidebar.multiselect("Select Language", df['Language'].unique(), default=[])

## Apply Filters:
if language_filter:
    df = df[df["Language"].isin(language_filter)]

## Year Slider filter 
year_range = st.sidebar.slider("Select Year Range", int(df['Year'].min()), int(df['Year'].max()), (1950,2025))
df = df[df['Year'].between(*year_range)]


## Display this filtered DF on screen.
st.subheader('Filtered Movie Data')
st.write(f"Found {len(df)} movies after filter")
st.dataframe(df)

## Data Vizualization
st.subheader('Vizualizations.. ')
viz_selection = st.selectbox("Choose from given Analysis options",
                             ['Top 10 movies by Ratings',
                              'Top 10 movies by Votes']
                            )

if viz_selection == 'Top 10 movies by Ratings':
    # filtered_df = df.sort_values(by = 'Ratings(10)', ascending=False).head(10)
    filtered_df = df.sort_values(by = 'Rating(10)', ascending=False).head(10)
    st.write('Top 10 Movies Based on Ratings')
    st.dataframe(filtered_df[['Movie Name','Year','Timing(min)','Rating(10)','Votes','Genre','Language']])
    st.write('BAR Chart: Top Movies with Ratings')
    fig = px.bar(filtered_df, x = 'Movie Name', y = 'Rating(10)', title = 'Movies with Ratings')
    st.plotly_chart(fig)

elif viz_selection == 'Top 10 movies by Ratings':
    filtered_df = df.sort_values(by = 'Votes', ascending=False).head(10)
    st.write('Top 10 Movies Based on Votes')
    st.dataframe(filtered_df[['Movie Name','Year','Timing(min)','Rating(10)','Votes','Genre','Language']])
    st.write('BAR Chart: Top Movies with Votes')
    fig = px.bar(filtered_df, x = 'Movie Name', y = 'Votes', title = 'Movies with Votes')
    st.plotly_chart(fig)
