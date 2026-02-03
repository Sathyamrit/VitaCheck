import React from 'react';

const FAQSection: React.FC = () => {
  const faqs = [
    {
      q: "Can I trust the yellow teeth assessment?",
      a: "The AI distinguishes between extrinsic stains (coffee/tobacco) and intrinsic yellowing caused by Vitamin D and Calcium deficiencies that affect enamel development ."
    },
    {
      q: "Is my health data secure?",
      a: "Yes. We adhere to 'Privacy by Design' principles. All data is encrypted using AES-256 and processed in HIPAA-compliant environments.[10, 2]"
    }
  ];

  return (
    <section>
      <h2 className="text-4xl font-black tracking-tighter text-gray-900 mb-12 uppercase">Frequently Asked Questions</h2>
      <div className="space-y-6">
        {faqs.map((faq, i) => (
          <div key={i} className="group p-8 bg-gray-50 rounded-[2rem] hover:bg-white hover:shadow-xl transition-all duration-300 border border-gray-100">
            <h3 className="text-xl font-black tracking-tighter text-gray-900 mb-3 group-hover:text-blue-600 transition-colors uppercase italic">
              Q: {faq.q}
            </h3>
            <p className="text-gray-600 font-bold leading-relaxed">
              {faq.a}
            </p>
          </div>
        ))}
      </div>
    </section>
  );
};

export default FAQSection;