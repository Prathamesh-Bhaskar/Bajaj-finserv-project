"""
Configuration file for FinSage Pro
"""

import os

# API Configuration
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "your_gemini_api_key")

# Model Configuration
EMBEDDINGS_MODEL = 'sentence-transformers/all-MiniLM-L6-v2'
GENERATIVE_MODEL = 'gemini-1.5-flash'

# Data Configuration
STOCK_DATA_FILE = 'BFS_Share_Price.csv'
EARNINGS_FILES = [
    'earnings_q1_fy25.txt',
    'earnings_q2_fy25.txt', 
    'earnings_q3_fy25.txt',
    'earnings_q4_fy25.txt'
]

# RAG Configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
MIN_CHUNK_LENGTH = 50
DEFAULT_SEARCH_RESULTS = 3

# Flask Configuration
DEBUG_MODE = True
TEMPLATES_DIR = 'templates'
