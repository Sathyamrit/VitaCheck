import React from 'react';
import ContactHero from '../components/contact/ContactHero';
import ContactForm from '../components/contact/ContactForm';
import ContactDetails from '../components/contact/ContactDetails';

const Contact: React.FC = () => {
  return (
    <div className="min-h-screen bg-white animate-in fade-in duration-700">
      <ContactHero />
      
      <main className="max-w-7xl mx-auto py-24 px-6">
        <div className="grid lg:grid-cols-2 gap-20 items-start">
          {/* Left Side: Interactive Form */}
          <section>
            <h2 className="text-4xl font-black tracking-tighter text-gray-900 mb-10 uppercase leading-none">
              Send us a <br /><span className="text-[#f7a221]">Message.</span>
            </h2>
            <ContactForm />
          </section>

          {/* Right Side: Direct Contact & Support info */}
          <ContactDetails />
        </div>
      </main>
    </div>
  );
};

export default Contact;