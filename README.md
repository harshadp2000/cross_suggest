# CrossSuggest: A Cross-Media Recommendation Engine

This project is a content-based recommender system that provides cross-media suggestions across books, games, movies, and shows. The system analyzes textual content (overview, genres, and titles) to generate relevant recommendations across different media types using TF-IDF vectorization and cosine similarity.

<img width="1614" height="906" alt="image" src="https://github.com/user-attachments/assets/519a44fe-b2e2-41c2-af60-490bdb08b3d7" />

## Features

- **Cross-Media Recommendations**: Seamlessly suggests related content across different media types
- **Interactive UI**: Clean and intuitive interface built with Streamlit
- **Memory Efficient**: Uses chunked similarity matrices to handle large datasets
- **Real-time Performance**: Implements caching for faster recommendation retrieval
- **Visual Indicators**: Uses emojis to clearly distinguish different media types:
  - 🎬 Movies
  - 📺 Shows
  - 📖 Books
  - 🎮 Games
- **Pagination**: Displays recommendations in manageable chunks with "More Recommendations" feature

## Technical Architecture

### Data Processing Pipeline
1. **Data Loading**: Imports separate datasets for books, games, movies, and shows
2. **Data Unification**: 
   - Combines all media types into a master dataset
   - Adds media type indicators
   - Creates unified name format with type information
3. **Text Processing**:
   - Cleans and normalizes genre information
   - Combines overview, genres, and name into searchable tags
   - Applies TF-IDF vectorization
4. **Similarity Computation**:
   - Calculates cosine similarity matrices
   - Splits computations into manageable chunks (5000 items per chunk)
   - Saves similarity data for efficient retrieval

### Application Components
- **Frontend**: Streamlit-based interface with custom CSS styling
- **Backend**: Python-based recommendation engine
- **Caching**: Implements Streamlit's caching for performance optimization
- **Memory Management**: Real-time memory usage monitoring

## Datasets

The system uses four primary datasets located in the `data/` directory:
- `books.csv`: Book information and metadata
- `games.csv`: Video game details and descriptions
- `movies.csv`: Movie information and synopses
- `shows.csv`: TV show details and descriptions

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/harshadp2000/cross_suggest.git
   cd cross_suggest
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Dependencies

- Python 3.x
- Key packages (with versions):
  - streamlit==1.27.0: Web application framework
  - pandas==2.1.1: Data manipulation and analysis
  - numpy==1.25.2: Numerical computations
  - scikit-learn==1.3.1: TF-IDF vectorization and similarity calculations
  - psutil==5.9.5: System and process monitoring
  - pickle5==0.0.12: Data serialization

## Setup and Usage

1. **Data Preparation**:
   Run the Jupyter notebook to process data and generate necessary files:
   ```bash
   jupyter notebook notebook.ipynb
   ```
   This will create:
   - `master_df.pkl`: Unified dataset
   - `similarity_chunks/`: Directory containing similarity matrices

2. **Launch Application**:
   ```bash
   streamlit run app.py
   ```
   The application will be available at `http://localhost:8501`

## Project Structure

```
.
├── app.py                 # Main Streamlit application
├── notebook.ipynb         # Data processing and model creation
├── requirements.txt       # Project dependencies
├── style.css             # Custom UI styling
├── master_df.pkl         # Processed unified dataset
├── data/                 # Raw datasets
│   ├── books.csv
│   ├── games.csv
│   ├── movies.csv
│   └── shows.csv
└── similarity_chunks/    # Chunked similarity matrices
    ├── sim_chunk_0.pkl
    └── sim_chunk_5000.pkl
```

## How It Works

1. **Data Processing**:
   - Combines data from all media types
   - Creates unified text representations
   - Generates TF-IDF vectors for content comparison

2. **Recommendation Generation**:
   - Uses cosine similarity for finding related content
   - Chunks similarity matrices for memory efficiency
   - Implements caching for faster retrieval

3. **User Interface**:
   - Provides intuitive media selection
   - Shows paginated recommendations
   - Displays memory usage statistics
   - Uses visual indicators for media types

## Performance Considerations

- Implements chunked similarity matrices to handle large datasets efficiently
- Uses Streamlit's caching mechanism for faster subsequent recommendations
- Monitors and displays memory usage in real-time
- Paginates results to manage memory and improve user experience

## Future Enhancements

1. **Technical Improvements**:
   - Implement collaborative filtering
   - Add support for more sophisticated NLP models (BERT, Word2Vec)
   - Optimize similarity computation for larger datasets

2. **Feature Additions**:
   - User profiles and preferences
   - Recommendation history
   - Rating system
   - Detailed content information

3. **UI Enhancements**:
   - Advanced filtering options
   - Sorting capabilities
   - Detailed media information cards
   - Mobile-responsive design improvements

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## 📧 Contact

For questions and feedback, please reach out to the repository owner:
[harshadpawarm](https://github.com/harshadpawarm)
