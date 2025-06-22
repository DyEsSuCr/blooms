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
│   │   └── scraped_data.csv      # Final data in CSV format
│   └── raw/                      # Raw data
│       └── freshproduce.json     # Extracted metadata
├── pyproject.toml                # Project configuration
├── README.md                     # This file
├── requirements.txt              # Pip dependencies
├── run.sh                        # Main execution script
├── scrapy.cfg                    # Scrapy configuration
└── uv.lock                       # uv lock file
```

## 🛠️ Technologies Used

- **Python 3.12**: Main programming language
- **Scrapy**: Web scraping framework
- **uv**: Modern and fast Python package manager
- **Ruff**: Code linter and formatter

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
# or
uv pip freeze > requirements.txt
```

### Using pip

```bash
# Install dependencies
pip install -r requirements.txt
```

## 🚀 Usage

### Automatic Execution

The project includes a shell script that runs both spiders sequentially:

```bash
# Give execution permissions to the script
chmod +x run.sh

# Run the complete scraping process
./run.sh
```

This script:
1. **Phase 1**: Runs the `freshproduce` spider to extract metadata
2. **Phase 2**: Runs the `articles` spider to extract complete content

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

The scraping process follows a clearly defined two-phase workflow:

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

## 📊 Data Format

### Output Data (Final CSV)

```csv
url,title,descripcion,categories,page_content
https://www.freshproduce.com/...,Article Title,Brief description,[Category list],Complete article content...
```

## 📝 Notes

- The `articles` spider automatically filters URLs containing `pdf-viewer?contentId=` to avoid processing PDF documents
- Data is stored in two formats: JSON (raw data) and CSV (processed data)
- The project uses automatic pagination to retrieve all available results

---

*Developed to extract and analyze fresh produce industry content efficiently and systematically.*