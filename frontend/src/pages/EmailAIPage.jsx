import React, { useState, useRef, useEffect } from 'react';
import { chatWithEmailAssistant, isAuthenticated } from '../services/api';

const EmailAIPage = () => {
  const [emailContent, setEmailContent] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [conversation, setConversation] = useState([]);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [conversation]);

  const handleChatSubmit = async (e) => {
    e.preventDefault();
    if (!emailContent.trim()) {
      setError('Please enter email content');
      return;
    }

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: emailContent,
      timestamp: new Date()
    };

    // Add user message to conversation
    setConversation(prev => [...prev, userMessage]);
    setEmailContent('');
    setError('');

    try {
      setIsLoading(true);
      const response = await chatWithEmailAssistant(emailContent);
      
      const aiMessage = {
        id: Date.now() + 1,
        type: 'ai',
        content: response.response,
        timestamp: new Date()
      };

      // Add AI response to conversation
      setConversation(prev => [...prev, aiMessage]);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const copyToClipboard = (text, messageId) => {
    navigator.clipboard.writeText(text);
    // Simple feedback
    const button = document.getElementById(`copy-btn-${messageId}`);
    if (button) {
      const originalText = button.textContent;
      button.textContent = '✅ Copied!';
      setTimeout(() => {
        button.textContent = originalText;
      }, 2000);
    }
  };

  const clearConversation = () => {
    setConversation([]);
    setEmailContent('');
    setError('');
  };

  // Don't render if user is not authenticated
  if (!isAuthenticated()) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Authentication Required</h1>
          <p className="text-gray-600">Please login to access the Email AI Assistant.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="max-w-4xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            🤖 Email AI Assistant
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Paste guest emails and get AI-powered responses using RAG technology
          </p>
        </div>

        {/* Chat Interface */}
        <div className="bg-white rounded-xl shadow-lg overflow-hidden">
          {/* Chat Header */}
          <div className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white p-4 flex items-center justify-between">
            <div className="flex items-center">
              <span className="text-2xl mr-3">💬</span>
              <div>
                <h2 className="text-xl font-semibold">Email Assistant Chat</h2>
                <p className="text-blue-100 text-sm">Powered by RAG technology</p>
              </div>
            </div>
            <button
              onClick={clearConversation}
              className="bg-white/20 hover:bg-white/30 text-white px-3 py-1 rounded-lg text-sm font-medium transition-colors"
            >
              🗑️ Clear Chat
            </button>
          </div>

          {/* Messages Area */}
          <div className="h-96 overflow-y-auto p-4 space-y-4">
            {conversation.length === 0 ? (
              <div className="text-center py-12">
                <div className="text-6xl mb-4">💭</div>
                <p className="text-gray-500 text-lg">Start a conversation</p>
                <p className="text-gray-400 text-sm mt-2">Paste a guest email below to get an AI response</p>
              </div>
            ) : (
              conversation.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-3xl px-4 py-3 rounded-lg ${
                      message.type === 'user'
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-100 text-gray-800 border'
                    }`}
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center mb-2">
                          <span className="text-sm mr-2">
                            {message.type === 'user' ? '👤 You' : '🤖 AI Assistant'}
                          </span>
                          <span className="text-xs opacity-70">
                            {message.timestamp.toLocaleTimeString()}
                          </span>
                        </div>
                        <div className="whitespace-pre-wrap text-sm leading-relaxed">
                          {message.content}
                        </div>
                      </div>
                      {message.type === 'ai' && (
                        <button
                          id={`copy-btn-${message.id}`}
                          onClick={() => copyToClipboard(message.content, message.id)}
                          className="ml-3 bg-blue-100 hover:bg-blue-200 text-blue-700 px-2 py-1 rounded text-xs font-medium transition-colors"
                        >
                          📋 Copy
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              ))
            )}
            
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-gray-100 text-gray-800 border px-4 py-3 rounded-lg">
                  <div className="flex items-center">
                    <svg className="animate-spin -ml-1 mr-3 h-4 w-4 text-gray-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    <span className="text-sm">AI is thinking...</span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="border-t p-4">
            <form onSubmit={handleChatSubmit} className="space-y-3">
              <div>
                <textarea
                  value={emailContent}
                  onChange={(e) => setEmailContent(e.target.value)}
                  placeholder="Paste the guest email content here..."
                  className="w-full h-24 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                  required
                />
              </div>
              
              <div className="flex justify-between items-center">
                <div className="text-sm text-gray-500">
                  {conversation.length > 0 && `${conversation.length} message${conversation.length !== 1 ? 's' : ''} in conversation`}
                </div>
                <button
                  type="submit"
                  disabled={isLoading}
                  className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-6 py-2 rounded-lg hover:from-blue-700 hover:to-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium transition-all duration-200 flex items-center"
                >
                  {isLoading ? (
                    <>
                      <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Processing...
                    </>
                  ) : (
                    <>
                      ✨ Get AI Response
                    </>
                  )}
                </button>
              </div>
            </form>

            {error && (
              <div className="mt-3 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
                {error}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default EmailAIPage;
