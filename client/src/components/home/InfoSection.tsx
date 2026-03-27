import React from 'react';

const InfoSection: React.FC = () => {
  return (
    <section className="max-w-4xl mx-auto py-16 px-6">
      <div className="mb-16">
        <h2 className="text-4xl font-bold mb-6">What is VitaCheck?</h2>
        <p className="text-xl text-gray-700 leading-relaxed">
          VitaCheck is an AI-powered micronutrient diagnostic platform that uses advanced reasoning (DeepSeek R1 8B) 
          combined with medical knowledge retrieval (RAG) to transform subjective symptoms into precise micronutrient insights. 
          It checks 33 micronutrients, screens for drug-nutrient interactions, and provides personalized recommendations grounded in clinical evidence.
        </p>
      </div>

      <div>
        <h2 className="text-4xl font-bold mb-8">How does VitaCheck Work?</h2>
        <div className="space-y-8 text-gray-800">
          <div>
            <h3 className="text-2xl font-bold mb-2">Intelligent Input (Frontend):</h3>
            <p className="text-lg">Users describe their symptoms, medications, and health context through an intuitive React dashboard. Your input is streamed directly to our API with real-time processing feedback via Server-Sent Events.</p>
          </div>
          <div>
            <h3 className="text-2xl font-bold mb-2">Multi-Stage Analysis (Python FastAPI):</h3>
            <p className="text-lg">Your input flows through our advanced pipeline:</p>
            <ul className="list-disc list-inside ml-4 mt-2 space-y-2 text-lg">
              <li><strong>Extraction:</strong> Groq API rapidly parses your symptoms, medications, and demographics from natural language.</li>
              <li><strong>Knowledge Retrieval:</strong> RAG retrieves relevant medical context by searching our knowledge base across micronutrients stored in ChromaDB.</li>
              <li><strong>Advanced Reasoning:</strong> DeepSeek R1 8B analyzes your complete profile, considering symptom clusters, drug interactions, and biochemistry to identify likely deficiencies with confidence scores.</li>
            </ul>
          </div>
          <div>
            <h3 className="text-2xl font-bold mb-2">Safety & Personalization:</h3>
            <p className="text-lg">Before recommendations are shown, our system checks for medication interactions, screens for toxic doses, and personalizes suggestions based on your history. Your profile is saved securely so you can track progress over time.</p>
          </div>
        </div>
      </div>
    </section>
  );
};

export default InfoSection;