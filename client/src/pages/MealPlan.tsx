import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

const MealPlan: React.FC = () => {
  const { taskId } = useParams<{ taskId: string }>();
  const navigate = useNavigate();
  const [report, setReport] = useState<any>(null);
  const [recipes, setRecipes] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      try {
        const response = await fetch(`http://localhost:8000/report-status/${taskId}`);
        const result = await response.json();
        
        if (result.status === 'completed' && result.data) {
          const data = JSON.parse(result.data);
          setReport(data);

// Robust check: Ensure diagnosis is treated as a string
const diagStr = String(data.diagnosis || "");

// Pattern: Diagnosis-to-Recipe Mapping (Simulation of RAG) [2, 3]
let targetedRecipes = [];
if (diagStr.toLowerCase().includes("iron") || diagStr.toLowerCase().includes("anemia")) {
  targetedRecipes = [
    { name: "Spinach & Lentil Curry", reason: "Rich in iron and vitamin C for anemia support." },
    { name: "Beetroot Salad", reason: "Beetroot helps improve hemoglobin levels." }
  ];
} else if (diagStr.toLowerCase().includes("vitamin d") || diagStr.toLowerCase().includes("calcium")) {
  targetedRecipes = [
    { name: "Grilled Salmon Bowl", reason: "Salmon is a great source of vitamin D." },
    { name: "Tofu & Broccoli Stir Fry", reason: "Tofu and broccoli are rich in calcium." }
  ];
} else {
  targetedRecipes = [
    { name: "Balanced Quinoa Salad", reason: "Provides a variety of nutrients for general wellness." }
  ];
}

setRecipes(targetedRecipes);
setLoading(false);
        }
      } catch (err) {
        console.error("Polling error:", err);
      }
    };
    loadData();
  }, [taskId]);

  if (loading) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-white">
        <div className="w-16 h-16 border-4 border-[#f7a221] border-t-transparent rounded-full animate-spin mb-4" />
        <h2 className="text-2xl font-black uppercase tracking-tighter text-gray-400">Synthesizing Meal Plan...</h2>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto py-16 px-6">
      {/* Header with Navigation [4] */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-end mb-12 gap-6">
        <div>
          <button 
            onClick={() => navigate(-1)} 
            className="mb-6 text-[10px] font-black uppercase tracking-widest text-gray-400 hover:text-[#f7a221] transition-colors"
          >
            ← Return to Dashboard
          </button>
          <h1 className="text-7xl font-black tracking-tighter uppercase leading-none">Dietary Therapy</h1>
          <p className="text-gray-400 font-bold uppercase text-xs mt-4 tracking-widest">
            Targeting: <span className="text-[#f7a221]">{report?.diagnosis}</span>
          </p>
        </div>
        <div className="bg-gray-900 text-white px-8 py-4 rounded-3xl text-xs font-black uppercase tracking-widest shadow-xl">
          Verified Analysis
        </div>
      </div>

      {/* Recipe Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
        {recipes.map((r, i) => (
          <div key={i} className="bg-gray-50 rounded-[3.5rem] p-12 border border-gray-100 hover:bg-white hover:shadow-2xl transition-all group relative overflow-hidden">
            <div className="absolute top-0 right-0 p-8 text-[80px] font-black text-gray-100 group-hover:text-[#f7a221]/10 leading-none pointer-events-none">
              0{i + 1}
            </div>
            <h3 className="text-4xl font-black uppercase mb-6 group-hover:text-[#f7a221] transition-colors leading-tight pr-12">
              {r.name}
            </h3>
            <div className="space-y-4">
              {/* <span className="text-[10px] font-black uppercase text-blue-600 underline tracking-widest block">
                Clinical Rationale
              </span> */}
              <p className="text-gray-500 font-medium italic leading-relaxed text-lg">
                "{r.reason}"
              </p>
            </div>
          </div>
        ))}
      </div>

      {/* Compliance Footer [5] */}
      <div className="mt-20 pt-10 border-t border-gray-100 flex flex-col md:flex-row justify-between items-center gap-6">
        <p className="text-[10px] text-gray-400 font-bold uppercase tracking-tighter text-center md:text-left">
          Clinical data processed in accordance with DPDP Act 2023 [5]
        </p>
        <button className="bg-[#f7a221] text-white px-10 py-4 rounded-full font-black uppercase tracking-widest text-xs hover:scale-105 transition-all shadow-lg">
          Download PDF Guide
        </button>
      </div>
    </div>
  );
};

export default MealPlan;