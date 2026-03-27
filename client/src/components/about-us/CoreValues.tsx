import React from 'react';

const CoreValues: React.FC = () => {
  const values = [
    {
      id: '01',
      title: 'ADVANCED REASONING',
      desc: 'DeepSeek R1 8B analyzes micronutrients with deep clinical reasoning. Every recommendation comes with transparent multi-step justification.',
      citation: ''
    },
    {
      id: '02',
      title: 'GROUNDED IN EVIDENCE',
      desc: 'RAG-powered knowledge retrieval ensures every diagnosis is anchored in medical context. Our vector database stores only evidence-based micronutrient science.',
      citation: ''
    },
    {
      id: '03',
      title: 'SAFETY FIRST',
      desc: 'Automatic drug-nutrient interaction detection, toxic dose prevention, and medication depletion screening protect you before recommendations.',
      citation: ''
    },
    {
      id: '04',
      title: 'HOLISTIC CLOSURE',
      desc: 'We don’t just identify gaps. We provide a path to recovery through bioavailable, customized recipes that turn data into health.',
      citation: ''
    }
  ];

  return (
    <section className="py-24 px-6 bg-white border-t border-gray-100">
      <div className="max-w-7xl mx-auto">
        <div className="flex flex-col md:flex-row justify-between items-end mb-16 gap-6">
          <h2 className="text-5xl md:text-7xl font-black tracking-tighter text-gray-900 leading-none">
            OUR CORE <br /> <span className="text-[#f7a221]">PRINCIPLES.</span>
          </h2>
          <p className="max-w-md text-lg font-bold text-gray-500 tracking-tight leading-snug">
            VitaCheck is built on a foundation of clinical integrity and user-centric 
            design to change the narrative of preventive healthcare.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
          {values.map((item) => (
            <div 
              key={item.id} 
              className="group p-8 bg-gray-50 hover:bg-[#f7a221] transition-all duration-500 rounded-[2rem] border border-gray-100 flex flex-col justify-between min-h-[320px]"
            >
              <div>
                <span className="text-5xl font-black opacity-10 group-hover:opacity-100 group-hover:text-white transition-all duration-500 leading-none">
                  {item.id}
                </span>
                <h3 className="mt-6 text-2xl font-black tracking-tighter text-gray-900 group-hover:text-white transition-colors duration-500 uppercase">
                  {item.title}
                </h3>
              </div>
              <div>
                <p className="text-sm font-bold text-gray-600 group-hover:text-white/90 transition-colors duration-500 leading-relaxed mb-2">
                  {item.desc}
                </p>
                <span className="text-[10px] font-black text-[#f7a221] group-hover:text-white transition-colors duration-500">
                  REF: {item.citation}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default CoreValues;