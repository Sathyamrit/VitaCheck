import React from 'react';
import MissionHero from '../components/about-us/MissionHero';
import ProblemScope from '../components/about-us/ProblemScope';
import TechStack from '../components/about-us/TechStack';
import CoreValues from '../components/about-us/CoreValues';

const About: React.FC = () => {
  return (
    <div className="min-h-screen bg-white animate-in fade-in duration-700">
      <MissionHero />
      <ProblemScope />
      <TechStack />
      <CoreValues />
      
      {/* Final Call to Action Section */}
      <section className="py-20 px-6 bg-gray-900 text-white text-center">
        <h2 className="text-4xl font-black tracking-tighter mb-8 uppercase">Start Your Health Journey</h2>
        <p className="text-gray-400 max-w-xl mx-auto mb-10 font-medium">
          Access our evidence-based symptom assessment and get your personalized nutritional roadmap today.
        </p>
        <button className="bg-[#f7a221] text-gray-900 px-12 py-5 rounded-full font-black hover:scale-105 transition-transform shadow-xl">
          TAKE THE ASSESSMENT
        </button>
      </section>
    </div>
  );
};

export default About;