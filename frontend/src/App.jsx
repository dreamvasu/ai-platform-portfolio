import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { HelmetProvider } from 'react-helmet-async';
import GoogleAnalytics from './components/GoogleAnalytics';
import Layout from './components/layout/Layout';
import Home from './pages/Home';
import TechSOPs from './pages/TechSOPs';
import Kubernetes from './pages/Kubernetes';
import GCP from './pages/GCP';
import RAG from './pages/RAG';
import CaseStudies from './pages/CaseStudies';
import About from './pages/About';
import Papers from './pages/Papers';
import BlogDetail from './pages/BlogDetail';
import HADR from './pages/HADR';

function App() {
  return (
    <HelmetProvider>
      <Router>
        <GoogleAnalytics />
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<Home />} />
            <Route path="tech-sops" element={<TechSOPs />} />
            <Route path="papers" element={<Papers />} />
            <Route path="blog/:slug" element={<BlogDetail />} />
            <Route path="kubernetes" element={<Kubernetes />} />
            <Route path="gcp" element={<GCP />} />
            <Route path="rag" element={<RAG />} />
            <Route path="hadr" element={<HADR />} />
            <Route path="case-studies" element={<CaseStudies />} />
            <Route path="about" element={<About />} />
          </Route>
        </Routes>
      </Router>
    </HelmetProvider>
  );
}

export default App;
