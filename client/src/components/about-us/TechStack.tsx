import React from 'react';

const TechStack: React.FC = () => {
  return (
    <section className="py-24 px-6 bg-white">
      <div className="max-w-4xl mx-auto">
        <h2 className="text-4xl font-black tracking-tighter text-gray-900 mb-12 uppercase text-center">Inside the AI Brain</h2>
        <div className="space-y-12">
          <div className="flex gap-8 items-start">
            <span className="text-4xl font-black text-[#f7a221] opacity-30">01</span>
            <div>
              <h3 className="text-2xl font-bold text-gray-900 tracking-tight mb-2">NLP Symptom Extraction</h3>
              <p className="text-gray-600 font-medium leading-relaxed">
                Using Natural Language Processing, our Python service parses free-text inputs like "sandpaper skin" 
                and maps them to clinical entities like follicular hyperkeratosis.
              </p>
            </div>
          </div>
          <div className="flex gap-8 items-start">
            <span className="text-4xl font-black text-[#f7a221] opacity-30">02</span>
            <div>
              <h3 className="text-2xl font-bold text-gray-900 tracking-tight mb-2">Vector-Based Prediction</h3>
              <p className="text-gray-600 font-medium leading-relaxed">
                We utilize Cosine Similarity to compare your symptom profile against a global clinical database 
                to calculate a similarity score for 13 essential vitamins and key minerals.
              </p>
            </div>
          </div>
          <div className="flex gap-8 items-start">
            <span className="text-4xl font-black text-[#f7a221] opacity-30">03</span>
            <div>
              <h3 className="text-2xl font-bold text-gray-900 tracking-tight mb-2">Algorithmic Recipe Closure</h3>
              <p className="text-gray-600 font-medium leading-relaxed">
                The system maps identified gaps to high-density food sources, prioritizing bioavailability—ensuring 
                iron sources are paired with Vitamin C for maximum absorption.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default TechStack;