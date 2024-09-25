```
# Ozon.ru Web Scraper


This project is a web scraper for extracting data from the ozon.ru website using Scrapy.

## Setup


1. Create and activate a virtual environment:

 ```bash
 python -m venv venv
```

On Windows:

``` bash
venv\Scripts\activate
```

On macOS and Linux:

# PDF Text Extractor

This project extracts text from PDF files using OCR technology.

## Setup

1. Clone the repository:
   
   git clone https://github.com/yourusername/pdf-text-extractor.git
   cd pdf-text-extractor
   

2. Create and activate a virtual environment:
   
   python -m venv venv
   

   On Windows:
   
   venv\Scripts\activate
   

   On macOS and Linux:
   
   source venv/bin/activate
   

3. Install the required packages:
   
   pip install -r requirements.txt
   

## Usage

1. Place your PDF files in the `input_files` folder.

2. Run the script:
   
   python pdf_text_extractor.py
   

3. The extracted text will be saved in the `output` folder.

## Notes

- Make sure you have Tesseract OCR installed on your system.
- The script processes all PDF files in the `input_files` folder.
- Extracted text is saved with the same filename as the input PDF, but with a .txt extension.

``` bash
source venv/bin/activate
```

2. Install the required packages:

``` bash
pip install -r requirements.txt
```

## Usage

1. Navigate to the project directory:

``` bash
cd ozon_scraper
```

2. Run the spider:

``` bash
scrapy crawl ozon
```

3. The scraped data will be saved in current folder.

## Notes

* Make sure to add all the excel files for the inputs inside the `input_files` folder.

