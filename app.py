"""
FinSage Pro - Modular Bajaj Finserv RAG Chatbot
Main Flask application
"""

from flask import Flask, render_template, request, jsonify
from rag_system import SimpleRAG
from config import DEBUG_MODE
from utils import setup_application


# Initialize Flask app
app = Flask(__name__)

# Initialize RAG system
rag = None


def initialize_rag():
    """Initialize the RAG system"""
    global rag
    try:
        print("Initializing RAG system...")
        rag = SimpleRAG()
        rag.create_vector_index()
        print("RAG system ready!")
        return True
    except Exception as e:
        print(f"Error initializing RAG system: {e}")
        return False


@app.route('/')
def index():
    """Serve the main chat interface"""
    return render_template('index.html')


@app.route('/api/query', methods=['POST'])
def process_query():
    """Process user queries and return responses"""
    try:
        data = request.json
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({
                'answer': 'Please provide a question.',
                'sources': []
            })
        
        # Initialize RAG if not already done
        if rag is None:
            if not initialize_rag():
                return jsonify({
                    'answer': 'Sorry, the system is not ready. Please try again later.',
                    'sources': []
                })
        
        # Process the query
        result = rag.process_query(query)
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Error processing query: {e}")
        return jsonify({
            'answer': 'Sorry, I encountered an error processing your request. Please try again.',
            'sources': []
        })


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'rag_initialized': rag is not None
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Endpoint not found',
        'message': 'The requested resource was not found on this server.'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal server error',
        'message': 'An internal error occurred. Please try again later.'
    }), 500


def main():
    """Main function to run the application"""
    print("Starting FinSage Pro...")
    
    # Setup application (create templates, etc.)
    setup_application()
    
    # Initialize RAG system
    initialize_rag()
    
    # Run the Flask app
    app.run(debug=DEBUG_MODE, host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()
