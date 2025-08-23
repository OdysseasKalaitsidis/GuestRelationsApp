import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import UploadPage from "./pages/UploadPage";
import CasesPage from "./pages/CasesPage";

function App() {
  return (
    <Router>
      <nav className="p-4 bg-gray-800 text-white">
        <Link to="/upload" className="mr-4">
          Upload PDF
        </Link>
        <Link to="/cases">Cases</Link>
      </nav>

      <Routes>
        <Route path="/upload" element={<UploadPage />} />
        <Route path="/cases" element={<CasesPage />} />
      </Routes>
    </Router>
  );
}

export default App;
