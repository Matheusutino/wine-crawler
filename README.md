# Wine Crawler

A simple Python-based web scraper designed to collect data on wines from "https://www.vinhosevinhos.com/". This project aims to extract details such as wine name, price, rating, description, etc.

## Features
- Crawls wine data from specified source
- Saves data into structured formats for easy analysis

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Matheusutino/wine-crawler.git
    cd wine-crawler
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the crawler:
    ```bash
    python -m src.run
    ```

2. The collected data will be saved in the `data/` directory.

## Requirements
- Python 3.x
- Libraries listed in `requirements.txt`

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
