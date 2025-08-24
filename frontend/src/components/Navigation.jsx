import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Navigation = () => {
  const location = useLocation();
  
  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <nav className="bg-white shadow-sm border-b">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            <div className="flex-shrink-0 flex items-center">
              <h1 className="text-xl font-bold text-gray-900">🏨 Guest Relations</h1>
            </div>
            <div className="hidden sm:ml-8 sm:flex sm:space-x-8">
              <Link
                to="/cases"
                className={`inline-flex items-center px-3 py-2 border-b-2 text-sm font-medium transition-colors ${
                  isActive('/cases')
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
                }`}
              >
                📋 Cases
              </Link>
              <Link
                to="/followups"
                className={`inline-flex items-center px-3 py-2 border-b-2 text-sm font-medium transition-colors ${
                  isActive('/followups')
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
                }`}
              >
                💬 Followups
              </Link>
              <Link
                to="/upload"
                className={`inline-flex items-center px-3 py-2 border-b-2 text-sm font-medium transition-colors ${
                  isActive('/upload')
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
                }`}
              >
                📄 Upload
              </Link>
            </div>
          </div>
          
          {/* Mobile menu button */}
          <div className="sm:hidden flex items-center">
            <button className="text-gray-500 hover:text-gray-700">
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navigation; 