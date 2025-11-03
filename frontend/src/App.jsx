import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/layout/Layout';
import Home from './pages/Home';
import TechSOPs from './pages/TechSOPs';
import Kubernetes from './pages/Kubernetes';
import GCP from './pages/GCP';
import RAG from './pages/RAG';
import CaseStudies from './pages/CaseStudies';
import About from './pages/About';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="tech-sops" element={<TechSOPs />} />
          <Route path="kubernetes" element={<Kubernetes />} />
          <Route path="gcp" element={<GCP />} />
          <Route path="rag" element={<RAG />} />
          <Route path="case-studies" element={<CaseStudies />} />
          <Route path="about" element={<About />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
