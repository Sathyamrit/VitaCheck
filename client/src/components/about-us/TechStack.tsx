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
              <h3 className="text-2xl font-bold text-gray-900 tracking-tight mb-2">RAG-Powered Symptom Analysis</h3>
              <p className="text-gray-600 font-medium leading-relaxed">
                Our streaming API uses Retrieval-Augmented Generation to ground symptom analysis in medical knowledge. 
                Free-text inputs like "extreme fatigue and brain fog" are processed with real-time medical context retrieval.
              </p>
            </div>
          </div>
          <div className="flex gap-8 items-start">
            <span className="text-4xl font-black text-[#f7a221] opacity-30">02</span>
            <div>
              <h3 className="text-2xl font-bold text-gray-900 tracking-tight mb-2">Advanced Multi-Step Reasoning</h3>
              <p className="text-gray-600 font-medium leading-relaxed">
                DeepSeek R1 8B analyzes your profile against 33 micronutrients (14 vitamins + 20 minerals) stored in ChromaDB. 
                The AI reasons through symptom clusters, biochemistry, and risk factors to identify the most likely deficiencies.
              </p>
            </div>
          </div>
          <div className="flex gap-8 items-start">
            <span className="text-4xl font-black text-[#f7a221] opacity-30">03</span>
            <div>
              <h3 className="text-2xl font-bold text-gray-900 tracking-tight mb-2">Drug & Nutrient Interaction Detection</h3>
              <p className="text-gray-600 font-medium leading-relaxed">
                We automatically check your medications for nutrient depletions and cross-reference your supplements for interactions. 
                Safety guardrails prevent toxic doses and contraindications before you even start.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default TechStack;