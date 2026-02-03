import React from 'react';

const SupportHero: React.FC = () => {
  return (
    <section className="bg-[#f7a221] pt-32 pb-20 px-6">
      <div className="max-w-4xl mx-auto text-center">
        <h1 className="text-6xl md:text-8xl font-black text-gray-900 tracking-tighter mb-8 leading-none">
          HOW CAN WE <br />HELP YOU?
        </h1>
        <div className="relative max-w-2xl mx-auto">
          <input 
            type="text" 
            placeholder="Search for symptoms, privacy, or AI methodology..."
            className="w-full bg-white border-none rounded-full py-5 px-8 text-lg font-bold text-gray-900 placeholder-gray-400 shadow-2xl focus:ring-4 focus:ring-blue-500/20 outline-none"
          />
          <button className="absolute right-3 top-3 bg-gray-900 text-white px-6 py-2.5 rounded-full font-black text-sm uppercase tracking-widest hover:bg-blue-600 transition-colors">
            Search
          </button>
        </div>
      </div>
    </section>
  );
};

export default SupportHero;