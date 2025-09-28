import pickle
import streamlit as st
import os

CHUNK_SIZE = 5000

# Load the master dataframe
try:
    master_df = pickle.load(open('master_df.pkl', 'rb'))
except FileNotFoundError:
    st.error('master_df.pkl not found. Please run the jnotebook.ipynb notebook first.')
    st.stop()

# Function to get recommendations
def recommend(media_name_with_type):
    try:
        index = master_df[master_df['name_with_type'] == media_name_with_type].index[0]
    except IndexError:
        st.error(f'Media "{media_name_with_type}" not found in the dataset.')
        return []

    # Determine which chunk to load
    chunk_num = index // CHUNK_SIZE
    chunk_file = f'similarity_chunks/sim_chunk_{chunk_num * CHUNK_SIZE}.pkl'

    if not os.path.exists(chunk_file):
        st.error(f'Similarity chunk file not found: {chunk_file}. Please run the jnotebook.ipynb notebook.')
        return []

    with open(chunk_file, 'rb') as f:
        sim_chunk = pickle.load(f)

    # Get similarity scores for the selected media
    sim_scores = list(enumerate(sim_chunk[index % CHUNK_SIZE]))

    # Sort the media based on similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the top 5 most similar media
    sim_scores = sim_scores[1:20]

    # Get media indices
    media_indices = [i[0] for i in sim_scores]

    # Get recommended media names with types
    recommended_media = master_df.iloc[media_indices]['name_with_type'].tolist()

    return recommended_media

# Streamlit app
st.header('Cross-Media Recommender System')

media_list = master_df['name_with_type'].values
selected_media = st.selectbox(
    "Type or select a media from the dropdown",
    media_list
)

if st.button('Show Recommendation'):
    recommended_media = recommend(selected_media)
    if recommended_media:
        for media in recommended_media:
            st.text(media)