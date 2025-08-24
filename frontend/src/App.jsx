import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import CasesPage from './pages/CasesPage';
import FollowupsPage from './pages/FollowupsPage';
import UploadPage from './pages/UploadPage';
import Navigation from './components/Navigation';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Navigation />
        <Routes>
          <Route path="/" element={<Navigate to="/cases" replace />} />
          <Route path="/cases" element={<CasesPage />} />
          <Route path="/followups" element={<FollowupsPage />} />
          <Route path="/upload" element={<UploadPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
