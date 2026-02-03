import React, { useState } from 'react';
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

type Page = 'home' | 'about-us' | 'about-vitacheck' | 'support' | 'contact' | 'privacy' | 'auth';

function App() {
  const [currentPage, setCurrentPage] = useState<Page>('home');

  const renderContent = () => {
    switch (currentPage) {
      case 'about-us':
        return <AboutUs />;
      case 'about-vitacheck':
        return <AboutVitacheck />;
      case 'support':
        return <Support />;
      case 'contact':
        return <Contact />;
      case 'privacy':
        return <Privacy />;
      case 'auth':
        return <Auth />;
      default:
        return (
          <>
            <Hero onStart={() => setCurrentPage('about-vitacheck')} />
            <InfoSection />
          </>
        );
    }
  };

  return (
    <div className="flex flex-col min-h-screen bg-white font-sans antialiased text-gray-900">
      <Navbar onNavigate={setCurrentPage} activePage={currentPage} />
      
      <main className="flex-grow">
        {renderContent()}
      </main>

      <Footer />
    </div>
  );
}

export default App;