import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

// 1. Interfaces for Type Safety
interface Recipe {
  name: string;
  rationale: string; // Unified from "reason" and "rationale"
  prep_time: string; // Unified from "time" and "prep_time"
}

interface DiagnosisData {
  diagnosis: string;
}

const MealPlan: React.FC = () => {
  const { taskId } = useParams<{ taskId: string }>();
  const navigate = useNavigate();

  // 2. State Management
  const [diagnosisData, setDiagnosisData] = useState<DiagnosisData | null>(null);
  const [genTaskId, setGenTaskId] = useState<string | null>(null);
  const [recipes, setRecipes] = useState<Recipe[] | null>(null);
  const [loading, setLoading] = useState(false);

  const [preferences, setPreferences] = useState({
    dietType: 'Standard',
    allergies: '',
    cookingTime: '30 mins'
  });

  const dietStyles = ['Standard', 'Vegetarian', 'Vegan', 'Keto', 'Paleo', 'Mediterranean', 'Gluten-Free'];

  // 3. Effect: Fetch Initial Diagnosis
  useEffect(() => {
    const fetchDiagnosis = async () => {
      try {
        const res = await fetch(`http://localhost:8000/report-status/${taskId}`);
        const result = await res.json();
        if (result.status === 'completed') {
          const parsedData = typeof result.data === 'string' ? JSON.parse(result.data) : result.data;
          setDiagnosisData(parsedData);
        }
      } catch (error) {
        console.error("Failed to fetch diagnosis:", error);
      }
    };
    if (taskId) fetchDiagnosis();
  }, [taskId]);

  // 4. Effect: Poll for Recipe Generation Status
  useEffect(() => {
    if (!genTaskId) return;

    const interval = setInterval(async () => {
      try {
        const res = await fetch(`http://localhost:8000/recipe-status/${genTaskId}`);
        const result = await res.json();

        if (result.status === 'completed') {
          const parsedRecipes = typeof result.data === 'string' ? JSON.parse(result.data) : result.data;
          setRecipes(parsedRecipes);
          setLoading(false);
          clearInterval(interval);
        }
      } catch (error) {
        console.error("Polling error:", error);
        setLoading(false);
        clearInterval(interval);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [genTaskId]);

  // 5. Action: Trigger AI Generation
  const handleStartGeneration = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/generate-meal-plan", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          diagnosis: diagnosisData?.diagnosis, 
          preferences: preferences 
        })
      });
      const data = await res.json();
      setGenTaskId(data.recipe_task_id);
    } catch (error) {
      console.error("Failed to start generation:", error);
      setLoading(false);
    }
  };

  // 6. Early Return for Loading State
  if (!diagnosisData) {
    return <div className="p-20 text-center font-black animate-pulse text-gray-400">Loading Clinical Data...</div>;
  }

  return (
    <div className="max-w-6xl mx-auto py-16 px-6">
      <button 
        onClick={() => navigate(-1)} 
        className="mb-8 text-xs font-black uppercase tracking-widest text-gray-400 hover:text-black transition-colors"
      >
        ← Back to Dashboard
      </button>

      {!recipes ? (
        /* UI: Preference Selection */
        <div className="bg-gray-50 rounded-[3rem] p-12 border border-gray-100 shadow-sm max-w-2xl mx-auto">
          <h1 className="text-4xl font-black uppercase tracking-tighter mb-2">Meal Plan Customizer</h1>
          <p className="text-gray-500 mb-10 text-sm font-bold uppercase tracking-widest">
            Targeting: <span className="text-black">{diagnosisData.diagnosis}</span>
          </p>

          <div className="space-y-8">
            <section>
              <label className="block text-xs font-black uppercase mb-4 text-[#f7a221]">Dietary Style</label>
              <div className="flex flex-wrap gap-3">
                {dietStyles.map(type => (
                  <button 
                    key={type}
                    type="button"
                    onClick={() => setPreferences({ ...preferences, dietType: type })}
                    className={`px-6 py-3 rounded-full text-xs font-black uppercase transition-all ${
                      preferences.dietType === type 
                        ? 'bg-[#f7a221] text-white shadow-lg' 
                        : 'bg-white border border-gray-200 text-gray-400 hover:border-[#f7a221]'
                    }`}
                  >
                    {type}
                  </button>
                ))}
              </div>
            </section>

            <section>
              <label className="block text-xs font-black uppercase mb-2">Known Allergies / Exclusions</label>
              <input 
                type="text" 
                placeholder="e.g. Peanuts, Shellfish..."
                className="w-full p-4 rounded-2xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-[#f7a221] transition-all"
                value={preferences.allergies}
                onChange={(e) => setPreferences({ ...preferences, allergies: e.target.value })}
              />
            </section>

            <button 
              onClick={handleStartGeneration}
              disabled={loading}
              className="w-full bg-gray-900 text-white py-5 rounded-3xl font-black uppercase text-sm tracking-widest hover:bg-[#f7a221] disabled:bg-gray-300 disabled:cursor-not-allowed transition-all"
            >
              {loading ? "AI is calculating macros..." : "Generate Personalized Plan"}
            </button>
          </div>
        </div>
      ) : (
        /* UI: Recipe Display */
        <div className="space-y-12">
          <header className="flex justify-between items-end">
            <div>
              <h1 className="text-7xl font-black tracking-tighter uppercase leading-none">Suggested Meals</h1>
              <p className="text-gray-400 font-bold uppercase text-xs mt-4 tracking-widest">
                Optimized for {preferences.dietType} preferences
              </p>
            </div>
            <button 
              onClick={() => setRecipes(null)} 
              className="text-xs font-black uppercase underline decoration-2 underline-offset-4 hover:text-[#f7a221] transition-colors"
            >
              Reset Filters
            </button>
          </header>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {recipes.map((r, i) => (
              <div key={i} className="bg-white rounded-[3.5rem] p-10 border border-gray-100 shadow-2xl hover:scale-[1.02] transition-all relative overflow-hidden group">
                <div className="absolute top-0 left-0 w-2 h-full bg-[#f7a221]" />
                <h3 className="text-3xl font-black uppercase mb-4 leading-tight">{r.name}</h3>
                <p className="text-gray-500 italic leading-relaxed mb-6">"{r.rationale}"</p>
                <div className="flex justify-between items-center">
                  <span className="text-[10px] font-black uppercase bg-gray-100 px-3 py-1 rounded-full text-gray-500">
                    Prep Time: {r.prep_time}
                  </span>
                  <button className="text-[#f7a221] font-black uppercase text-xs hover:underline">
                    View Recipe Details →
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default MealPlan;