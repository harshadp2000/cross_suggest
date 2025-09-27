# Cross-Media Recommendation Engine

## Project Overview

This project is a content-based recommendation engine that suggests similar media (books, games, movies, and TV shows) based on a user's input. The goal is to provide a unified recommendation experience across different media types.

## How It Works

The recommendation engine is built on the concept of "content-based filtering". It works in the following steps:

1.  **Data Ingestion and Unification:** The engine starts by loading four separate datasets: books, games, movies, and TV shows. These datasets are cleaned and merged into a single master dataframe with a unified schema.

2.  **Feature Engineering:** For each item in the master dataframe, a "feature soup" is created. This is a single string that combines the item's overview (plot summary, description) and its genres. This "soup" represents the textual content of the item.

3.  **TF-IDF Vectorization:** The "feature soup" for all items is then processed using a Term Frequency-Inverse Document Frequency (TF-IDF) vectorizer. This converts the text into a numerical matrix, where each row represents an item and each column represents a word, with the values indicating the importance of that word to the item.

4.  **Cosine Similarity:** A cosine similarity matrix is then computed from the TF-IDF matrix. This matrix contains a similarity score between every pair of items. A higher score indicates a greater similarity in content.

5.  **Recommendation Generation:** When a user selects a title, the system looks up its corresponding row in the similarity matrix. The items with the highest similarity scores are then returned as recommendations.

## The Streamlit Application (`app.py`)

The project includes a web application built with Streamlit that allows users to interact with the recommendation engine.

-   **Search:** Users can search for a title they like.
-   **Selection:** The app displays search results, and the user can select the item they are interested in.
-   **Recommendations:** Once an item is selected, the app retrieves and displays the top 10 most similar items from the dataset.

Due to the large size of the similarity matrix, it is stored in chunks on disk. The Streamlit app loads only the necessary chunk for the selected item, making it more memory-efficient.

## What Went Wrong & Challenges

This project, while functional, faced several challenges and has some inherent limitations:

1.  **Memory Constraints:** The primary challenge was the size of the cosine similarity matrix. For a dataset of over 100,000 items, the full matrix would be too large to fit into memory. The solution was to compute and store the matrix in smaller chunks. The Streamlit app then loads only the required chunk on demand. This, however, introduces I/O overhead and complexity.

2.  **Scalability:** The chunking approach, while a valid workaround, does not scale well. As the number of items grows, so does the number of chunks, leading to a more fragmented and potentially slower system.

3.  **Recommendation Quality:** The recommendations are purely content-based, relying on TF-IDF of item overviews and genres. This has几tations:
    *   **"Cold Start" Problem:** The model cannot recommend items that are not in the initial dataset.
    *   **Limited Scope:** It doesn't incorporate user ratings or behavior (collaborative filtering), which could provide more personalized and diverse recommendations.
    *   **Garbage In, Garbage Out:** The quality of recommendations is highly dependent on the quality and richness of the `overview` and `genres` data.

4.  **Deployment and Maintenance:** The need to manage a large number of data files (the master dataframe and all the similarity chunks) makes deploying and updating the application cumbersome.

## How to Run the Project

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Prepare the Data (if not already done):**
    Run the `jupyter_notebook.ipynb` to perform the data cleaning, feature engineering, and to generate the `master_df.pkl` and the similarity matrix chunks in the `similarity_chunks/` directory.

3.  **Run the Streamlit App:**
    ```bash
    streamlit run app.py
    ```

This documentation serves as a record of the project's design, implementation, and the lessons learned.
