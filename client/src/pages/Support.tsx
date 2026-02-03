import React from 'react';
import SupportHero from '../components/support/SupportHero';
import FAQSection from '../components/support/FAQSection';
import ContactSupport from '../components/support/ContactSupport';

const Support: React.FC = () => {
  return (
    <div className="min-h-screen bg-white animate-in fade-in duration-500">
      <SupportHero />
      
      <main className="max-w-7xl mx-auto py-20 px-6">
        <div className="grid lg:grid-cols-3 gap-16">
          {/* FAQ takes up more space */}
          <div className="lg:col-span-2">
            <FAQSection />
          </div>
          
          {/* Contact and Quick Links sidebar */}
          <div className="lg:col-span-1 space-y-12">
            <ContactSupport />
            <div className="p-8 bg-[#f7a221]/5 rounded-[2rem] border border-[#f7a221]/10">
              <h4 className="text-xl font-black tracking-tighter text-gray-900 mb-4 uppercase">Medical Note</h4>
              <p className="text-sm font-bold text-gray-600 leading-relaxed">
                VitaCheck provides informational assessments based on AI symptom mapping. 
                It is not a substitute for professional clinical diagnosis.[3, 4]
              </p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Support;