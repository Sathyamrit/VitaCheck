import React from 'react';

const ContactHero: React.FC = () => {
  return (
    <section className="bg-[#f7a221] pt-32 pb-20 px-6">
      <div className="max-w-5xl mx-auto">
        <h1 className="text-6xl md:text-8xl font-black text-gray-900 tracking-tighter mb-6 leading-[0.85] uppercase">
          Let's talk <br />Health.
        </h1>
        <p className="text-xl md:text-2xl text-gray-900 font-bold max-w-xl leading-tight">
          Whether you have questions about our AI brain, data privacy, or 
          technical support, our team is here to help.
        </p>
      </div>
    </section>
  );
};

export default ContactHero;