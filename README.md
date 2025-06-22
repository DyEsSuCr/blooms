# Fresh Produce Scraper

A web scraping project developed with Scrapy to extract articles and content from Fresh Produce.

## 🚀 Features

- **Two-phase scraping**: First extracts article metadata, then retrieves complete content
- **Category filtering**: Allows filtering by Food Safety, Global Trade, and Technology
- **Multiple content types**: Support for Articles, Events, Podcasts, Videos, etc.
- **Automatic pagination**: Automatically navigates through all result pages
- **Flexible export**: Saves data in JSON and CSV formats
- **Modern dependency management**: Uses `uv` for package management

## 📁 Project Structure

```
.
├── app/                          # Main Scrapy application
│   ├── __init__.py
│   ├── items.py                  # Item/data definitions to extract
│   ├── middlewares.py            # Custom middlewares
│   ├── pipelines.py              # Processing pipelines
│   ├── settings.py               # Scrapy configuration
│   └── spiders/                  # Spiders directory
│       ├── articles.py           # Spider for extracting complete content
│       ├── freshproduce.py       # Spider for extracting metadata
│       └── __init__.py
├── assets/                       # Project resources
│   └── flow.png                  # Process flow diagram
├── config.py                     # Additional configurations
├── data/                         # Data directory
│   ├── processed/                # Processed data
│   │   ├── scraped_data.csv      # Complete articles with content
│   │   └── analysis_summary.csv  # LLM analysis results
│   └── raw/                      # Raw data
│       └── freshproduce.json     # Metadata from API
├── pyproject.toml                # Project configuration
├── README.md                     # This file
├── requirements.txt              # Pip dependencies
├── run.sh                        # Main execution script (runs all processes)
├── run_llm.py                    # Script for analyzing data with LLM
├── run_server.py                 # Script to start Streamlit server for data visualization
├── run_spiders.py                # Script to execute spiders for data extraction
├── scrapy.cfg                    # Scrapy configuration
└── uv.lock                       # uv lock file
```

## 🛠️ Technologies Used

- **Python 3.12**: Main programming language
- **Scrapy**: Web scraping framework
- **uv**: Modern and fast Python package manager
- **Ruff**: Code linter and formatter
- **HTTPX**: Modern HTTP client for Python
- **Asyncio**: Asynchronous I/O framework

## 📋 Prerequisites

- Python 3.12+
- uv (recommended) or pip

## 🔧 Installation

### Using uv (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd fresh-produce-scraper

# Create virtual environment with Python 3.12
uv venv --python=3.12 .venv

# Activate virtual environment
source .venv/bin/activate  # On Linux/Mac
# or
.venv\Scripts\activate     # On Windows

# Install dependencies with uv
uv sync
```

### Using pip

```bash
# Install dependencies
pip install -r requirements.txt
```

## 🚀 Usage

The project includes multiple execution options for different workflow needs:

### Complete Workflow (Recommended)

Execute the entire pipeline with a single command:

```bash
# Give execution permissions
chmod +x run.sh

# Run the complete workflow: scraping → analysis → server
./run.sh
```

This script runs all three phases sequentially:
1. **Data Extraction**: Executes `run_spiders.py` to scrape articles
2. **Data Analysis**: Runs `run_llm.py` to analyze data with LLM
3. **Data Visualization**: Starts `run_server.py` for Streamlit dashboard

### Individual Components

You can also run each component separately:

#### 1. Data Extraction Only

Extract articles and content from Fresh Produce:

```bash
python run_spiders.py
```

This script:
1. **Phase 1**: Runs the `freshproduce` spider to extract metadata
2. **Phase 2**: Runs the `articles` spider to extract complete content

#### 2. Data Analysis Only

Analyze the extracted data using LLM:

```bash
python run_llm.py
```

#### 3. Data Visualization Only

Start a Streamlit server to visualize the analyzed data:

```bash
python run_server.py
```

The server will be available at `http://localhost:8501` (default Streamlit port).

### Manual Execution

#### Spider 1: Metadata Extraction (freshproduce)

```bash
scrapy crawl freshproduce \
  -a categories="Technology|Food Safety|Global Trade" \
  -a page_size=50 \
  -a content_type="Article" \
  -a sort_by=2 \
  -O data/raw/freshproduce.json
```

#### Spider 2: Content Extraction (articles)

```bash
scrapy crawl articles -O data/processed/scraped_data.csv
```

## ⚙️ Configuration

### `freshproduce` Spider Parameters

| Parameter | Description | Available Values |
|-----------|-------------|-----------------|
| `categories` | Categories to filter | `Food Safety`, `Global Trade`, `Technology` |
| `page_size` | Items per page | Integer number (e.g.: 50, 100) |
| `content_type` | Content type | `Article`, `Event`, `Podcast`, `Video`, `Virtual Town Hall`, `Webinar` |
| `sort_by` | Sorting criteria | Integer number (e.g.: 2) |

### Custom Configuration Example

```bash
scrapy crawl freshproduce \
  -a categories="Food Safety" \
  -a page_size=25 \
  -a content_type="Article|Podcast" \
  -O my_custom_file.json
```

## 🔄 Workflow

<img src="../../assets/flow.png" alt="Flow Diagram" width="500" />

The scraping and analysis process follows a clearly defined three-phase workflow:

1. **FreshProduce Spider**: 
   - Queries the Fresh Produce search API
   - Extracts basic metadata (title, description, URL, categories)
   - Handles pagination automatically
   - Saves results to `data/raw/freshproduce.json`

2. **Articles Spider**:
   - Reads data from the previously generated JSON file
   - Visits each individual URL (excluding PDFs)
   - Extracts complete content from each article
   - Combines metadata with content
   - Saves final result to `data/processed/scraped_data.csv`

3. **LLM Analysis**:
   - Processes the complete article data
   - Generates summaries and extracts key topics using LLM
   - Creates analysis results in `data/processed/analysis_summary.csv`

## 📊 Data Format

### 1. Raw Metadata (freshproduce.json)

```json
[
  {
    "url": "https://www.freshproduce.com/...",
    "title": "Article Title",
    "description": "Brief description",
    "categories": ["Food Safety", "Technology"]
  }
]
```

### 2. Complete Articles (scraped_data.csv)

```csv
categories,descripcion,page_content,title,url
"[""Food Safety"", ""Technology""]",Brief description,Complete article content...,Article Title,https://www.freshproduce.com/...
```

**Columns:**
- `categories`: Article categories as array
- `descripcion`: Brief article description
- `page_content`: Full article content
- `title`: Article title
- `url`: Article URL

### 3. LLM Analysis Results (analysis_summary.csv)

```csv
Title,URL,Category,Summary,Topics
Article Title,https://www.freshproduce.com/...,Food Safety,AI-generated summary of the article,Key topics extracted by LLM
```

**Columns:**
- `Title`: Article title
- `URL`: Article URL
- `Category`: Primary category
- `Summary`: AI-generated article summary
- `Topics`: Key topics identified by LLM

## 📝 Notes

- The `articles` spider automatically filters URLs containing `pdf-viewer?contentId=` to avoid processing PDF documents
- Data flows through three stages: raw JSON → complete CSV → analyzed CSV
- The project uses automatic pagination to retrieve all available results
- LLM analysis provides summaries and topic extraction for better content understanding

---

*Developed to extract and analyze fresh produce industry content efficiently and systematically.*