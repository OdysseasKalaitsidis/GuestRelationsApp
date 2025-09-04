import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Navigation = ({ user, onLogout }) => {
  const location = useLocation();
  
  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <nav className="bg-white shadow-sm border-b border-third">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            <div className="flex-shrink-0 flex items-center">
              <div className="flex items-center space-x-2">
                <img src="/docg.png" alt="Guest Relations" className="h-8 w-8" />
                <h1 className="text-xl font-bold text-main">Guest Relations</h1>
              </div>
            </div>
            <div className="hidden sm:ml-8 sm:flex sm:space-x-8">
              <Link
                to="/cases"
                className={`inline-flex items-center px-3 py-2 border-b-2 text-sm font-medium transition-colors ${
                  isActive('/cases')
                    ? 'border-secondary text-secondary'
                    : 'border-transparent text-third hover:border-third hover:text-main'
                }`}
              >
                📋 Cases
              </Link>
              <Link
                to="/followups"
                className={`inline-flex items-center px-3 py-2 border-b-2 text-sm font-medium transition-colors ${
                  isActive('/followups')
                    ? 'border-secondary text-secondary'
                    : 'border-transparent text-third hover:border-third hover:text-main'
                }`}
              >
                💬 Followups
              </Link>
            </div>
          </div>
          
          {/* User info and logout */}
          <div className="flex items-center space-x-4">
            <div className="hidden sm:block">
              <span className="text-sm text-main">
                Welcome, <span className="font-medium">{user?.name}</span>
                {user?.is_admin && <span className="ml-1 px-2 py-1 text-xs bg-secondary bg-opacity-20 text-secondary rounded-full">Admin</span>}
              </span>
            </div>
            <button
              onClick={onLogout}
              className="text-sm text-third hover:text-main px-3 py-2 rounded-md hover:bg-third hover:bg-opacity-10"
            >
              Logout
            </button>
          </div>
          
          {/* Mobile menu button */}
          <div className="sm:hidden flex items-center">
            <button className="text-third hover:text-main">
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