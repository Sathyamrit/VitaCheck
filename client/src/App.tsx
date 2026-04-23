import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Navbar from './components/layout/Navbar';
import Footer from './components/layout/Footer';
import Hero from './components/home/Hero';
import InfoSection from './components/home/InfoSection';
import AboutUs from './pages/AboutUs';
import AboutVitacheck from './pages/AboutVitacheck';
import Support from './pages/Support';
import Contact from './pages/Contact';
import Privacy from './pages/Privacy';
import Auth from './pages/Auth';
import Dashboard from './pages/Dashboard';
import MealPlan from './pages/MealPlan';
import { DiagnosticDashboard } from './pages/DiagnosticDashboard';
import { Diagnostic } from './pages/Diagnostic';
import RAGDashboard from './components/RAGDashboard/RAGDashboard';
import RecipeDetails from './components/RecipeDetails/RecipeDetails';

function App() {
  return (
    <div className="flex flex-col min-h-screen bg-white font-sans antialiased text-gray-900">
      <Navbar />
      
      <main className="flex-grow">
        <Routes>
          <Route path="/" element={<><Hero /><InfoSection /></>} />
          <Route path="/about-us" element={<AboutUs />} />
          <Route path="/about-vitacheck" element={<AboutVitacheck />} />
          <Route path="/support" element={<Support />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="/privacy" element={<Privacy />} />
          <Route path="/auth" element={<Auth />} />
          <Route path="/questionnaire" element={<DiagnosticDashboard />} />
          <Route path="/diagnostic" element={<Diagnostic />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/dashboard/:taskId" element={<Dashboard />} />
          <Route path="/meal-plan" element={<MealPlan />} />
          <Route path="/meal-plan/:taskId" element={<MealPlan />} />
          <Route path="/diagnostic-dashboard" element={<DiagnosticDashboard />} />
          <Route path="/rag-dashboard" element={<RAGDashboard />} />
          <Route path="/meal-plan/recipe/:index" element={<RecipeDetails />} />
        </Routes>
      </main>

      <Footer />
    </div>
  );
}

export default App;