'use client';
import { useState, useEffect } from 'react';

export default function ChatPage() {
  const [messages, setMessages] = useState([]);
  const [query, setQuery] = useState('');
  const [processing, setProcessing] = useState(false);

  useEffect(() => {
    // Listen for messages from content script
    const handleMessage = (event) => {
      if (event.data.type === 'QUERY_RESPONSE') {
        // Handle response from extension
        console.log('Response received:', event.data.response);
        setProcessing(false);
      }
    };

    window.addEventListener('message', handleMessage);
    return () => window.removeEventListener('message', handleMessage);
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    // Add user message
    setMessages(prev => [...prev, { role: 'user', content: query }]);
    setProcessing(true);

    // Send to content script
    window.parent.postMessage({
      type: 'QUERY_REQUEST',
      query: query,
    }, '*');

    setQuery('');
  };

  return (
    <div className="flex flex-col h-screen max-w-4xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">📄 AskMyDoc</h1>
      <p className="text-gray-600 mb-6">Ask me anything about the PDF you're viewing!</p>
      
      {/* Messages */}
      <div className="flex-1 overflow-y-auto space-y-4 mb-4">
        {messages.map((message, index) => (
          <div key={index} className={`p-3 rounded-lg ${
            message.role === 'user' 
              ? 'bg-blue-100 ml-8' 
              : 'bg-gray-100 mr-8'
          }`}>
            <div className="font-semibold mb-1">
              {message.role === 'user' ? 'You' : 'Assistant'}
            </div>
            <div>{message.content}</div>
          </div>
        ))}
        {processing && (
          <div className="bg-gray-100 mr-8 p-3 rounded-lg">
            <div className="font-semibold mb-1">Assistant</div>
            <div>Processing your question...</div>
          </div>
        )}
      </div>

      {/* Input */}
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask a question about the document..."
          disabled={processing}
          className="flex-1 p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          type="submit"
          disabled={processing || !query.trim()}
          className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50"
        >
          Send
        </button>
      </form>
    </div>
  );
}
