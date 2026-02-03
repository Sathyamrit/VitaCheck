import React from 'react';

const DataPolicy: React.FC = () => {
  return (
    <div className="space-y-12">
      <section>
        <h2 className="text-3xl font-black tracking-tighter text-gray-900 mb-6 uppercase">1. Information We Collect</h2>
        <p className="text-gray-600 font-bold leading-relaxed mb-4">
          To provide accurate vitamin deficiency assessments, VitaCheck collects:
        </p>
        <ul className="grid sm:grid-cols-2 gap-4">
          <li className="p-4 bg-gray-50 rounded-xl border-l-4 border-[#f7a221] font-bold text-sm text-gray-700">
            Symptom Descriptions (NLP Data)
          </li>
          <li className="p-4 bg-gray-50 rounded-xl border-l-4 border-[#f7a221] font-bold text-sm text-gray-700">
            Dermatological & Appendage Signs
          </li>
          <li className="p-4 bg-gray-50 rounded-xl border-l-4 border-[#f7a221] font-bold text-sm text-gray-700">
            Basic Demographics (Age/Gender)
          </li>
          <li className="p-4 bg-gray-50 rounded-xl border-l-4 border-[#f7a221] font-bold text-sm text-gray-700">
            Dietary Restrictions & Habits
          </li>
        </ul>
      </section>

      <section>
        <h2 className="text-3xl font-black tracking-tighter text-gray-900 mb-6 uppercase">2. How the AI Uses Your Data</h2>
        <p className="text-gray-600 font-bold leading-relaxed">
          Your inputs are processed by our <strong>Python Intelligence Layer</strong> using Cosine Similarity to map symptoms to nutritional gaps. 
          We do not sell this data to third parties. It is used exclusively to generate your personalized report and recipe recommendations 
          optimized for nutrient density and bioavailability.
        </p>
      </section>

      <section>
        <h2 className="text-3xl font-black tracking-tighter text-gray-900 mb-6 uppercase">3. Your Rights</h2>
        <p className="text-gray-600 font-bold leading-relaxed mb-6">
          In accordance with GDPR, you have the "Right to be Forgotten." You can delete your health profile and 
          MongoDB records at any time via your user dashboard.
        </p>
      </section>
    </div>
  );
};

export default DataPolicy;