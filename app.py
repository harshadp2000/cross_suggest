
import pickle
import streamlit as st
import os

CHUNK_SIZE = 5000

# Load the master dataframe
try:
    master_df = pickle.load(open('master_df.pkl', 'rb'))
except FileNotFoundError:
    st.error('master_df.pkl not found. Please run the multimedia_recommender_chunked.ipynb notebook first.')
    st.stop()

# Function to get recommendations
def recommend(media):
    try:
        index = master_df[master_df['name'] == media].index[0]
    except IndexError:
        st.error(f'Media "{media}" not found in the dataset.')
        return [], []

    # Determine which chunk to load
    chunk_num = index // CHUNK_SIZE
    chunk_file = f'similarity_chunks/sim_chunk_{chunk_num * CHUNK_SIZE}.pkl'

    if not os.path.exists(chunk_file):
        st.error(f'Similarity chunk file not found: {chunk_file}. Please run the multimedia_recommender_chunked.ipynb notebook.')
        return [], []

    with open(chunk_file, 'rb') as f:
        sim_chunk = pickle.load(f)

    # Get similarity scores for the selected media
    sim_scores = list(enumerate(sim_chunk[index % CHUNK_SIZE]))

    # Sort the media based on similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the top 5 most similar media
    sim_scores = sim_scores[1:6]

    # Get media indices
    media_indices = [i[0] for i in sim_scores]

    # Get recommended media names and types
    recommended_media_names = master_df.iloc[media_indices]['name'].tolist()
    recommended_media_types = master_df.iloc[media_indices]['media_type'].tolist()

    return recommended_media_names, recommended_media_types

# Streamlit app
st.header('Cross-Media Recommender System')

media_list = master_df['name'].values
selected_media = st.selectbox(
    "Type or select a media from the dropdown",
    media_list
)

if st.button('Show Recommendation'):
    recommended_media_names, recommended_media_types = recommend(selected_media)
    if recommended_media_names:
        for i in range(len(recommended_media_names)):
            st.text(f"{recommended_media_names[i]} ({recommended_media_types[i]})")
