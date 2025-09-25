# CrossSuggest - Cross-Media Recommendation Engine

## Overview

CrossSuggest is a Flask-based web application that provides cross-media search and discovery functionality across movies, TV shows, books, and games. The application allows users to search for content using two distinct modes: exact title matching and semantic search through genres, descriptions, and character names. It features a clean, responsive web interface with gradient styling and provides detailed match scoring to help users find the most relevant content across different media types.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Flask's built-in rendering
- **UI Design**: Custom CSS with gradient backgrounds and responsive design
- **Layout Structure**: Base template inheritance pattern for consistent styling
- **Search Interface**: Single-page application with form-based search functionality

### Backend Architecture
- **Framework**: Flask web framework with minimal routing structure
- **Search Logic**: Two-mode search system:
  - Title Mode: Exact and partial string matching with scoring
  - Terms Mode: Multi-field semantic search across metadata
- **Data Processing**: In-memory JSON data loading with collections.defaultdict for result organization
- **Scoring Algorithm**: Match percentage calculation based on search relevance

### Data Storage
- **Storage Format**: Static JSON files for each media type (movies, shows, books, games)
- **Data Structure**: Consistent schema across media types with fields like title, genres, description, characters, year
- **Data Organization**: Separate files in `/data/` directory for each content category
- **Loading Strategy**: Runtime JSON parsing with error handling for missing files

### Search and Matching System
- **Search Modes**: 
  - Title-based search with exact and partial matching
  - Metadata search across genres, descriptions, and character fields
- **Scoring System**: Numerical match scores (100 for exact, 80 for partial)
- **Result Organization**: Grouped by media type with score-based sorting
- **Query Processing**: Case-insensitive search with term splitting for metadata mode

## External Dependencies

### Core Framework
- **Flask**: Web framework for routing, templating, and request handling
- **Jinja2**: Template engine (bundled with Flask)

### Python Standard Library
- **json**: JSON file parsing and data loading
- **re**: Regular expression support for text processing
- **collections.defaultdict**: Result organization and grouping

### Static Assets
- **Custom CSS**: Embedded styling with gradient themes and responsive design
- **No external CSS frameworks**: Self-contained styling approach

### Data Dependencies
- **Static JSON datasets**: Local files for movies, shows, books, and games
- **No external APIs**: Fully offline search functionality
- **No database**: File-based data storage approach

## Developer setup

To set up a Python virtual environment and run the project locally (macOS / zsh):

1. Create the virtual environment (if you haven't already):

```bash
python3 -m venv venv
```

2. Activate it:

```bash
source venv/bin/activate
```

3. Upgrade packaging tools and install dependencies:

```bash
pip install -U pip setuptools wheel
pip install -r requirements.txt
```

4. Run the app:

```bash
export FLASK_APP=app.py
flask run
```

Notes:
- The project lists core dependencies in `pyproject.toml` and a pinned `requirements.txt` is included for reproducible installs.
- The `venv/` directory is ignored by git via `.gitignore`.