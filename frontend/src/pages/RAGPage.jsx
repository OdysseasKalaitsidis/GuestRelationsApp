import React, { useState, useEffect, useRef } from 'react';
import { chatWithAI, getCollectionStats } from '../services/api';

const RAGPage = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [collectionStats, setCollectionStats] = useState(null);
  const messagesEndRef = useRef(null);

  // Load collection stats on component mount
  useEffect(() => {
    loadCollectionStats();
    // Add welcome message
    setMessages([{
      id: 1,
      type: 'ai',
      content: 'Hello! I\'m your AI assistant for guest relations. I can help you with hotel policies, procedures, and guest relations. How can I assist you today?',
      timestamp: new Date()
    }]);
  }, []);

  // Scroll to bottom when new messages are added
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const loadCollectionStats = async () => {
    try {
      const stats = await getCollectionStats();
      setCollectionStats(stats);
    } catch (err) {
      console.error('Failed to load collection stats:', err);
    }
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || loading) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputMessage.trim(),
      timestamp: new Date()
    };

    // Add user message immediately
    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setLoading(true);
    setError(null);

    try {
      // Prepare messages for API (only role and content)
      const apiMessages = [
        ...messages.map(msg => ({
          role: msg.type === 'user' ? 'user' : 'assistant',
          content: msg.content
        })),
        {
          role: 'user',
          content: userMessage.content
        }
      ];

      const response = await chatWithAI(apiMessages);
      
      const aiMessage = {
        id: Date.now() + 1,
        type: 'ai',
        content: response.reply,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (err) {
      console.error('Chat failed:', err);
      setError(`Failed to get AI response: ${err.message}`);
      
      // Add error message
      const errorMessage = {
        id: Date.now() + 1,
        type: 'ai',
        content: 'I apologize, but I encountered an error. Please try again.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="w-full px-4 py-8 max-w-4xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl lg:text-3xl font-bold text-main mb-2">AI Assistant</h1>
        <p className="text-third">
          Chat with your AI assistant for hotel policies, procedures, and guest relations
        </p>
      </div>

      {/* Collection Stats */}
      {collectionStats && (
        <div className="mb-6">
          <div className="bg-white rounded-lg shadow p-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-2">
                  <span className="text-2xl">📚</span>
                  <span className="text-sm text-third">
                    {collectionStats.total_chunks} training documents loaded
                  </span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className={`w-2 h-2 rounded-full ${
                    collectionStats.status === 'active' ? 'bg-green-500' : 'bg-yellow-500'
                  }`}></div>
                  <span className="text-sm text-third capitalize">{collectionStats.status}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Chat Interface */}
      <div className="bg-white rounded-lg shadow-lg h-[600px] flex flex-col">
        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] rounded-lg p-4 ${
                  message.type === 'user'
                    ? 'bg-secondary text-white'
                    : 'bg-third bg-opacity-10 text-main'
                }`}
              >
                <div className="whitespace-pre-wrap">{message.content}</div>
                <div className={`text-xs mt-2 ${
                  message.type === 'user' ? 'text-white text-opacity-70' : 'text-third'
                }`}>
                  {message.timestamp.toLocaleTimeString()}
                </div>
              </div>
            </div>
          ))}
          
          {/* Loading indicator */}
          {loading && (
            <div className="flex justify-start">
              <div className="bg-third bg-opacity-10 rounded-lg p-4">
                <div className="flex items-center space-x-2">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-secondary"></div>
                  <span className="text-third">AI is thinking...</span>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="border-t border-third p-4">
          <div className="flex space-x-3">
            <textarea
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message here... (Press Enter to send, Shift+Enter for new line)"
              className="flex-1 px-3 py-2 border border-third rounded-lg focus:outline-none focus:ring-2 focus:ring-secondary focus:border-transparent resize-none"
              rows={2}
              disabled={loading}
            />
            <button
              onClick={handleSendMessage}
              disabled={loading || !inputMessage.trim()}
              className="bg-secondary text-white px-6 py-2 rounded-lg hover:bg-secondary hover:bg-opacity-80 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
            >
              <span>📤</span>
              <span>Send</span>
            </button>
          </div>
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="mt-6 bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex items-center space-x-2">
            <span className="text-red-500 text-xl">⚠️</span>
            <p className="text-red-800">{error}</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default RAGPage;
