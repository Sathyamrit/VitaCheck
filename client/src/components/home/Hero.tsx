import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Hero: React.FC = () => {
  const [input, setInput] = useState('');
  const navigate = useNavigate();

  return (
    <section className="bg-[#f7a221] py-16 px-4 flex flex-col items-center justify-center min-h-[400px]">
      <div className="w-full max-w-2xl bg-gray-400/80 rounded-full p-1 flex items-center shadow-lg mb-6">
        <input 
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Tell us how you feel (Age, Gender, Symptoms, etc.)"
          className="w-full bg-transparent px-6 py-4 text-white placeholder-gray-200 focus:outline-none"
        />
        <div className="bg-blue-100 rounded-full p-4 mr-1">
          {/* Search Icon */}
          <div className="w-4 h-4 rounded-full border-2 border-blue-400" />
        </div>
      </div>
      
      <button 
      className="bg-gray-200 text-gray-800 px-8 py-3 rounded-full font-semibold shadow-md hover:bg-white transition-all"
        onClick={() => navigate('/questionnaire')}
      >
        Try out our Questionnaire
      </button>
    </section>
  );
};

export default Hero;