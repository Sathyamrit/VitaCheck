import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import { useRecipeGeneration } from '../hooks/useRecipeGeneration';
import { extractNutritionTargetsFromDiagnosis } from '../utils/diagnosisNutrition';

// 1. Interfaces for Type Safety
interface Recipe {
  name: string;
  rationale: string;
  prep_time: string;
  cooking_time?: string;
  ingredients?: string[];
  instructions?: string[];
  nutrients_provided?: string[];
  servings?: number;
}

interface DiagnosisData {
  diagnosis: string;
  nutrients?: string[];
  foodTypes?: string[];
}

const MealPlan: React.FC = () => {
  const { taskId } = useParams<{ taskId: string }>();
  const navigate = useNavigate();
  const location = useLocation();
  const { recipes, loading, error: recipeError, generateRecipes } = useRecipeGeneration();

  // 2. State Management
  const [diagnosisData, setDiagnosisData] = useState<any>(null);
  const [genTaskId, setGenTaskId] = useState<string | null>(null);
  const [recipesData, setRecipesData] = useState<Recipe[] | null>(null);
  const [loadingRecipes, setLoadingRecipes] = useState(false);
  const [recipeErrorMsg, setRecipeErrorMsg] = useState<string | null>(null);
  const [contextChecked, setContextChecked] = useState(false);

  const [preferences, setPreferences] = useState({
    dietType: 'Standard',
    allergies: '',
    cookingTime: '30 mins'
  });

  const dietStyles = ['Standard', 'Vegetarian', 'Vegan', 'Keto', 'Paleo', 'Mediterranean', 'Gluten-Free'];

  // 3. Effect: Get diagnosis from navigation state or API
  useEffect(() => {
    // First priority: Check if we came from DiagnosticDashboard with state
    if (location.state?.diagnosis) {
      setDiagnosisData({
        diagnosis: location.state.diagnosis,
        extracted: location.state.extracted,
        symptoms: location.state.symptoms,
        medications: location.state.medications,
        allergies: location.state.allergies,
        nutrients: location.state.nutrients || [],
        foodTypes: location.state.foodTypes || [],
      });
      setContextChecked(true);
      return;
    }

    // Fallback: Try to fetch from taskId if provided
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
      } finally {
        setContextChecked(true);
      }
    };

    if (taskId) {
      void fetchDiagnosis();
      return;
    }

    setContextChecked(true);
  }, [taskId, location.state]);

  // 4. Effect: Poll for Recipe Generation Status (for legacy API compatibility)
  useEffect(() => {
    if (!genTaskId) return;

    const interval = setInterval(async () => {
      try {
        const res = await fetch(`http://localhost:8000/recipe-status/${genTaskId}`);
        const result = await res.json();

        if (result.status === 'completed') {
          const parsedRecipes = typeof result.data === 'string' ? JSON.parse(result.data) : result.data;
          setRecipesData(parsedRecipes);
          setLoadingRecipes(false);
          clearInterval(interval);
        }
      } catch (error) {
        console.error("Polling error:", error);
        setLoadingRecipes(false);
        clearInterval(interval);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [genTaskId]);

  // 5. Action: Trigger Recipe Generation using Groq
  const handleStartGeneration = async () => {
    if (!diagnosisData?.diagnosis) {
      setRecipeErrorMsg('No diagnosis data available');
      return;
    }

    setLoadingRecipes(true);
    setRecipeErrorMsg(null);

    try {
      const parsedTargets = extractNutritionTargetsFromDiagnosis(diagnosisData.diagnosis);
      const nutrients = diagnosisData.nutrients?.length
        ? diagnosisData.nutrients
        : parsedTargets.nutrients;
      const foodTypes = diagnosisData.foodTypes?.length
        ? diagnosisData.foodTypes
        : parsedTargets.foodTypes;

      const generatedRecipes = await generateRecipes(
        diagnosisData.diagnosis,
        nutrients,
        foodTypes,
        preferences
      );
      setRecipesData(generatedRecipes);
    } catch (err) {
      setRecipeErrorMsg(err instanceof Error ? err.message : 'Failed to generate recipes');
    } finally {
      setLoadingRecipes(false);
    }
  };

  if (!contextChecked) {
    return <div className="p-20 text-center font-black animate-pulse text-gray-400">Loading clinical data...</div>;
  }

  if (!diagnosisData?.diagnosis) {
    return (
      <div className="max-w-xl mx-auto py-20 px-6 text-center space-y-6">
        <p className="text-gray-600 font-bold">
          No diagnosis data found. Run the AI questionnaire first, then use &quot;Generate Recipes From AI Diagnosis&quot; to open this page with nutritional targets.
        </p>
        <button
          type="button"
          onClick={() => navigate('/questionnaire')}
          className="bg-[#f7a221] text-gray-900 px-8 py-4 rounded-full font-black uppercase text-xs tracking-widest"
        >
          Go to questionnaire
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto py-16 px-6">
      <button 
        onClick={() => navigate(-1)} 
        className="mb-8 text-xs font-black uppercase tracking-widest text-gray-400 hover:text-black transition-colors"
      >
        ← Back to Dashboard
      </button>

      {!recipesData ? (
        /* UI: Preference Selection */
        <div className="bg-gray-50 rounded-[3rem] p-12 border border-gray-100 shadow-sm max-w-2xl mx-auto">
          <h1 className="text-4xl font-black uppercase tracking-tighter mb-2">Meal Plan Customizer</h1>
          <p className="text-gray-500 mb-10 text-sm font-bold uppercase tracking-widest">
            Targeting: <span className="text-black">{diagnosisData.diagnosis.substring(0, 100)}...</span>
          </p>

          <div className="mb-6 p-4 rounded-2xl border border-[#f7a221]/20 bg-[#f7a221]/5">
            <p className="text-[10px] font-black uppercase tracking-widest text-[#f7a221] mb-2">DeepSeek RAG Targets</p>
            <p className="text-xs font-bold text-gray-600">
              Nutrients: {(diagnosisData.nutrients || []).join(', ') || 'Auto-detected from diagnosis'}
            </p>
            <p className="text-xs font-bold text-gray-600 mt-1">
              Food Types: {(diagnosisData.foodTypes || []).join(', ') || 'Auto-detected from diagnosis'}
            </p>
          </div>

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

            {recipeErrorMsg && (
              <div className="p-4 bg-red-50 border-l-4 border-red-500 text-red-700 text-xs font-bold">
                ⚠️ {recipeErrorMsg}
              </div>
            )}

            <button 
              onClick={handleStartGeneration}
              disabled={loadingRecipes}
              className="w-full bg-gray-900 text-white py-5 rounded-3xl font-black uppercase text-sm tracking-widest hover:bg-[#f7a221] disabled:bg-gray-300 disabled:cursor-not-allowed transition-all"
            >
              {loadingRecipes ? "AI is creating recipes..." : "Generate Personalized Recipes"}
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
              onClick={() => setRecipesData(null)} 
              className="text-xs font-black uppercase underline decoration-2 underline-offset-4 hover:text-[#f7a221] transition-colors"
            >
              Reset Filters
            </button>
          </header>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {recipesData.map((r, i) => (
              <div key={i} className="bg-white rounded-[3.5rem] p-10 border border-gray-100 shadow-2xl hover:scale-[1.02] transition-all relative overflow-hidden group">
                <div className="absolute top-0 left-0 w-2 h-full bg-[#f7a221]" />
                <h3 className="text-3xl font-black uppercase mb-4 leading-tight">{r.name}</h3>
                <p className="text-gray-500 italic leading-relaxed mb-6">"{r.rationale}"</p>

                {r.ingredients && r.ingredients.length > 0 && (
                  <div className="mb-4">
                    <p className="text-[10px] font-black uppercase text-gray-500 mb-2">Ingredients</p>
                    <ul className="text-sm text-gray-700 list-disc list-inside space-y-1">
                      {r.ingredients.slice(0, 12).map((ing, j) => (
                        <li key={j}>{ing}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {r.instructions && r.instructions.length > 0 && (
                  <div className="mb-4">
                    <p className="text-[10px] font-black uppercase text-gray-500 mb-2">Steps</p>
                    <ol className="text-sm text-gray-700 list-decimal list-inside space-y-1">
                      {r.instructions.slice(0, 10).map((step, j) => (
                        <li key={j}>{step}</li>
                      ))}
                    </ol>
                  </div>
                )}
                
                {r.nutrients_provided && r.nutrients_provided.length > 0 && (
                  <div className="mb-6">
                    <p className="text-[10px] font-black uppercase text-gray-500 mb-2">Key Nutrients</p>
                    <div className="flex flex-wrap gap-2">
                      {r.nutrients_provided.map((nutrient, idx) => (
                        <span key={idx} className="px-2 py-1 bg-[#f7a221]/10 text-[#f7a221] rounded text-[9px] font-bold">
                          {nutrient}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
                
                <div className="flex justify-between items-center flex-wrap gap-2">
                  <span className="text-[10px] font-black uppercase bg-gray-100 px-3 py-1 rounded-full text-gray-500">
                    Prep: {r.prep_time}
                    {r.cooking_time ? ` · Cook: ${r.cooking_time}` : ''}
                    {r.servings != null ? ` · Serves ${r.servings}` : ''}
                  </span>
                  <button className="text-[#f7a221] font-black uppercase text-xs hover:underline">
                    View Details →
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