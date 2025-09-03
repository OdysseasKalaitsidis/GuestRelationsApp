import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import CasesPage from './pages/CasesPage';
import FollowupsPage from './pages/FollowupsPage';
import TasksPage from './pages/TasksPage';
import Navigation from './components/Navigation';
import AuthModal from './components/AuthModal';
import { isAuthenticated, getCurrentUser, logout } from './services/api';

// Protected Route Component
const ProtectedRoute = ({ children, user }) => {
  if (!user) {
    return <Navigate to="/auth" replace />;
  }
  return children;
};

// Auth Page Component
const AuthPage = ({ onLoginSuccess }) => {
  const [showAuthModal, setShowAuthModal] = useState(true);

  const handleLoginSuccess = (userData) => {
    onLoginSuccess(userData);
    setShowAuthModal(false);
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-800 mb-4">Guest Relations System</h1>
        <p className="text-gray-600 mb-6">Please login to access the system</p>
        <button
          onClick={() => setShowAuthModal(true)}
          className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600"
        >
          Login
        </button>
      </div>
      <AuthModal
        isOpen={showAuthModal}
        onClose={() => setShowAuthModal(false)}
        onLoginSuccess={handleLoginSuccess}
      />
    </div>
  );
};

// Main App Layout Component
const AppLayout = ({ user, onLogout }) => {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation user={user} onLogout={onLogout} />
      <Routes>
        <Route path="/" element={<Navigate to="/cases" replace />} />
        <Route 
          path="/cases" 
          element={
            <ProtectedRoute user={user}>
              <CasesPage />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/followups" 
          element={
            <ProtectedRoute user={user}>
              <FollowupsPage />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/tasks" 
          element={
            <ProtectedRoute user={user}>
              <TasksPage user={user} />
            </ProtectedRoute>
          } 
        />
        <Route path="*" element={<Navigate to="/cases" replace />} />
      </Routes>
    </div>
  );
};

function App() {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check if user is already authenticated
    const checkAuth = async () => {
      try {
        if (isAuthenticated()) {
          const currentUser = getCurrentUser();
          if (currentUser) {
            setUser(currentUser);
          } else {
            // If token exists but no user data, clear invalid auth
            logout();
          }
        }
      } catch (error) {
        console.error('Auth check error:', error);
        logout();
      } finally {
        setIsLoading(false);
      }
    };
    
    checkAuth();
  }, []);

  const handleLoginSuccess = (userData) => {
    setUser(userData);
  };

  const handleLogout = () => {
    logout();
    setUser(null);
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <Router>
      <Routes>
        <Route 
          path="/auth" 
          element={
            user ? <Navigate to="/cases" replace /> : <AuthPage onLoginSuccess={handleLoginSuccess} />
          } 
        />
        <Route 
          path="/*" 
          element={
            user ? <AppLayout user={user} onLogout={handleLogout} /> : <Navigate to="/auth" replace />
          } 
        />
      </Routes>
    </Router>
  );
}

export default App;
