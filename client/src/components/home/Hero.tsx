import React from 'react';
import { useNavigate } from 'react-router-dom';

const Hero: React.FC = () => {
  const navigate = useNavigate();
  // const handleStartAssessment = () => {
  //     const isAuthenticated = !!localStorage.getItem('token'); 
  //     if (isAuthenticated) {
  //       navigate('/questionnaire');
  //     } else {
  //       navigate('/auth', { state: { from: '/questionnaire' } });
  //     }
  //   };
  const handleStartAssessment = () => {
    navigate('/questionnaire');
  };
  return (
    <section className="relative bg-[#f7a221] overflow-hidden py-24 px-6 flex items-center justify-center min-h-[500px]">

      <div className="relative z-10 max-w-4xl text-center flex flex-col items-center">

        <h1 className="text-5xl md:text-7xl font-black tracking-tighter text-gray-900 mb-6 uppercase leading-none">
          Unlock Your <br />
          Health Potential
        </h1>

        <p className="text-gray-900 font-bold mb-10 text-lg md:text-xl max-w-xl">
          Powered by Functional Medicine and AI-Driven Insights to map your symptoms to real solutions.
        </p>

        <button 
          onClick={handleStartAssessment}
          className="bg-gray-900 text-white px-12 py-5 rounded-full font-black uppercase tracking-widest hover:bg-white hover:text-black transition-all shadow-2xl scale-100 hover:scale-105 active:scale-95"
        >
          Start Your Free Assessment
        </button>

        <button 
          onClick={() => navigate('/about-vitacheck')}
          className="mt-6 text-sm font-black uppercase tracking-widest text-gray-900 underline decoration-2 underline-offset-4 hover:text-white transition-colors"
        >
          How it works
        </button>
      </div>
    </section>
  );
};

export default Hero;