import React from 'react';

type Point = {
  title: string;
  desc: string;
};

const ProblemScope: React.FC = () => {
  const points: Point[] = [
    { title: "Subclinical Deficiency", desc: "No visible symptoms, but cellular processes are impaired." },
    { title: "Biochemical Alterations", desc: "Enzyme activities and metabolic pathways are disrupted." },
    { title: "Functional Impairment", desc: "Reduced immunity, cognitive decline, and fatigue set in." },
    { title: "Clinical Manifestation", desc: "Physical symptoms like anemia, poor wound healing, and more appear." }
  ];

  return (
    <section className="py-24 px-6 bg-white border-b border-gray-100">
      <div className="max-w-6xl mx-auto grid md:grid-cols-2 gap-16 items-center">
        <div>
          <h2 className="text-4xl font-black tracking-tighter text-gray-900 mb-6 uppercase">The Invisible Crisis</h2>
          <p className="text-lg text-gray-600 leading-relaxed mb-6 font-medium">
            Micronutrient deficiencies are systemic disruptions that manifest through a hierarchical cascade of physiological signs. 
            By the time clinical symptoms appear, the body has often been struggling for months.
          </p>
          <div className="h-2 w-24 bg-[#f7a221]" />
        </div>
        <div className="grid sm:grid-cols-2 gap-6">
          {points.map((point: Point, idx: number) => (
            <div key={idx} className="p-6 bg-gray-50 rounded-2xl border border-gray-100">
              <h4 className="font-bold text-gray-900 mb-2 tracking-tight">{point.title}</h4>
              <p className="text-sm text-gray-500 leading-snug font-medium">{point.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default ProblemScope;