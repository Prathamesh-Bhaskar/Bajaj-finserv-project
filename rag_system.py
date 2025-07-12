"""
RAG (Retrieval-Augmented Generation) system for FinSage Pro
"""

import os
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
import faiss
from config import (
    GEMINI_API_KEY, 
    EMBEDDINGS_MODEL, 
    GENERATIVE_MODEL,
    EARNINGS_FILES,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    MIN_CHUNK_LENGTH,
    DEFAULT_SEARCH_RESULTS
)
from stock_analyzer import StockAnalyzer


class SimpleRAG:
    def __init__(self):
        # Configure Gemini
        genai.configure(api_key=GEMINI_API_KEY)
        
        # Initialize models
        self.embeddings_model = SentenceTransformer(EMBEDDINGS_MODEL)
        self.generative_model = genai.GenerativeModel(GENERATIVE_MODEL)
        
        # Initialize components
        self.stock_analyzer = StockAnalyzer()
        self.index = None
        self.documents = []
        self.doc_metadata = []
        
    def load_documents(self):
        """Load all available documents for RAG"""
        documents = []
        
        # Add stock price data summary
        stock_doc = self.stock_analyzer.get_stock_summary()
        if stock_doc:
            documents.append(stock_doc)
        
        # Load earnings transcripts
        for file in EARNINGS_FILES:
            doc = self._load_text_file(file)
            if doc:
                documents.append(doc)
        
        # Add fallback business information if limited data
        if len(documents) <= 1:
            documents.append(self._get_sample_business_info())
        
        return documents
    
    def _load_text_file(self, filename):
        """Load a single text file"""
        try:
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                    return {
                        'content': content,
                        'source': filename,
                        'type': 'transcript'
                    }
        except Exception as e:
            print(f"Error reading {filename}: {e}")
        return None
    
    def _get_sample_business_info(self):
        """Provide sample business information as fallback"""
        sample_info = """
        Bajaj Finserv Business Information:
        
        Bajaj Finserv is a leading financial services company in India offering lending, insurance, and investment services.
        
        Key Business Segments:
        1. Bajaj Finance - Consumer and business lending
        2. Bajaj Allianz General Insurance (BAGIC) - General insurance products  
        3. Bajaj Allianz Life Insurance - Life insurance products
        4. Bajaj Markets - Digital platform for financial products
        
        Recent Developments:
        - Strong growth in lending business
        - Digital transformation initiatives
        - Expansion in insurance segments
        - Partnership strategies for market expansion
        
        Investment Highlights:
        - Strong brand recognition in Indian market
        - Diversified financial services portfolio
        - Digital-first approach to customer acquisition
        - Consistent financial performance track record
        """
        
        return {
            'content': sample_info,
            'source': 'business_overview',
            'type': 'business_info'
        }
    
    def create_vector_index(self):
        """Create FAISS vector index from documents"""
        documents = self.load_documents()
        
        if not documents:
            print("No documents loaded")
            return False
        
        # Split documents into chunks
        all_chunks, all_metadata = self._create_chunks(documents)
        
        if not all_chunks:
            print("No valid chunks created")
            return False
        
        # Create embeddings and index
        return self._build_faiss_index(all_chunks, all_metadata)
    
    def _create_chunks(self, documents):
        """Split documents into chunks for processing"""
        all_chunks = []
        all_metadata = []
        
        for doc in documents:
            text = doc['content']
            chunks = [
                text[i:i+CHUNK_SIZE] 
                for i in range(0, len(text), CHUNK_SIZE - CHUNK_OVERLAP)
            ]
            
            for chunk in chunks:
                if len(chunk.strip()) > MIN_CHUNK_LENGTH:
                    all_chunks.append(chunk.strip())
                    all_metadata.append({
                        'source': doc['source'],
                        'type': doc['type']
                    })
        
        return all_chunks, all_metadata
    
    def _build_faiss_index(self, chunks, metadata):
        """Build FAISS index from chunks"""
        try:
            print(f"Creating embeddings for {len(chunks)} chunks...")
            embeddings = self.embeddings_model.encode(chunks)
            
            # Create FAISS index
            dimension = embeddings.shape[1]
            self.index = faiss.IndexFlatL2(dimension)
            self.index.add(embeddings.astype('float32'))
            
            self.documents = chunks
            self.doc_metadata = metadata
            
            print(f"Vector index created with {len(chunks)} documents")
            return True
            
        except Exception as e:
            print(f"Error building FAISS index: {e}")
            return False
    
    def search(self, query, k=DEFAULT_SEARCH_RESULTS):
        """Search for relevant documents"""
        if self.index is None:
            return []
        
        try:
            query_embedding = self.embeddings_model.encode([query])
            distances, indices = self.index.search(query_embedding.astype('float32'), k)
            
            results = []
            for i, idx in enumerate(indices[0]):
                if idx < len(self.documents):
                    results.append({
                        'content': self.documents[idx],
                        'metadata': self.doc_metadata[idx],
                        'score': float(distances[0][i])
                    })
            
            return results
            
        except Exception as e:
            print(f"Error during search: {e}")
            return []
    
    def generate_answer(self, query, context_docs):
        """Generate answer using Gemini"""
        context = "\n\n".join([doc['content'] for doc in context_docs])
        
        prompt = self._create_prompt(query, context)
        
        try:
            response = self.generative_model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating answer: {e}")
            return "I apologize, but I encountered an error generating the response. Please try again."
    
    def _create_prompt(self, query, context):
        """Create prompt for the generative model"""
        return f"""
        Based on the following context about Bajaj Finserv, please answer the user's question.
        
        Context:
        {context}
        
        Question: {query}
        
        Instructions:
        - Provide a clear, accurate answer based on the context
        - If the context doesn't contain enough information, say so
        - Focus on being helpful and informative
        - Use specific numbers and facts when available
        """
    
    def process_query(self, query):
        """Process a user query and return answer with sources"""
        # Check if it's a stock-related query
        if self.stock_analyzer.is_stock_query(query):
            answer = self.stock_analyzer.get_stock_stats_response(query)
            return {
                'answer': answer,
                'sources': [self.stock_analyzer.STOCK_DATA_FILE]
            }
        
        # Use RAG for other queries
        relevant_docs = self.search(query)
        
        if not relevant_docs:
            return {
                'answer': 'I don\'t have enough information to answer your question. Please try asking about stock prices or business performance.',
                'sources': []
            }
        
        answer = self.generate_answer(query, relevant_docs)
        sources = list(set([doc['metadata']['source'] for doc in relevant_docs]))
        
        return {
            'answer': answer,
            'sources': sources
        }
