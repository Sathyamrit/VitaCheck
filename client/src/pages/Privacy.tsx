import React from 'react';
import PrivacyHero from '../components/privacy/PrivacyHero';
import DataPolicy from '../components/privacy/DataPolicy';
import ComplianceSection from '../components/privacy/ComplianceSection';

const Privacy: React.FC = () => {
  return (
    <div className="min-h-screen bg-white animate-in fade-in duration-700">
      <PrivacyHero />
      
      <main className="max-w-6xl mx-auto py-24 px-6">
        <div className="grid lg:grid-cols-3 gap-16">
          {/* Main Policy Content */}
          <div className="lg:col-span-2 space-y-16">
            <DataPolicy />
          </div>
          
          {/* Compliance Sidebar */}
          <div className="lg:col-span-1">
            <ComplianceSection />
          </div>
        </div>
      </main>
    </div>
  );
};

export default Privacy;