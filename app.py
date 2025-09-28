import pickle
import streamlit as st
import os
import psutil
import random
import pandas as pd

CHUNK_SIZE = 5000
SEPARATOR = "\u2003"
RECS_PER_PAGE = 10

# --- Page Configuration ---
st.set_page_config(
    page_title="Cross-Media Recommender",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="expanded",
)

# --- Function to load external CSS ---
def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"CSS file not found: {file_name}. Styles will not be applied.")

# --- Data Loading and Transformation ---
@st.cache_data
def load_data():
    try:
        with open('master_df.pkl', 'rb') as f:
            master_df = pickle.load(f)

        parsed_df = master_df['name_with_type'].str.rsplit(' (', n=1, expand=True)
        master_df['name'] = parsed_df[0]
        master_df['type'] = parsed_df[1].str.replace(')', '', regex=False).str.lower()

        master_df['media_prefix'] = master_df['type'].map({'movie': '🎬', 'show': '📺', 'book': '📖', 'game': '🎮'})
        
        master_df['name_with_prefix'] = master_df.apply(
            lambda row: f"{row['media_prefix']}{SEPARATOR}{row['name']}", axis=1
        )
        return master_df
    except FileNotFoundError:
        st.error("master_df.pkl not found. Please run the notebook.ipynb to generate it.")
        return None
    except Exception as e:
        st.error(f"An error occurred while loading or processing the data: {e}")
        return None

# --- Recommendation Logic ---
@st.cache_data
def get_all_recommendations(media_name_with_prefix):
    try:
        index = master_df[master_df['name_with_prefix'] == media_name_with_prefix].index[0]
    except IndexError:
        return None, f'Media "{media_name_with_prefix}" not found. The dataset might be out of sync.'

    chunk_num = index // CHUNK_SIZE
    chunk_file = f'similarity_chunks/sim_chunk_{chunk_num * CHUNK_SIZE}.pkl'

    if not os.path.exists(chunk_file):
        return None, f"Similarity chunk file not found: {chunk_file}. Please run the notebook.ipynb."

    with open(chunk_file, 'rb') as f:
        sim_chunk = pickle.load(f)

    sim_scores = list(enumerate(sim_chunk[index % CHUNK_SIZE]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    media_indices = [i[0] for i in sim_scores[1:]]
    
    return master_df.iloc[media_indices], None

# --- Initialize State ---
def init_state():
    if 'page' not in st.session_state:
        st.session_state.page = 0  # 0 means no recommendations shown yet
    if 'current_selection' not in st.session_state:
        st.session_state.current_selection = None
    if 'recommendations' not in st.session_state:
        st.session_state.recommendations = pd.DataFrame()

# --- UI Rendering ---
master_df = load_data()
if master_df is None:
    st.stop()

init_state()
local_css("style.css")

# --- Sidebar --- 
with st.sidebar:
    st.markdown("### App Information")
    st.markdown("""
    <div class="sidebar-content">
        <div class="legend">
            <div class="legend-item legend-movie"><span class='legend-icon'>🎬</span><span class='legend-label'>Movie</span></div>
            <div class="legend-item legend-show"><span class='legend-icon'>📺</span><span class='legend-label'>Show</span></div>
            <div class="legend-item legend-book"><span class='legend-icon'>📖</span><span class='legend-label'>Book</span></div>
            <div class="legend-item legend-game"><span class='legend-icon'>🎮</span><span class='legend-label'>Game</span></div>
        </div>
        <h4>App Memory Usage</h4>
        <p>This shows the memory currently used by the Streamlit app process.</p>
    """, unsafe_allow_html=True)
    
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    st.metric(label="Current Usage", value=f"{mem_info.rss / (1024 ** 2):.2f} MB")

    st.markdown("""
    <div class="sidebar-content">
        <h4>Cache Information</h4>
        <p>The app caches data and recommendations to improve performance. You can clear the cache from the ☰ menu in the top-right corner.</p>
    </div>
    """, unsafe_allow_html=True)

# --- Main Page --- 
st.title('Cross-Media Recommender System')

media_list = master_df['name_with_prefix'].values
if 'placeholder' not in st.session_state or st.session_state['placeholder'] not in media_list:
    st.session_state['placeholder'] = random.choice(media_list)

# --- Layout for Search and Button ---
col1, col2 = st.columns([5, 2])

with col1:
    selected_media = st.selectbox(
        "Select a media to get recommendations",
        media_list,
        placeholder=f"e.g., {st.session_state['placeholder']}",
        index=None,
        label_visibility="collapsed"
    )

# --- Main Logic for Instant Recommendations & Pagination ---
if selected_media and st.session_state.current_selection != selected_media:
    st.session_state.current_selection = selected_media
    st.session_state.page = 1  # Show first page on new selection
    with st.spinner('Finding recommendations...'):
        recs, error = get_all_recommendations(selected_media)
        if error:
            st.error(error)
            st.session_state.recommendations = pd.DataFrame()
        else:
            st.session_state.recommendations = recs

# --- Button Logic ---
button_text = "More Recommendations" if st.session_state.page > 0 else "Show Recommendations"
with col2:
    if st.button(button_text):
        if st.session_state.page > 0:
            st.session_state.page += 1
        elif selected_media:
            st.session_state.page = 1 # Show the first page if nothing is shown yet

# --- Display Recommendations ---
if st.session_state.page > 0:
    if not st.session_state.recommendations.empty:
        st.subheader("Here are some recommendations for you:")
        
        start_index = (st.session_state.page - 1) * RECS_PER_PAGE
        end_index = start_index + RECS_PER_PAGE
        current_recs = st.session_state.recommendations.iloc[start_index:end_index]

        if current_recs.empty:
            st.warning("No more recommendations to show.")
        else:
            for _, row in current_recs.iterrows():
                st.markdown(
                    f'''<div class="media-container {row["type"]}-style">
                        <span class="media-prefix">{row["media_prefix"]}</span>
                        <span>{row["name"]}</span>
                    </div>''',
                    unsafe_allow_html=True
                )
    elif selected_media: # Handle case where selection was made but recs are empty
         st.warning("Could not find any recommendations for the selected item.")
