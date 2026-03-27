import React from 'react';

const Story: React.FC = () => {
  const barriers = [
    { title: 'Cost', desc: 'Affordable micronutrient testing for everyone' },
    { title: 'Fear', desc: 'Simple, non-invasive testing process' },
    { title: 'Awareness', desc: 'Education about micronutrient deficiencies' }
  ];

  return (
    <section className="grid md:grid-cols-2 gap-16 items-center mb-24">
      <div>
        <h2 className="text-4xl font-bold tracking-tighter mb-6 text-gray-900">Why we built VitaCheck</h2>
        <p className="text-lg text-gray-600 leading-relaxed mb-6">
          Micronutrient deficiencies affect billions silently—causing brain fog, fatigue, weakened immunity, and poor wound healing. 
          Yet clinical testing is expensive, inaccessible, or dismissed as "just getting older." Traditional medicine overlooks 
          subclinical deficiencies until they become serious health crises.
        </p>
        <p className="text-lg text-gray-600 leading-relaxed">
          VitaCheck uses advanced AI reasoning to bridge this gap—providing evidence-based micronutrient insights without 
          blood tests, making prevention accessible to everyone.
        </p>
      </div>

      <div className="grid gap-4">
        {barriers.map((item, i) => (
          <div key={i} className="p-6 border-l-4 border-[#f7a221] bg-orange-50/30 rounded-r-xl">
            <h4 className="font-bold text-gray-900 mb-1">{item.title}</h4>
            <p className="text-sm text-gray-600">{item.desc}</p>
          </div>
        ))}
      </div>
    </section>
  );
};

export default Story;