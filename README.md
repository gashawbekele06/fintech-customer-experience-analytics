# Fintech Customer Experience Analytics
## Project Overview
This project focuses on analyzing customer experience in the fintech industry using advanced analytics and data-driven insights. The goal is to help fintech companies understand customer behavior, improve satisfaction, and optimize engagement strategies.

## Project Goals
- Understand customer behavior through data analytics
- Identify pain points and improve user experience
- Predict churn and enhance retention strategies
- Provide actionable insights via dashboards

## Analytics Workflow
1. **Data Collection**: Gather raw data from multiple sources
2. **Preprocessing**: Clean and transform data using `src/preprocess.py`
3. **Exploratory Data Analysis (EDA)**: Conduct analysis in `notebooks/eda.ipynb`
4. **Sentiment Analysis**: Analyze customer feedback in `notebooks/sentiment_analysis.ipynb`
5. **Visualization**: Generate interactive dashboards using Plotly

## Features
- Customer segmentation and profiling
- Sentiment analysis on customer feedback
- Predictive analytics for churn detection
- Interactive dashboards for visualization
- Data preprocessing and feature engineering

## Installation
```bash
git clone https://github.com/gashawbekele06/fintech-customer-experience-analytics.git
cd fintech-customer-experience-analytics
pip install -r requirements.txt
```

##  Usage
```bash
# Run preprocessing script
python src/preprocess.py

# Run scraping script
python src/scrap.py

# For Jupyter Notebook analysis
jupyter notebook notebooks/eda.ipynb
```

## Technologies Used
- Python (Pandas, NumPy, Scikit-learn)
- Jupyter Notebook
- Matplotlib & Seaborn for visualization
- Plotly for interactive dashboards

## 📂 Folder Structure
```
fintech-customer-experience-analytics/
│
├── data/                     # Raw and processed datasets
├── notebooks/                # Jupyter notebooks for analysis
│   ├── __init__.py
│   ├── eda.ipynb             # Exploratory Data Analysis
│   └── sentiment_analysis.ipynb # Sentiment analysis notebook
├── src/                      # Source code for data processing and configuration
│   ├── __pycache__/
│   ├── data/                 # Additional data-related scripts or files
│   ├── config.py             # Configuration settings
│   ├── preprocess.py         # Data preprocessing logic
│   └── scrap.py              # Data scraping or extraction
├── venv/                     # Virtual environment
├── .gitignore                # Git ignore file
├── README.md                 # Project documentation
└── requirements.txt          # Python dependencies
```

##  Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any improvements or new features.

## 📄 License
This project is licensed under the MIT License.
