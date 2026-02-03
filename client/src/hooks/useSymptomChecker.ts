import { useState } from 'react';
import { SymptomPayload, AnalysisResult } from '../types';

export const useSymptomChecker = () => {
  const [loading, setLoading] = useState(false);
  const = useState<AnalysisResult | null>(null);

  const analyzeSymptoms = async (payload: SymptomPayload) => {
    setLoading(true);
    try {
      // Logic for API call to Node.js backend
      // const response = await fetch('/api/analyze', { method: 'POST', body: JSON.stringify(payload) });
      // const data = await response.json();
      // setResults(data);
    } catch (error) {
      console.error("Analysis failed:", error);
    } finally {
      setLoading(false);
    }
  };

  return { analyzeSymptoms, results, loading };
};