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
          A significant portion of the global population experiences chronic fatigue, weakened immunity, and 
          cognitive difficulties without understanding the cause. Research shows these often stem 
          from simple micronutrient deficiencies.[1, 2]
        </p>
        <p className="text-lg text-gray-600 leading-relaxed">
          VitaCheck was born to break down the barriers of cost, fear, and awareness that prevent 
          people from getting the care they need.[3, 4]
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