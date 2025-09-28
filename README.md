# Cross-Media Recommendation Engine

## Project Overview

This project is a content-based recommendation engine that suggests similar media (books, games, movies, and TV shows) based on a user's input. The goal is to provide a unified recommendation experience across different media types.

## How It Works

The recommendation engine is built on the concept of "content-based filtering". It works in the following steps:

1.  **Data Ingestion and Unification:** The engine starts by loading four separate datasets: books, games, movies, and TV shows. These datasets are cleaned and merged into a single master dataframe with a unified schema.

2.  **Feature Engineering:** For each item in the master dataframe, a "tags" string is created. This is a single string that combines the item's overview (plot summary, description) and its genres. This "tags" string represents the textual content of the item.

3.  **TF-IDF Vectorization:** The "tags" for all items is then processed using a Term Frequency-Inverse Document Frequency (TF-IDF) vectorizer. This converts the text into a numerical matrix, where each row represents an item and each column represents a word, with the values indicating the importance of that word to the item.

4.  **Cosine Similarity:** A cosine similarity matrix is then computed from the TF-IDF matrix. This matrix contains a similarity score between every pair of items. A higher score indicates a greater similarity in content.

5.  **Recommendation Generation:** When a user selects a title, the system looks up its corresponding row in the similarity matrix. The items with the highest similarity scores are then returned as recommendations.

## The Streamlit Application (`app.py`)

The project includes a web application built with Streamlit that allows users to interact with the recommendation engine.

-   **Search:** Users can search for a title they like.
-   **Selection:** The app displays search results, and the user can select the item they are interested in.
-   **Recommendations:** Once an item is selected, the app retrieves and displays the top 5 most similar items from the dataset.

## How to Run the Project

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Prepare the Data (if not already done):**
    Run the `multimedia_recommender.ipynb` to perform the data cleaning, feature engineering, and to generate the `master_list.pkl` and the `similarity.pkl` files.

3.  **Run the Streamlit App:**
    ```bash
    streamlit run app.py
    ```

This documentation serves as a record of the project's design, implementation, and the lessons learned.