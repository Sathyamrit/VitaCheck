import React, { useState, useEffect } from 'react';
import { useParams, useLocation } from 'react-router-dom'; // Add useLocation
import RecipeSection from '../components/dashboard/RecipeSection';

const Dashboard: React.FC = () => {
  const { taskId } = useParams<{ taskId: string }>();
  const location = useLocation(); // Access the state passed from navigate
  
  const [report, setReport] = useState<any>(null);
  const [status, setStatus] = useState<'processing' | 'completed' | 'failed'>('processing');

  useEffect(() => {
    // 1. Priority: Check if data was passed via state (Instant)
    if (location.state?.diagnosis) {
      setReport({
        diagnosis: location.state.diagnosis,
        user_info: {
          name: location.state.extracted?.name || "Guest",
          age: location.state.extracted?.age || "N/A"
        },
        clinician_notes: "AI-generated analysis based on real-time symptoms.",
        nutrients: location.state.nutrients,
        foodTypes: location.state.foodTypes
      });
      setStatus('completed');
      return; // Exit effect, no need to poll
    }

    // 2. Fallback: Check if we have a taskId to poll the backend
    if (!taskId) {
       // If no state and no taskId, it's a failed entry
       setStatus('failed');
       return;
    }

    const pollStatus = setInterval(async () => {
      try {
        const response = await fetch(`http://localhost:8000/report-status/${taskId}`);
        const result = await response.json();
        
        if (result.status === 'completed' && result.data) {
          setReport(JSON.parse(result.data));
          setStatus('completed');
          clearInterval(pollStatus);
        }
      } catch (err) {
        console.error("Polling error:", err);
      }
    }, 2000);

    return () => clearInterval(pollStatus);
  }, [taskId, location.state]);

  if (status === 'processing') {
    return (
      <div className="min-h-[70vh] flex flex-col items-center justify-center">
        <div className="w-12 h-12 border-4 border-[#f7a221] border-t-transparent rounded-full animate-spin mb-4" />
        <h2 className="text-xl font-black uppercase tracking-tighter">AI Processing Clinical Markers...</h2>
      </div>
    );
  }

  if (status === 'failed' && !report) {
    return <div className="p-20 text-center font-bold">No diagnosis data found. Please complete the questionnaire.</div>;
  }

  return (
    <div className="max-w-6xl mx-auto py-12 px-6 animate-in fade-in duration-700">
      {/* Patient Header */}
      <div className="bg-gray-50 rounded-[2rem] p-8 border border-gray-100 mb-8 shadow-sm flex justify-between items-center">
        <div>
            <h1 className="text-4xl font-black tracking-tighter uppercase">Clinical Dashboard</h1>
            <div className="flex gap-6 mt-4 text-[10px] font-bold text-gray-500 uppercase tracking-widest">
              <span>Patient: {report?.user_info?.name || 'Guest User'}</span>
              <span>Age: {report?.user_info?.age || 'N/A'}</span>
              <span className="text-green-600">● Verification Status: AI-Verified</span>
            </div>
        </div>
        {/* Performance Badge from State */}
        {location.state?.metrics && (
            <div className="text-right">
                <p className="text-[8px] font-black text-gray-400 uppercase">Analysis Speed</p>
                <p className="text-xs font-black text-[#f7a221]">{location.state.metrics.ttft}ms</p>
            </div>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-6">
          <section className="bg-white rounded-[2rem] p-10 shadow-2xl border border-gray-50">
            <h3 className="text-[#f7a221] font-black uppercase text-xs tracking-widest mb-6">Initial Diagnosis</h3>
            <p className="text-2xl font-bold leading-tight text-gray-900 mb-8">
              {report?.diagnosis}
            </p>
            
            {/* Visual breakdown of identified nutrients */}
            {report?.nutrients && (
                <div className="flex flex-wrap gap-2 mb-8">
                    {report.nutrients.map((n: string) => (
                        <span key={n} className="px-3 py-1 bg-gray-900 text-white text-[9px] font-black uppercase rounded-full">
                            Target: {n}
                        </span>
                    ))}
                </div>
            )}

            <div className="p-6 bg-blue-50 rounded-[2rem] border border-blue-100">
              <span className="text-[10px] font-black uppercase text-blue-800 underline mb-2 block">Clinician Interpretation</span>
              <p className="text-sm text-blue-600 font-medium leading-relaxed italic">
                {report?.clinician_notes || "Micronutrient levels prioritized based on reported symptoms."}
              </p>
            </div>
          </section>
        </div>

        <aside className="space-y-6">
             <RecipeSection diagnosis={report?.diagnosis} />
             
             {/* Optional: Add a small card for "Next Steps" */}
             <div className="bg-black text-white p-8 rounded-[2rem]">
                <h4 className="text-xs font-black uppercase tracking-widest mb-4">Recommendation</h4>
                <p className="text-xs text-gray-400 leading-relaxed">
                    Based on your <b>{location.state?.metrics?.symptomCount || 0}</b> reported symptoms, we suggest generating a 7-day meal plan.
                </p>
             </div>
        </aside>
      </div>
    </div>
  );
};

export default Dashboard;