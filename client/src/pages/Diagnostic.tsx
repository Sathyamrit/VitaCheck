import React, { useState } from 'react';
import { useStreamingDiagnosis, useDiagnosisDisplay } from '../hooks/useStreamingDiagnosis';

export function Diagnostic() {
  const [input, setInput] = useState('');
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

  // This hook handles splitting the <think> tags from the actual response
  const { formatted, hasThinking } = useDiagnosisDisplay(diagnosis);

  const handleSubmit = async () => {
    if (!input.trim()) return;
    await streamDiagnosis(input);
  };

  return (
    <div className="max-w-2xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Micronutrient Diagnostic</h1>

      {/* Input Section */}
      <div className="mb-4">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Describe your symptoms..."
          className="w-full h-24 p-3 border rounded-lg"
          disabled={status === 'streaming'}
        />
        <button
          onClick={handleSubmit}
          disabled={status === 'streaming' || !input.trim()}
          className="mt-2 px-4 py-2 bg-blue-600 text-white rounded-lg disabled:bg-gray-400"
        >
          {status === 'streaming' ? 'Analyzing...' : 'Get Diagnosis'}
        </button>
      </div>

      {/* Metrics */}
      {status !== 'idle' && (
        <div className="grid grid-cols-2 gap-2 mb-4 text-sm">
          <div className="p-2 bg-gray-100 rounded">
            <strong>Status:</strong> {status}
          </div>
          {ttft && (
            <div className="p-2 bg-gray-100 rounded">
              <strong>TTFT:</strong> {ttft}ms ⚡
            </div>
          )}
          {totalTime && (
            <div className="p-2 bg-gray-100 rounded">
              <strong>Total:</strong> {totalTime}ms
            </div>
          )}
        </div>
      )}

      {/* Extracted Data */}
      {extracted && (
        <div className="mb-4 p-3 bg-blue-50 rounded-lg">
          <strong className="block mb-2">Extracted Information:</strong>
          <ul className="text-sm space-y-1">
            <li>Symptoms: {extracted.symptoms.join(', ')}</li>
            <li>Age: {extracted.age}</li>
            <li>Sex: {extracted.sex}</li>
          </ul>
        </div>
      )}

      {/* Diagnosis Output */}
      {diagnosis && (
        <div className="space-y-4">
          
          {/* Thinking Section - Displayed if <think> tags are present */}
          {hasThinking && (
            <div className="p-4 bg-gray-50 border-l-4 border-gray-300 rounded-r-lg">
              <span className="text-xs font-bold uppercase tracking-widest text-gray-400 block mb-2">AI Reasoning</span>
              <div className="text-sm text-gray-500 italic whitespace-pre-wrap leading-relaxed">
                {formatted.thinking}
              </div>
            </div>
          )}

          {/* Final Response Section */}
          <div className="mb-4 p-4 bg-green-50 rounded-lg border border-green-200">
            <strong className="block mb-2">Diagnostic Analysis:</strong>
            <div className="whitespace-pre-wrap text-sm text-gray-800">
              {formatted.response || (status === 'streaming' && !formatted.response ? 'Thinking...' : '')}
            </div>
          </div>
          
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="p-3 bg-red-100 border border-red-400 rounded-lg text-red-700">
          ⚠️ {error}
        </div>
      )}

      {/* Reset Button */}
      {status === 'completed' && (
        <button
          onClick={() => {
            resetDiagnosis();
            setInput('');
          }}
          className="px-4 py-2 bg-gray-600 text-white rounded-lg"
        >
          New Analysis
        </button>
      )}
    </div>
  );
}