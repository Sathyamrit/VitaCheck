import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const categories = [
  {
    id: 'oral',
    name: 'Oral & Dental',
    symptoms: [
      'Canker sores or mouth ulcers',
      'Swollen, red, or bleeding gums',
      'Coated tongue or "fuzzy" feeling',
      'Dry mouth (Xerostomia)',
      'Cracks at the corners of lips'
    ]
  },
  { 
    id: 'skin', 
    name: 'Dermatological', 
    symptoms: [
      'Acne or frequent breakouts',
      'Itchy skin or hives (Urticaria)',
      'Excessive sweating or night sweats',
      'Dry, flaky, or rough skin',
      'Easy bruising'
    ]
  },
  { 
    id: 'appendages', 
    name: 'Hands, Nails & Hair', 
    symptoms: [
      'Brittle, peeling, or ridged nails',
      'White spots on fingernails',
      'Thinning hair or excessive loss',
      'Dry, straw-like hair texture',
      'Cracked skin on heels or fingertips'
    ]
  },
  { 
    id: 'energy', 
    name: 'Energy & Activity', 
    symptoms: [
      'Persistent fatigue or sluggishness', 
      'Cold hands/feet or cold intolerance', 
      'Craving non-food items (ice, dirt, paper)', 
      'Morning lethargy or apathy', 
      'Hyperactivity or physical restlessness'
    ] 
  },
  { 
    id: 'neuro', 
    name: 'Neurological & Mental', 
    symptoms: [
      'Brain fog or poor concentration',
      'Irritability or quick temper',
      'Anxiety, fear, or nervousness',
      'Depression or low mood',
      'Poor memory or forgetfulness'
    ]
  },
  { 
    id: 'digestive', 
    name: 'Digestive Tract', 
    symptoms: [
      'Bloating or abdominal gas',
      'Heartburn or acid reflux',
      'Constipation or infrequent stools',
      'Diarrhea or loose stools',
      'Stomach pain or cramping'
    ]
  },
  { 
    id: 'musculoskeletal', 
    name: 'Joints & Muscles', 
    symptoms: [
      'Joint pain or stiffness',
      'Muscle aches or soreness',
      'Muscle cramps or spasms',
      'General physical weakness',
      'Feeling of "heaviness" in limbs'
    ]
  },
  { 
    id: 'sensory', 
    name: 'Head & Sensory', 
    symptoms: [
      'Frequent headaches or migraines',
      'Faintness or dizziness',
      'Dark circles under eyes',
      'Watery or itchy eyes',
      'Ringing in ears (Tinnitus)'
    ]
  }
];

const Questionnaire: React.FC = () => {
  const navigate = useNavigate();
  
  const [step, setStep] = useState(0);
  const [responses, setResponses] = useState<Record<string, number>>({});

  const handleScore = (symptom: string, score: number) => {
    setResponses(prev => ({ ...prev, [symptom]: score }));
  };

  const handleGenerateReport = async () => {
    try {
      const response = await fetch("http://localhost:8000/generate-report/user_123", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_name: "Sathya",
          age: 25,
          sex: "Male",
          symptoms: Object.keys(responses).filter(s => responses[s] > 0),
          raw_scores: responses,
          dietary_preferences: ["Vegetarian"]
        })
      });
      
      if (response.ok) {
        const data = await response.json();
        navigate(`/dashboard/${data.task_id}`);
      }
    } catch (error) {
      console.error("Failed to generate report:", error);
    }
  };

  return (
    <div className="min-h-screen bg-white py-24 px-6">
      <div className="max-w-3xl mx-auto">
        {/* Progress Indicator */}
        <div className="flex gap-2 mb-12">
          {categories.map((_, i) => (
            <div key={i} className={`h-1 flex-grow rounded-full ${i <= step ? 'bg-[#f7a221]' : 'bg-gray-100'}`} />
          ))}
        </div>

        <h1 className="text-5xl font-black tracking-tighter text-gray-900 mb-4 uppercase leading-none">
          {categories[step].name}
        </h1>
        <p className="text-gray-500 font-bold mb-10 text-sm italic underline">
          Rate symptoms for the PAST 30 DAYS (0 = Never, 4 = Frequent/Severe).
        </p>

        <div className="space-y-4 mb-12">
          {categories[step].symptoms.map((symptom) => (
            <div key={symptom} className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-6 bg-gray-50 rounded-3xl border border-gray-100 hover:bg-white hover:shadow-xl transition-all group">
              <span className="font-black text-lg tracking-tight uppercase group-hover:text-[#f7a221] transition-colors">{symptom}</span>
              <div className="flex gap-2">
                {[0, 1, 2, 3, 4].map((num) => (
                  <button
                    key={num}
                    onClick={() => handleScore(symptom, num)}
                    className={`w-10 h-10 rounded-full font-black text-xs transition-all ${
                      responses[symptom] === num ? 'bg-[#f7a221] text-white scale-110 shadow-lg' : 'bg-white text-gray-400 hover:bg-gray-100 border border-gray-100'
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
            <button onClick={() => setStep(step - 1)} className="font-black uppercase tracking-widest text-gray-400 hover:text-black">Back</button>
          )}
          <button 
            onClick={() => step < categories.length - 1 ? setStep(step + 1) : handleGenerateReport()}
            className="ml-auto bg-gray-900 text-white px-10 py-4 rounded-full font-black uppercase tracking-widest hover:bg-[#f7a221] transition-all shadow-xl"
          >
            {step === categories.length - 1 ? 'Generate Report' : 'Next Section'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Questionnaire;