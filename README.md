# Journal-summarizer from RSS

## Description

This project contains a set of Python scripts designed to interact with various APIs and handle data processing tasks. It includes functionality for managing run dates, retrieving and parsing data from external sources, and a wrapper for OpenAI API interactions.

## Modules

- `main.py`: Main script that initiates the process.
- `sender.py`, `retriever.py`: Scripts responsible for sending and retrieving data.
- `run_date_mgt.py`: Manages run dates to keep track of operations.
- `openai_wrapper.py`: Simplifies interactions with the OpenAI API.

## Installation

To install the required dependencies, run the following command:

```bash
pip install -r requirements.txt
```

## Dependencies

- `openai==1.17.0`: For interacting with OpenAI APIs.
- `feedparser==6.0.11`: For parsing feeds.
- `requests==2.31.0`: For making HTTP requests.
- `beautifulsoup4==4.12.3`: For parsing HTML and XML documents.
- `pytz==2021.1`: For timezone calculations.

## Running the Project

To run the project, execute the `main.py` script:

```bash
python main.py
```

## Last Run

The last run date of the scripts is stored in `last_run_date.json`.
