"""
Stock data analysis module for Bajaj Finserv
"""

import pandas as pd
import re
from config import STOCK_DATA_FILE


class StockAnalyzer:
    def __init__(self):
        self.df = None
        self.load_data()
    
    def load_data(self):
        """Load stock price data from CSV"""
        try:
            self.df = pd.read_csv(STOCK_DATA_FILE)
            self.df['Date'] = pd.to_datetime(self.df['Date'], dayfirst=True)
            print(f"Loaded {len(self.df)} stock price records")
        except Exception as e:
            print(f"Error loading stock data: {e}")
            self.df = None
    
    def get_stock_summary(self):
        """Generate stock data summary for RAG context"""
        if self.df is None:
            return None
        
        stats = self._calculate_stats()
        
        summary = f"""
        Bajaj Finserv Stock Price Data Summary:
        - Total records: {stats['total_records']}
        - Date range: {stats['date_range']}
        - Highest price: ₹{stats['highest_price']:.2f}
        - Lowest price: ₹{stats['lowest_price']:.2f}
        - Average price: ₹{stats['average_price']:.2f}
        - Latest price: ₹{stats['latest_price']:.2f} on {stats['latest_date']}
        
        The stock price data covers daily closing prices for Bajaj Finserv shares.
        This data can be used for price analysis, trend identification, and performance evaluation.
        """
        
        return {
            'content': summary,
            'source': STOCK_DATA_FILE,
            'type': 'stock_data'
        }
    
    def _calculate_stats(self):
        """Calculate basic statistics from stock data"""
        if self.df is None:
            return {}
        
        return {
            'total_records': len(self.df),
            'date_range': f"{self.df['Date'].min().strftime('%Y-%m-%d')} to {self.df['Date'].max().strftime('%Y-%m-%d')}",
            'highest_price': self.df['Close Price'].max(),
            'lowest_price': self.df['Close Price'].min(),
            'average_price': self.df['Close Price'].mean(),
            'latest_price': self.df.iloc[-1]['Close Price'],
            'latest_date': self.df.iloc[-1]['Date'].strftime('%Y-%m-%d')
        }
    
    def get_filtered_data(self, query):
        """Filter stock data based on query (e.g., by year)"""
        if self.df is None:
            return None
        
        # Extract year from query if present
        year_match = re.search(r'(\d{4})', query)
        if year_match:
            year = int(year_match.group(1))
            filtered_df = self.df[self.df['Date'].dt.year == year]
            if filtered_df.empty:
                return None
            return filtered_df
        
        return self.df
    
    def get_stock_stats_response(self, query):
        """Generate response for stock-specific queries"""
        if self.df is None:
            return "Sorry, I couldn't load the stock price data."
        
        filtered_df = self.get_filtered_data(query)
        if filtered_df is None:
            year_match = re.search(r'(\d{4})', query)
            if year_match:
                return f"No stock data available for {year_match.group(1)}."
            return "No data available for the specified criteria."
        
        stats = self._calculate_stats_for_df(filtered_df)
        
        if 'highest' in query.lower():
            return f"The highest stock price was ₹{stats['highest']:.2f} during the period {stats['period_start']} to {stats['period_end']}."
        elif 'lowest' in query.lower():
            return f"The lowest stock price was ₹{stats['lowest']:.2f} during the period {stats['period_start']} to {stats['period_end']}."
        elif 'average' in query.lower():
            return f"The average stock price was ₹{stats['average']:.2f} during the period {stats['period_start']} to {stats['period_end']}."
        else:
            return f"""Stock Price Summary for the period {stats['period_start']} to {stats['period_end']}:
            
• Highest Price: ₹{stats['highest']:.2f}
• Lowest Price: ₹{stats['lowest']:.2f}  
• Average Price: ₹{stats['average']:.2f}
• Latest Price: ₹{stats['latest']:.2f}
• Total Records: {stats['total_records']}"""
    
    def _calculate_stats_for_df(self, df):
        """Calculate statistics for a specific dataframe"""
        return {
            'highest': df['Close Price'].max(),
            'lowest': df['Close Price'].min(),
            'average': df['Close Price'].mean(),
            'latest': df.iloc[-1]['Close Price'],
            'period_start': df['Date'].min().strftime('%d-%b-%Y'),
            'period_end': df['Date'].max().strftime('%d-%b-%Y'),
            'total_records': len(df)
        }
    
    def is_stock_query(self, query):
        """Check if query is related to stock prices"""
        stock_keywords = ['stock', 'price', 'highest', 'lowest', 'average', 'trading', 'share']
        return any(word in query.lower() for word in stock_keywords)
