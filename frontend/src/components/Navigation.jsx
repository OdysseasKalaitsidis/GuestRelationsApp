import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Navigation = ({ user, onLogout }) => {
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
        to="/tasks"
        className={`inline-flex items-center px-3 py-2 border-b-2 text-sm font-medium transition-colors ${
          isActive('/tasks')
            ? 'border-blue-500 text-blue-600'
            : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
        }`}
      >
        📋 Tasks
      </Link>
      <Link
        to="/email-ai"
        className={`inline-flex items-center px-3 py-2 border-b-2 text-sm font-medium transition-colors ${
          isActive('/email-ai')
            ? 'border-blue-500 text-blue-600'
            : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
        }`}
      >
        🤖 Email AI
      </Link>
            </div>
          </div>
          
          {/* User info and logout */}
          <div className="flex items-center space-x-4">
            <div className="hidden sm:block">
              <span className="text-sm text-gray-700">
                Welcome, <span className="font-medium">{user?.name}</span>
                {user?.is_admin && <span className="ml-1 px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-full">Admin</span>}
              </span>
            </div>
            <button
              onClick={onLogout}
              className="text-sm text-gray-500 hover:text-gray-700 px-3 py-2 rounded-md hover:bg-gray-100"
            >
              Logout
            </button>
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