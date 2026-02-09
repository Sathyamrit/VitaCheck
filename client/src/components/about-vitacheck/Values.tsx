import React from 'react';

const Values: React.FC = () => {
  return (
    <section className="py-12 border-t border-gray-100">
      <h2 className="text-3xl font-bold tracking-tight mb-12 text-center text-gray-900">Our Core Principles</h2>
      <div className="grid sm:grid-cols-3 gap-12">
        <div className="text-center">
          <div className="w-16 h-16 bg-blue-100 text-blue-600 rounded-2xl flex items-center justify-center mx-auto mb-6 text-2xl">🛡️</div>
          <h3 className="font-bold text-xl mb-3">Privacy First</h3>
          {/* <p className="text-gray-500 text-sm">We use HIPAA-compliant infrastructure and encryption to ensure your health data remains yours alone.</p> */}
        </div>
        <div className="text-center">
          <div className="w-16 h-16 bg-green-100 text-green-600 rounded-2xl flex items-center justify-center mx-auto mb-6 text-2xl">🔬</div>
          <h3 className="font-bold text-xl mb-3">Evidence-Based</h3>
          {/* <p className="text-gray-500 text-sm">Our AI models are trained on clinical datasets like NHANES to ensure accuracy in symptom mapping.</p> */}
        </div>
        <div className="text-center">
          <div className="w-16 h-16 bg-purple-100 text-purple-600 rounded-2xl flex items-center justify-center mx-auto mb-6 text-2xl">🥗</div>
          <h3 className="font-bold text-xl mb-3">Holistic Closure</h3>
          <p className="text-gray-500 text-sm">We don't just identify gaps; we provide customized recipes optimized for bioavailability.</p>
        </div>
      </div>
    </section>
  );
};

export default Values;