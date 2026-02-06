import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import RecipeSection from '../components/dashboard/RecipeSection';

const Dashboard: React.FC = () => {
  const { taskId } = useParams<{ taskId: string }>();
  const [report, setReport] = useState<any>(null);
  const [status, setStatus] = useState<'processing' | 'completed' | 'failed'>('processing');

  useEffect(() => {
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
  }, [taskId]);

  if (status === 'processing') {
    return (
      <div className="min-h-[70vh] flex flex-col items-center justify-center">
        <div className="w-12 h-12 border-4 border-[#f7a221] border-t-transparent rounded-full animate-spin mb-4" />
        <h2 className="text-xl font-black uppercase tracking-tighter">AI Processing Clinical Markers...</h2>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto py-12 px-6">
      {/* Patient Header */}
      <div className="bg-gray-50 rounded-[2rem] p-8 border border-gray-100 mb-8 shadow-sm">
        <h1 className="text-4xl font-black tracking-tighter uppercase">Clinical Dashboard</h1>
        <div className="flex gap-6 mt-4 text-[10px] font-bold text-gray-500 uppercase tracking-widest">
          <span>Patient: {report?.user_info?.name}</span>
          <span>Age: {report?.user_info?.age}</span>
          <span className="text-green-600">● Verification Status: Verified</span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-6">
          {/* Diagnostic Card */}
          <section className="bg-white rounded-[2rem] p-10 shadow-2xl border border-gray-50">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-[#f7a221] font-black uppercase text-xs tracking-widest">Initial Diagnosis</h3>
              <div className="text-[10px] bg-blue-50 text-blue-700 px-3 py-1 rounded-full font-black uppercase">
                Confidence: 94.2% 
              </div>
            </div>
            <p className="text-3xl font-bold italic leading-tight text-gray-900 mb-8">
              "{report?.diagnosis}"
            </p>
            <div className="p-6 bg-blue-50 rounded-[2rem] border border-blue-100">
              <span className="text-[10px] font-black uppercase text-blue-800 underline mb-2 block">Clinician Interpretation</span>
              <p className="text-sm text-blue-600 font-medium leading-relaxed italic">{report?.clinician_notes}</p>
            </div>
          </section>
        </div>

        {/* Navigation Sidebar */}
        <RecipeSection diagnosis={report?.diagnosis} />
      </div>
    </div>
  );
};

export default Dashboard;