# AI Data Analyst Dashboard

Upload any CSV file (sales, ecommerce, employee, or general business data) and get instant data cleaning, visual charts, and an AI-generated summary — all in one dashboard.

## Features

- Drag-and-drop CSV upload
- Automatic data cleaning (missing values, duplicates)
- Auto-generated charts (distribution, category counts, correlation heatmap)
- Plain-English AI summary of your data using GPT
- One-click Excel report download

## Setup

1. Clone this repo
2. Install dependencies:  pip install -r requirements.txt
3. Create a `.env` file in the project folder and add your OpenAI API key:  OPENAI_API_KEY=your_key_here
4. Run the app:streamlit run app.py


## Sample Data

A sample CSV (`sample_sales.csv`) is included so you can test the app right away.

## Tech Stack

Python, Streamlit, Pandas, Matplotlib, Seaborn, OpenAI API
