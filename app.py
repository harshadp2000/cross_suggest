import streamlit as st
import pandas as pd
import pickle
import os
import numpy as np
from scipy import sparse
import json
import gc
import psutil
import time

# --- Custom CSS for a rich, classy beige theme ---
st.markdown('''
<style>
    /* Core background and text colors */
    .stApp {
        background-color: #F5F5DC; /* Beige background */
    }
    /* Main text color */
    .st-emotion-cache-16txtl3, .st-emotion-cache-1jicfl2, .st-emotion-cache-1y4p8pa {
        color: #3D362A; /* Dark brown text for readability */
    }
    h1, h2, h3, h4, h5, h6 {
        color: #5C5241; /* Slightly lighter brown for headers */
    }

    /* Text input styling */
    .st-emotion-cache-ue6h4q {
        background-color: #EAE0C8; /* Lighter beige for input background */
        border: 1px solid #D3C5AA;
        color: #3D362A;
    }

    /* Button styling */
    .stButton>button {
        background-color: #D3C5AA; /* Muted beige for buttons */
        color: #3D362A;
        border: 1px solid #5C5241;
        border-radius: 5px;
        padding: 8px 12px;
        width: 100%; /* Make buttons full width */
        text-align: left; /* Align text to the left */
    }
    .stButton>button:hover {
        background-color: #C4B79F;
        color: #3D362A;
    }

    /* Expander (for overview) styling */
    .st-emotion-cache-p5msec {
        background-color: #EAE0C8; /* Lighter beige for expander header */
        border-radius: 5px;
    }
    
    /* Sidebar styling */
    .st-emotion-cache-10oheav {
        background-color: #EAE0C8; /* Lighter beige for sidebar */
    }

</style>
''', unsafe_allow_html=True)


# --- Helper Functions ---
def get_memory_usage():
    """Get current memory usage in MB"""
    process = psutil.Process()
    return process.memory_info().rss / (1024 * 1024)

def log_memory(message):
    """Log memory usage with a message"""
    mem = get_memory_usage()
    st.sidebar.text(f"{message}: {mem:.0f}MB")
    return mem

# --- 1. Load & Index Artifacts (Memory-Efficiently) ---
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_metadata_and_index_chunks():
    """Loads only metadata and chunk index, not the actual matrices."""
    try:
        log_memory("Before loading data")
        
        # Load master dataframe
        df_chunks = []
        if os.path.exists('master_df_part_0.pkl'):
            chunk_num = 0
            while os.path.exists(f'master_df_part_{chunk_num}.pkl'):
                with open(f'master_df_part_{chunk_num}.pkl', 'rb') as f:
                    df_chunks.append(pickle.load(f))
                chunk_num += 1
            master_df = pd.concat(df_chunks, ignore_index=True)
        else:
            with open('master_df.pkl', 'rb') as f:
                master_df = pickle.load(f)

        del df_chunks
        gc.collect()
        
        chunk_dir = 'similarity_chunks'
        if not os.path.exists(chunk_dir):
            st.error(f"Directory '{chunk_dir}' not found")
            return None, None

        # Load chunk index
        with open(os.path.join(chunk_dir, 'chunk_index.json'), 'r') as f:
            chunk_metadata = json.load(f)

        if 'genres' in master_df.columns:
            master_df['genres'] = master_df['genres'].apply(
                lambda g: tuple(g) if isinstance(g, list) else g
            )
            
        log_memory("After loading data")
        return master_df, chunk_metadata['index']

    except Exception as e:
        st.error(f"Error loading metadata: {e}")
        return None, None

master_df, chunk_index = load_metadata_and_index_chunks()

# --- 2. Core Recommendation Logic ---
@st.cache_data(ttl=300)
def get_recommendations(title, top_n=10):
    """Memory-efficient recommendation lookup."""
    if master_df is None or chunk_index is None: return pd.DataFrame()
    try:
        idx = master_df.index[master_df['name'] == title][0]
    except IndexError:
        return pd.DataFrame()

    chunk_info = next((c for c in chunk_index if c['start_row'] <= idx < c['end_row']), None)
    if not chunk_info: return pd.DataFrame()

    try:
        log_memory("Before loading similarity chunk")
        chunk = sparse.load_npz(os.path.join('similarity_chunks', chunk_info['file']))
        
        similarities = chunk.getrow(idx - chunk_info['start_row']).toarray().ravel()
        top_indices = np.argsort(similarities)[::-1][1:top_n+1]
        
        del similarities, chunk
        gc.collect()
        
        log_memory("After recommendation computation")
        return master_df.iloc[top_indices][['name', 'media_type', 'overview', 'genres']]
    
    except Exception as e:
        st.error(f"Error loading chunk {chunk_info['file']}: {e}")
        return pd.DataFrame()

# --- 3. Streamlit User Interface ---
st.set_page_config(layout="wide", page_title="Cross-Media Recommendations", initial_sidebar_state="expanded")

# Sidebar
st.sidebar.title("System Monitor")
log_memory("Current Memory")
if 'last_gc_time' not in st.session_state: st.session_state.last_gc_time = time.time()
if time.time() - st.session_state.last_gc_time > 300:
    gc.collect()
    st.session_state.last_gc_time = time.time()
    log_memory("After GC")

st.title("Cross-Media Recommendation System")
st.markdown("Discover new Books, Games, Movies, and TV Shows based on your interests.")

if master_df is not None and chunk_index is not None:
    # Initialize session state
    if 'search_query' not in st.session_state:
        st.session_state.search_query = ""
    if 'selected_item_name' not in st.session_state:
        st.session_state.selected_item_name = None

    # --- Search UI ---
    def update_search_query():
        # Callback to update search query from text input
        st.session_state.search_query = st.session_state.search_box
        st.session_state.selected_item_name = None # Clear selection when user types

    st.text_input(
        "Search for a title you like:",
        key='search_box',
        on_change=update_search_query,
        placeholder="e.g., The Office, Game of Thrones, Elden Ring...",
    )

    # --- Live Search Results ---
    if st.session_state.search_query and st.session_state.selected_item_name is None:
        query_lower = st.session_state.search_query.lower()
        search_results = master_df[master_df['name'].str.lower().str.contains(query_lower, na=False)]

        if not search_results.empty:
            st.write("Did you mean...?")
            for index, row in search_results.head(5).iterrows(): # Show top 5 matches
                if st.button(f"{row['name']} ({row['media_type']})", key=f"select_{index}"):
                    st.session_state.selected_item_name = row['name']
                    st.session_state.search_query = row['name'] # Set search box to the full name
                    st.rerun()
        else:
            st.info("No matches found for your search.")

    # --- Recommendation Display ---
    if st.session_state.selected_item_name:
        st.header(f"Recommendations for '{st.session_state.selected_item_name}':")
        
        recommendations = get_recommendations(st.session_state.selected_item_name, top_n=10)

        if not recommendations.empty:
            cols = st.columns(2)
            for i, (index, row) in enumerate(recommendations.iterrows()):
                with cols[i % 2]:
                    with st.container(border=True):
                        st.subheader(f"{row['name']} ({row['media_type']})")
                        if isinstance(row['genres'], (list, tuple)):
                            st.write(f"**Genres:** {', '.join(row['genres']).title()}")
                        with st.expander("View Overview"):
                            st.write(row['overview'] or "No overview available.")
        else:
            st.write("Could not find any recommendations for this title.")
        
        if st.button("Search for another title"):
            st.session_state.selected_item_name = None
            st.session_state.search_query = ""
            st.rerun()
else:
    st.error("Application data could not be loaded. Please check the logs.")
