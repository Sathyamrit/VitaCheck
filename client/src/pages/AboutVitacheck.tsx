import React from 'react';
import Story from '../components/about-vitacheck/Story';
import Values from '../components/about-vitacheck/Values';

const About: React.FC = () => {
  return (
    <div className="bg-white">
      {/* Hero Header */}
      <section className="bg-[#f7a221] py-20 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-5xl md:text-6xl font-extrabold text-gray-900 tracking-tighter mb-6">
            Our Mission
          </h1>
          <p className="text-xl md:text-2xl text-gray-800 font-medium leading-relaxed">
            Democratizing nutritional health through accessible, AI-driven insights 
            and evidence-based lifestyle adjustments.
          </p>
        </div>
      </section>

      <main className="max-w-6xl mx-auto py-16 px-6">
        <Story />
        <Values />
        
        {/* Call to Action */}
        <section className="mt-20 p-12 bg-gray-50 rounded-3xl text-center border border-gray-100">
          <h2 className="text-3xl font-bold tracking-tight mb-4 text-gray-900">
            Ready to check your vitality?
          </h2>
          <p className="text-gray-600 mb-8 max-w-lg mx-auto">
            Join thousands of users who have taken control of their health 
            using our intelligent symptom analysis.
          </p>
          <button className="bg-blue-600 text-white px-10 py-4 rounded-full font-bold hover:bg-blue-700 transition-all shadow-lg shadow-blue-200">
            Start Free Assessment
          </button>
        </section>
      </main>
    </div>
  );
};

export default About;