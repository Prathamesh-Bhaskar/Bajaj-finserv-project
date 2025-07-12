"""
Utility functions for FinSage Pro
"""

import os
from config import TEMPLATES_DIR


def ensure_templates_directory():
    """Ensure templates directory exists"""
    os.makedirs(TEMPLATES_DIR, exist_ok=True)


def create_html_template():
    """Create the HTML template file if it doesn't exist"""
    template_path = os.path.join(TEMPLATES_DIR, 'index.html')
    
    if not os.path.exists(template_path):
        html_content = get_html_template_content()
        
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Created template: {template_path}")


def get_html_template_content():
    """Return the HTML template content"""
    return r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FinSage Pro - Bajaj Finserv Assistant</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --primary-color: #003d7d;
            --secondary-color: #0072bc;
            --accent-color: #f7941d;
            --light-gray: #f5f5f5;
            --dark-gray: #333;
            --white: #fff;
            --shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            --border-radius: 8px;
            --transition: all 0.3s ease;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        body {
            background-color: var(--light-gray);
            color: var(--dark-gray);
            line-height: 1.6;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            display: flex;
            flex-direction: column;
            height: 100vh;
        }

        header {
            display: flex;
            align-items: center;
            padding: 15px 0;
            border-bottom: 1px solid rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }

        .logo h1 {
            font-size: 1.5rem;
            color: var(--primary-color);
            font-weight: 600;
        }

        main {
            display: flex;
            flex: 1;
            gap: 20px;
            height: calc(100vh - 120px);
        }

        .chat-container {
            flex: 1;
            display: flex;
            flex-direction: column;
            background: var(--white);
            border-radius: var(--border-radius);
            box-shadow: var(--shadow);
            overflow: hidden;
        }

        .chat-header {
            background-color: var(--primary-color);
            color: var(--white);
            padding: 15px;
            font-weight: 600;
            display: flex;
            align-items: center;
        }

        .chat-header i {
            margin-right: 10px;
            font-size: 1.2rem;
        }

        .chat-messages {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        .message {
            max-width: 80%;
            padding: 12px 15px;
            border-radius: 18px;
            position: relative;
            animation: fadeIn 0.3s ease;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .user-message {
            align-self: flex-end;
            background-color: var(--secondary-color);
            color: var(--white);
            border-bottom-right-radius: 5px;
        }

        .assistant-message {
            align-self: flex-start;
            background-color: var(--light-gray);
            border-bottom-left-radius: 5px;
        }

        .sources {
            font-size: 0.8rem;
            margin-top: 8px;
            color: #666;
            font-style: italic;
        }

        .chat-input {
            display: flex;
            padding: 15px;
            background-color: var(--white);
            border-top: 1px solid rgba(0, 0, 0, 0.1);
        }

        .chat-input input {
            flex: 1;
            padding: 12px 15px;
            border: 1px solid #ddd;
            border-radius: 25px;
            font-size: 0.95rem;
            outline: none;
            transition: var(--transition);
        }

        .chat-input input:focus {
            border-color: var(--secondary-color);
            box-shadow: 0 0 0 2px rgba(0, 114, 188, 0.2);
        }

        .chat-input button {
            background-color: var(--secondary-color);
            color: var(--white);
            border: none;
            border-radius: 50%;
            width: 45px;
            height: 45px;
            margin-left: 10px;
            cursor: pointer;
            transition: var(--transition);
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .chat-input button:hover {
            background-color: var(--primary-color);
        }

        .info-panel {
            width: 300px;
            background: var(--white);
            border-radius: var(--border-radius);
            box-shadow: var(--shadow);
            padding: 20px;
        }

        .example-query {
            background-color: var(--light-gray);
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 0.9rem;
            margin-bottom: 8px;
            cursor: pointer;
            transition: var(--transition);
        }

        .example-query:hover {
            background-color: rgba(0, 114, 188, 0.1);
        }

        .typing-indicator {
            display: flex;
            align-items: center;
            padding: 12px 15px;
            background-color: var(--light-gray);
            border-radius: 18px;
            align-self: flex-start;
        }

        .typing-indicator span {
            height: 8px;
            width: 8px;
            background-color: #666;
            border-radius: 50%;
            display: inline-block;
            margin-right: 5px;
            animation: typing 1.3s infinite;
        }

        .typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
        .typing-indicator span:nth-child(3) { animation-delay: 0.4s; margin-right: 0; }

        @keyframes typing {
            0%, 100% { opacity: 0.3; transform: translateY(0); }
            50% { opacity: 1; transform: translateY(-5px); }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="logo">
                <h1>FinSage Pro - Bajaj Finserv Assistant</h1>
            </div>
        </header>
        <main>
            <div class="chat-container">
                <div class="chat-header">
                    <i class="fas fa-robot"></i>
                    <span>Chat with FinSage Pro</span>
                </div>
                <div class="chat-messages" id="chat-messages">
                    <div class="message assistant-message">
                        Hello! I'm FinSage Pro, your Bajaj Finserv Assistant. I can help you with stock price analysis and business information. How can I assist you today?
                    </div>
                </div>
                <div class="chat-input">
                    <input type="text" id="user-input" placeholder="Type your question here..." autocomplete="off">
                    <button id="send-button">
                        <i class="fas fa-paper-plane"></i>
                    </button>
                </div>
            </div>
            <div class="info-panel">
                <h2><i class="fas fa-question-circle"></i> Example Questions</h2>
                <div class="example-query" data-query="What was the highest stock price in 2024?">What was the highest stock price in 2024?</div>
                <div class="example-query" data-query="Show me stock price trends">Show me stock price trends</div>
                <div class="example-query" data-query="What is the average stock price?">What is the average stock price?</div>
                <div class="example-query" data-query="Compare recent performance">Compare recent performance</div>
            </div>
        </main>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const chatMessages = document.getElementById('chat-messages');
            const userInput = document.getElementById('user-input');
            const sendButton = document.getElementById('send-button');
            const exampleQueries = document.querySelectorAll('.example-query');

            sendButton.addEventListener('click', handleUserMessage);
            userInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    handleUserMessage();
                }
            });

            exampleQueries.forEach(query => {
                query.addEventListener('click', function() {
                    userInput.value = this.getAttribute('data-query');
                    handleUserMessage();
                });
            });

            function handleUserMessage() {
                const message = userInput.value.trim();
                if (!message) return;

                addMessage(message, 'user');
                userInput.value = '';

                const typingIndicator = document.createElement('div');
                typingIndicator.className = 'typing-indicator';
                typingIndicator.innerHTML = '<span></span><span></span><span></span>';
                chatMessages.appendChild(typingIndicator);
                chatMessages.scrollTop = chatMessages.scrollHeight;

                processQuery(message)
                    .then(response => {
                        if (typingIndicator && typingIndicator.parentNode) {
                            typingIndicator.parentNode.removeChild(typingIndicator);
                        }
                        addMessage(response.answer, 'assistant', response.sources);
                    })
                    .catch(error => {
                        if (typingIndicator && typingIndicator.parentNode) {
                            typingIndicator.parentNode.removeChild(typingIndicator);
                        }
                        addMessage('Sorry, I encountered an error. Please try again.', 'assistant');
                        console.error('Error:', error);
                    });
            }

            function addMessage(text, sender, sources = []) {
                const messageElement = document.createElement('div');
                messageElement.className = `message ${sender}-message`;
                
                let formattedText = text
                    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                    .replace(/\*(.*?)\*/g, '<em>$1</em>')
                    .replace(/\n/g, '<br>');
                
                messageElement.innerHTML = formattedText;
                
                if (sources && sources.length > 0) {
                    const sourcesElement = document.createElement('div');
                    sourcesElement.className = 'sources';
                    sourcesElement.innerHTML = 'Sources: ' + sources.join(', ');
                    messageElement.appendChild(sourcesElement);
                }
                
                chatMessages.appendChild(messageElement);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }

            async function processQuery(query) {
                try {
                    const response = await fetch('/api/query', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ query: query }),
                    });
                    
                    if (!response.ok) {
                        throw new Error(`HTTP error ${response.status}`);
                    }
                    
                    return await response.json();
                } catch (error) {
                    console.error('Error calling API:', error);
                    throw error;
                }
            }
        });
    </script>
</body>
</html>"""


def setup_application():
    """Setup the application by creating necessary directories and files"""
    ensure_templates_directory()
    create_html_template()
    print("Application setup completed!")
