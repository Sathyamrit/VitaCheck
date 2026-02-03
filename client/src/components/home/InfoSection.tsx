import React from 'react';

const InfoSection: React.FC = () => {
  return (
    <section className="max-w-4xl mx-auto py-16 px-6">
      <div className="mb-16">
        <h2 className="text-4xl font-bold mb-6">What is VitaCheck?</h2>
        <p className="text-xl text-gray-700 leading-relaxed">
          VitaCheck operates as a Hybrid Microservice application that transforms subjective user input 
          (like feeling tired or having dry skin) into objective data. It uses machine learning to 
          "map" symptoms to specific nutrients, providing a data-backed starting point for lifestyle and dietary adjustments.
        </p>
      </div>

      <div>
        <h2 className="text-4xl font-bold mb-8">How does VitaCheck Work?</h2>
        <div className="space-y-8 text-gray-800">
          <div>
            <h3 className="text-2xl font-bold mb-2">Intelligent Input (Frontend):</h3>
            <p className="text-lg">Users interact with a React-based dashboard where they can either select specific symptoms from a list or describe their condition in plain English. This makes the tool accessible even for users who aren't sure how to categorize their health concerns.</p>
          </div>
          <div>
            <h3 className="text-2xl font-bold mb-2">Orchestration (Backend):</h3>
            <p className="text-lg">A Node.js server manages the heavy lifting of security, user accounts, and data storage. It ensures that your personal health history is saved in MongoDB so you can track your progress over time.</p>
          </div>
          <div>
            <h3 className="text-2xl font-bold mb-2">The AI Brain (Python Service):</h3>
            <p className="text-lg">This is the "computational engine."</p>
            <ul className="list-disc list-inside ml-4 mt-2 space-y-2 text-lg">
              <li><strong>NLP:</strong> It uses Natural Language Processing to understand text descriptions.</li>
              <li><strong>Vector Mapping:</strong> It uses Cosine Similarity to compare your symptoms against a database of known deficiencies.</li>
              <li><strong>Recommendation Engine:</strong> It uses content-based filtering to suggest specific recipes and meals that are mathematically optimized to fill your identified nutritional gaps.[1]</li>
            </ul>
          </div>
        </div>
      </div>
    </section>
  );
};

export default InfoSection;