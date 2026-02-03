import React from 'react';

const PrivacyHero: React.FC = () => {
  return (
    <section className="bg-[#f7a221] pt-32 pb-20 px-6 text-center">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-6xl md:text-8xl font-black text-gray-900 tracking-tighter mb-6 leading-none uppercase">
          Your Data. <br />Your Health.
        </h1>
        <p className="text-xl md:text-2xl text-gray-900 font-bold max-w-2xl mx-auto leading-tight italic">
          Transparency is the foundation of our AI-driven diagnostics.
        </p>
      </div>
    </section>
  );
};

export default PrivacyHero;