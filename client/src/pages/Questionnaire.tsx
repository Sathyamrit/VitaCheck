import React, { useState } from 'react';

const categories = [
  { id: 'skin', name: 'Skin', symptoms: ['Dry skin', 'Rashes', 'Pale complexion'] },
  { id: 'oral', name: 'Mouth & Teeth', symptoms: ['Mouth ulcers', 'Bleeding gums', 'Tooth decay'] },
  { id: 'nails', name: 'Hands & Nails', symptoms: ['Brittle nails', 'Pale nails', 'Ridged nails'] },
  { id: 'neuro', name: 'Neurological', symptoms: ['Numbness', 'Tingling', 'Fatigue'] }
];

const Questionnaire: React.FC = () => {
  const [step, setStep] = useState(0);
  const [responses, setResponses] = useState<Record<string, number>>({});

  const handleScore = (symptom: string, score: number) => {
    setResponses({...responses, [symptom]: score });
  };

  return (
    <div className="min-h-screen bg-white py-24 px-6">
      <div className="max-w-3xl mx-auto">
        {/* Progress Indicator */}
        <div className="flex gap-2 mb-12">
          {categories.map((_, i) => (
            <div key={i} className={`h-1 flex-grow rounded-full ${i <= step? 'bg-[#f7a221]' : 'bg-gray-100'}`} />
          ))}
        </div>

        <h1 className="text-5xl font-black tracking-tighter text-gray-900 mb-4 uppercase leading-none">
          {categories[step].name}
        </h1>
        <p className="text-gray-500 font-bold mb-10 text-sm italic underline">
          Rate symptoms for the PAST 30 DAYS (0 = Never, 4 = Frequent/Severe).[1, 2]
        </p>

        <div className="space-y-8 mb-12">
          {categories[step].symptoms.map((symptom) => (
            <div key={symptom} className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-6 bg-gray-50 rounded-3xl border border-gray-100">
              <span className="font-black text-lg tracking-tight uppercase">{symptom}</span>
              <div className="flex gap-2">
                {[0, 1, 2, 3, 4].map((num) => (
                  <button
                    key={num}
                    onClick={() => handleScore(symptom, num)}
                    className={`w-10 h-10 rounded-full font-black text-xs transition-all ${
                      responses[symptom] === num? 'bg-[#f7a221] text-white scale-110' : 'bg-white text-gray-400 hover:bg-gray-100'
                    }`}
                  >
                    {num}
                  </button>
                ))}
              </div>
            </div>
          ))}
        </div>

        <div className="flex justify-between">
          {step > 0 && (
            <button onClick={() => setStep(step - 1)} className="font-black uppercase tracking-widest text-gray-400">Back</button>
          )}
          <button 
            onClick={() => step < categories.length - 1? setStep(step + 1) : console.log("Final Data:", responses)}
            className="ml-auto bg-gray-900 text-white px-10 py-4 rounded-full font-black uppercase tracking-widest hover:bg-blue-600 transition-all shadow-xl"
          >
            {step === categories.length - 1? 'Generate Report' : 'Next Section'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Questionnaire;