# FinSage Pro - Modular Bajaj Finserv RAG Chatbot

A modular, well-structured Flask application that provides a conversational AI assistant for Bajaj Finserv stock analysis and business information using Retrieval-Augmented Generation (RAG).

## 🏗️ Project Structure

```
finsage-pro/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── rag_system.py         # RAG system implementation
├── stock_analyzer.py     # Stock data analysis module
├── utils.py              # Utility functions
├── requirements.txt      # Python dependencies
├── templates/
│   └── index.html       # Frontend template
├── BFS_Share_Price.csv  # Stock price data (required)
└── earnings_*.txt       # Optional earnings transcripts
```



## 🚀 Installation & Setup

1. **Clone or download the project files**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   export GEMINI_API_KEY="your_gemini_api_key_here"
   ```

4. **Prepare data files:**
   - Place `BFS_Share_Price.csv` in the root directory
   - Optionally add earnings transcript files (earnings_*.txt)

5. **Run the application:**
   ```bash
   python app.py
   ```

6. **Access the application:**
   - Open your browser to `http://localhost:5000`

## 📊 Data Requirements

### Required Files:
- **BFS_Share_Price.csv**: Stock price data with columns:
  - Date (DD/MM/YYYY format)
  - Close Price (numeric)

### Optional Files:
- **earnings_q1_fy25.txt**: Q1 earnings transcript
- **earnings_q2_fy25.txt**: Q2 earnings transcript
- **earnings_q3_fy25.txt**: Q3 earnings transcript
- **earnings_q4_fy25.txt**: Q4 earnings transcript

## 🔧 Configuration

Modify `config.py` to customize:

- **Model Settings**: Change embedding or generative models
- **RAG Parameters**: Adjust chunk size, overlap, search results
- **File Paths**: Update data file locations
- **Flask Settings**: Modify debug mode, host, port

## 🎯 Features

### Stock Analysis
- Query highest, lowest, average stock prices
- Filter by specific years or date ranges
- Real-time stock data processing

### RAG-based Q&A
- Document retrieval from earnings transcripts
- Context-aware responses using Google Gemini
- Source attribution for transparency

