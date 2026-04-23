import React, { useState, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { useStreamingDiagnosis } from '../hooks/useStreamingDiagnosis';
import { extractNutritionTargetsFromDiagnosis } from '../utils/diagnosisNutrition';

const categories = [
  { id: 'oral', name: 'Oral & Dental', symptoms: ['Canker sores', 'Bleeding gums', 'Dry mouth','Angular Cheilitis (cracked corners)', 'Lip cracks'] },
  { id: 'skin', name: 'Dermatological', symptoms: ['Acne', 'Itchy skin', 'Night sweats', 'Dry skin', 'Easy bruising'] },
  { id: 'appendages', name: 'Hands, Nails & Hair', symptoms: ['Brittle nails', 'White spots on nails', 'Thinning hair', 'Dry hair'] },
  { id: 'energy', name: 'Energy & Activity', symptoms: ['Persistent fatigue', 'Cold hands/feet', 'Pica (craving ice/dirt)', 'Morning lethargy'] },
  { id: 'neuro', name: 'Neurological', symptoms: ['Brain fog', 'Irritability', 'Anxiety', 'Poor memory'] },
  { id: 'digestive', name: 'Digestive', symptoms: ['Bloating', 'Heartburn', 'Constipation', 'Diarrhea'] },
  { id: 'musculoskeletal', name: 'Joints & Muscles', symptoms: ['Joint pain', 'Muscle cramps', 'Physical weakness', 'Heavy limbs'] },
];

export function DiagnosticDashboard() {
  // --- State ---
  const navigate = useNavigate();
  const [step, setStep] = useState(0);
  const [responses, setResponses] = useState<Record<string, number>>({});
  const [userDescription, setUserDescription] = useState("");
  
  const {
    diagnosis,
    status,
    ttft,
    totalTime,
    extracted,
    error,
    streamDiagnosis,
    resetDiagnosis,
  } = useStreamingDiagnosis();

  // --- Helpers ---
  const activeSymptoms = useMemo(() => 
    Object.entries(responses).filter(([_, score]) => score > 0),
    [responses]
  );

  const handleScore = (symptom: string, score: number) => {
    setResponses(prev => ({ ...prev, [symptom]: score }));
  };

  const startAnalysis = async () => {
    // Compile everything into a rich text prompt for the AI
    const symptomSummary = activeSymptoms
      .map(([symptom, score]) => `${symptom} (Severity: ${score}/4)`)
      .join(', ');

    const fullPrompt = `
      PATIENT DATA SUMMARY:
      Symptoms Reported: ${symptomSummary || "None explicitly selected"}
      Personal Narrative: ${userDescription}
      Goal: Provide a micronutrient deficiency analysis based on these clinical markers.
    `.trim();

    await streamDiagnosis(fullPrompt);
  };

  const handleReset = () => {
    setStep(0);
    setResponses({});
    setUserDescription("");
    resetDiagnosis();
  };

  const handleGenerateRecipe = () => {
    const targets = extractNutritionTargetsFromDiagnosis(diagnosis || '');

    // Pass diagnosis data to MealPlan via navigation state
    navigate('/meal-plan', {
      state: {
        diagnosis,
        extracted,
        symptoms: extracted?.symptoms || [],
        medications: extracted?.medications || [],
        allergies: extracted?.allergies || [],
        nutrients: targets.nutrients,
        foodTypes: targets.foodTypes,
      },
    });
  };

  const handleOpenDashboard = () => {
  // Pre-calculate nutritional targets for the dashboard to use immediately
  const targets = extractNutritionTargetsFromDiagnosis(diagnosis || '');

  navigate('/dashboard', {
    state: {
      diagnosis,
      extracted,
      nutrients: targets.nutrients,
      foodTypes: targets.foodTypes,
      metrics: {
        ttft,
        totalTime,
        symptomCount: activeSymptoms.length
      },
      // Pass the original raw responses in case the dashboard needs to show the severity chart
      rawResponses: responses 
    },
  });
};

  // --- Sub-Components for UI cleanliness ---
  const ProgressHeader = () => (
    <div className="flex gap-2 mb-12">
      {[...Array(categories.length + 1)].map((_, i) => (
        <div 
          key={i} 
          className={`h-1.5 flex-grow rounded-full transition-all duration-700 ${
            i <= step ? 'bg-[#f7a221]' : 'bg-gray-100'
          }`} 
        />
      ))}
    </div>
  );

  // --- Main Render Logic ---
  return (
    <div className="min-h-screen bg-white py-12 px-6">
      <div className="max-w-3xl mx-auto">
        
        {/* Header Section */}
        <div className="mb-8">
          <h1 className="text-6xl font-black tracking-tighter text-gray-900 uppercase leading-none mb-2">
            VitaCheck<span className="text-[#f7a221]">.</span>
          </h1>
          <p className="text-gray-400 font-bold tracking-widest text-xs uppercase">
            Real-time Micronutrient Diagnostic Engine
          </p>
        </div>

        {status === 'idle' ? (
          /* PHASE 1: QUESTIONNAIRE */
          <div className="animate-in fade-in duration-500">
            <ProgressHeader />
            
            {step < categories.length ? (
              <section>
                <h2 className="text-4xl font-black tracking-tighter text-gray-900 mb-8 uppercase italic">
                  {categories[step].name}
                </h2>
                <div className="space-y-3">
                  {categories[step].symptoms.map((symptom) => (
                    <div key={symptom} className="flex flex-col md:flex-row md:items-center justify-between p-5 bg-gray-50 rounded-2xl border border-gray-100 hover:border-[#f7a221]/30 transition-all group">
                      <span className="font-bold text-gray-800 uppercase text-sm tracking-tight group-hover:text-[#f7a221] transition-colors">
                        {symptom}
                      </span>
                      <div className="flex gap-1.5 mt-3 md:mt-0">
                        {[0, 1, 2, 3, 4].map((num) => (
                          <button
                            key={num}
                            onClick={() => handleScore(symptom, num)}
                            className={`w-9 h-9 rounded-full font-black text-[10px] transition-all ${
                              responses[symptom] === num 
                                ? 'bg-[#f7a221] text-white scale-110 shadow-lg' 
                                : 'bg-white text-gray-300 border border-gray-100 hover:bg-gray-50'
                            }`}
                          >
                            {num}
                          </button>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </section>
            ) : (
              <section className="space-y-6">
                <h2 className="text-4xl font-black tracking-tighter text-gray-900 uppercase italic">
                  Contextual Analysis
                </h2>
                <p className="text-gray-500 font-medium text-sm">
                  Describe any patterns (e.g., "energy crashes at 3 PM") or dietary habits.
                </p>
                <textarea
                  className="w-full h-48 p-6 bg-gray-50 rounded-[2rem] border-2 border-transparent focus:border-[#f7a221] focus:bg-white text-gray-800 font-medium transition-all outline-none"
                  placeholder="Tell us more about how you feel..."
                  value={userDescription}
                  onChange={(e) => setUserDescription(e.target.value)}
                />
              </section>
            )}

            <div className="flex justify-between mt-12 pt-6 border-t border-gray-50">
              <button 
                onClick={() => setStep(Math.max(0, step - 1))}
                className={`font-black uppercase tracking-widest text-xs ${step === 0 ? 'opacity-0' : 'text-gray-400 hover:text-black'}`}
              >
                Back
              </button>
              <button 
                onClick={() => step < categories.length ? setStep(step + 1) : startAnalysis()}
                className="bg-gray-900 text-white px-12 py-4 rounded-full font-black uppercase tracking-widest text-xs hover:bg-[#f7a221] transition-all shadow-xl active:scale-95"
              >
                {step === categories.length ? 'Start AI Analysis' : 'Next Category'}
              </button>
            </div>
          </div>
        ) : (
          /* PHASE 2: STREAMING RESULTS */
          <div className="space-y-6 animate-in slide-in-from-bottom-8 duration-700">
            
            {/* Status & Performance Metrics */}
            <div className="flex flex-wrap gap-3">
              <div className="px-4 py-2 bg-black text-white rounded-full text-[10px] font-black uppercase tracking-widest flex items-center gap-2">
                <span className={`w-2 h-2 rounded-full ${status === 'streaming' ? 'bg-green-400 animate-pulse' : 'bg-blue-400'}`} />
                {status}
              </div>
              {ttft && <div className="px-4 py-2 bg-gray-100 rounded-full text-[10px] font-black uppercase tracking-widest">TTFT: {ttft}ms ⚡</div>}
              {totalTime && <div className="px-4 py-2 bg-gray-100 rounded-full text-[10px] font-black uppercase tracking-widest">Total: {totalTime}ms</div>}
            </div>

            {/* AI Extracted Entity View */}
            {extracted && (
              <div className="p-6 bg-[#f7a221]/5 rounded-3xl border border-[#f7a221]/20">
                <h3 className="text-xs font-black uppercase tracking-[0.2em] text-[#f7a221] mb-4">Extracted Patient Data</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                  {/* Symptoms */}
                  <div className="col-span-2">
                    <p className="text-[8px] font-bold text-gray-500 uppercase mb-2">Symptoms</p>
                    <div className="flex flex-wrap gap-1">
                      {(extracted.symptoms || []).map((s: string) => (
                        <span key={s} className="px-2 py-1 bg-white border border-[#f7a221]/30 rounded text-[9px] font-bold">{s}</span>
                      ))}
                    </div>
                  </div>
                  
                  {/* Age */}
                  <div>
                    <p className="text-[8px] font-bold text-gray-500 uppercase mb-2">Age</p>
                    <p className="px-2 py-1 bg-white border border-[#f7a221]/30 rounded text-[9px] font-bold">{extracted.age || 'Unknown'}</p>
                  </div>
                  
                  {/* Sex */}
                  <div>
                    <p className="text-[8px] font-bold text-gray-500 uppercase mb-2">Sex</p>
                    <p className="px-2 py-1 bg-white border border-[#f7a221]/30 rounded text-[9px] font-bold capitalize">{extracted.sex || 'Unknown'}</p>
                  </div>
                  
                  {/* Medications */}
                  {extracted.medications && extracted.medications.length > 0 && (
                    <div className="col-span-2">
                      <p className="text-[8px] font-bold text-gray-500 uppercase mb-2">Medications</p>
                      <div className="flex flex-wrap gap-1">
                        {(extracted.medications || []).map((m: string) => (
                          <span key={m} className="px-2 py-1 bg-orange-50 border border-orange-200 rounded text-[8px] font-bold">{m}</span>
                        ))}
                      </div>
                    </div>
                  )}
                  
                  {/* Allergies */}
                  {extracted.allergies && extracted.allergies.length > 0 && (
                    <div className="col-span-2">
                      <p className="text-[8px] font-bold text-gray-500 uppercase mb-2">Allergies</p>
                      <div className="flex flex-wrap gap-1">
                        {(extracted.allergies || []).map((a: string) => (
                          <span key={a} className="px-2 py-1 bg-red-50 border border-red-200 rounded text-[8px] font-bold">{a}</span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* The Live Stream Output */}
            <div className="relative group">
               <div className="absolute -inset-1 bg-gradient-to-r from-[#f7a221] to-orange-600 rounded-[2rem] blur opacity-10 group-hover:opacity-20 transition duration-1000"></div>
               <div className="relative p-8 bg-white border border-gray-100 rounded-[2rem] min-h-[300px] shadow-2xl">
                <h3 className="text-xs font-black uppercase tracking-[0.2em] text-gray-400 mb-6 italic">Clinical Diagnosis Stream</h3>
                {diagnosis ? (
                  <div className="whitespace-pre-wrap text-gray-800 leading-relaxed font-medium">
                    {diagnosis}
                  </div>
                ) : (
                  <div className="flex flex-col items-center justify-center py-12 text-gray-300 space-y-6">
                    <div className="relative w-12 h-12">
                      <div className="absolute inset-0 bg-gradient-to-r from-[#f7a221] to-orange-600 rounded-full animate-spin" style={{
                        mask: 'conic-gradient(from 0deg, transparent 75%, black 100%)',
                        WebkitMask: 'conic-gradient(from 0deg, transparent 75%, black 100%)',
                      }} />
                    </div>
                    <div className="text-center space-y-2">
                      <p className="font-black uppercase tracking-widest text-[10px]">
                        {ttft && ttft < 30000 ? 'Analyzing Symptoms' : ttft ? 'Generating Diagnosis' : 'Starting Analysis'}
                      </p>
                      <p className="text-[9px] text-gray-400 font-medium">
                        {ttft 
                          ? `TTFT: ${(ttft / 1000).toFixed(1)}s ⚡ • Streaming response...`
                          : 'Extracting symptoms and retrieving medical context...'}
                      </p>
                      {!ttft && (
                        <p className="text-[8px] text-gray-500 mt-3">
                          AI is analyzing your symptoms and thinking phase
                        </p>
                      )}
                      {ttft && ttft < 30000 && (
                        <p className="text-[8px] text-gray-500 mt-3">
                          Still thinking... answers coming soon
                        </p>
                      )}
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Error Message */}
            {error && (
              <div className="p-4 bg-red-50 border-l-4 border-red-500 text-red-700 text-xs font-bold uppercase tracking-widest">
                ⚠️ Error: {error}
              </div>
            )}

            {/* Final Actions */}
            {status === 'completed' && (
              <div className="space-y-3">
                <button 
                  onClick={handleOpenDashboard}
                  className="w-full bg-[#f7a221] text-gray-900 py-5 rounded-[1.5rem] font-black uppercase tracking-[0.3em] hover:bg-orange-500 transition-all shadow-xl shadow-orange-200"
                >
                  Open Dashboard
                </button>
              <div className="space-y-3">
                <button 
                  onClick={handleGenerateRecipe}
                  className="w-full bg-[#f7a221] text-gray-900 py-5 rounded-[1.5rem] font-black uppercase tracking-[0.3em] hover:bg-orange-500 transition-all shadow-xl shadow-orange-200"
                >
                  Generate Recipes From AI Diagnosis
                </button>
                  <button 
                    onClick={handleReset}
                    className="w-full bg-gray-900 text-white py-5 rounded-[1.5rem] font-black uppercase tracking-[0.3em] hover:bg-gray-700 transition-all shadow-xl shadow-orange-200"
                  >
                    Start New Session
                  </button>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}