
# Persian News Search Engine

A Python-based search engine designed to index and search Persian news articles efficiently. This project processes, normalizes, tokenizes, and indexes text data to enable fast and accurate search results.

## Features

- **Indexing**: Creates a positional index of tokens for efficient document retrieval.
- **Normalization**: Normalizes Persian text, including handling spacing, punctuation, and converting English numbers to Persian numbers.
- **Stemming**: Implements Persian stemming for better token matching.
- **Search Engine**: Provides a search interface to query indexed documents and return relevant results with their scores and metadata.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/12ali21/project.git
   ```
2. Navigate to the project directory:
   ```bash
   cd project
   ```
3. Install the required dependencies (make sure you have `pip` installed):
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the main script to index the data and perform searches:
   ```bash
   python main.py
   ```
2. Enter your query when prompted, and the search engine will return the most relevant results.

## Project Structure

- **`indexer.py`**: Handles indexing and preprocessing of text data, including tokenization, normalization, stemming, and positional indexing.
- **`search_engine.py`**: Implements the search functionality, including calculating document scores and retrieving the top results.
- **`utils.py`**: Contains utility functions and constants used across the project, such as stopword handling, punctuation definitions, and common word counting.
- **`main.py`**: The entry point of the project, integrates the indexing and search functionalities.
- **`data/`**: Contains the JSON files for storing indexed data, stopwords, and other intermediate results.
- **`.gitignore`**: Specifies ignored files and directories such as `data/`, `pack/`, and cache files.

## Data Processing

The project processes Persian text through the following stages:
1. **Tokenization**: Splits text into individual words or tokens.
2. **Normalization**: Adjusts spacing, punctuation, and character representation to standardize tokens.
3. **Stemming**: Reduces words to their root forms using a Persian stemmer.
4. **Indexing**: Creates a positional index for fast retrieval of documents based on token positions.

## Example Input/Output

### Input
```plaintext
Enter your query: خبر جدید
```

### Output
```plaintext
Score: 0.85
Title: Example News Title
URL: http://example.com/news
```

## Requirements

- Python 3.x
- Libraries: `math`, `json`, `PersianStemmer`
- JSON-formatted data files for news articles.
