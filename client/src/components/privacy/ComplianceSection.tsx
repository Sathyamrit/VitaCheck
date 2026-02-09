import React from 'react';

const ComplianceSection: React.FC = () => {
  return (
    <div className="sticky top-32 space-y-8">
      <div className="p-8 bg-gray-900 rounded-[2.5rem] text-white">
        <h3 className="text-xl font-black tracking-tighter mb-6 uppercase">Security Stack</h3>
        <div className="space-y-6">
          <div className="flex items-center gap-4">
            <div className="w-10 h-10 rounded-lg bg-[#f7a221] flex items-center justify-center font-black text-gray-900 text-xs">AES</div>
            <p className="text-xs font-bold text-gray-400">256-bit Encryption for data at rest.</p>
          </div>
          <div className="flex items-center gap-4">
            <div className="w-10 h-10 rounded-lg bg-blue-600 flex items-center justify-center font-black text-white text-xs">TLS</div>
            <p className="text-xs font-bold text-gray-400">1.2+ Secure Transit for API communication.</p>
          </div>
          <div className="flex items-center gap-4">
            <div className="w-10 h-10 rounded-lg bg-green-600 flex items-center justify-center font-black text-white text-xs">ISO</div>
            <p className="text-xs font-bold text-gray-400">HIPAA & GDPR Compliant Infrastructure.</p>
          </div>
        </div>
      </div>

      <div className="p-8 border-2 border-gray-100 rounded-[2.5rem]">
        <h3 className="text-lg font-black tracking-tighter text-gray-900 mb-4 uppercase">Medical Disclaimer</h3>
        <p className="text-xs font-bold text-gray-500 leading-relaxed italic">
          VitaCheck results are for informational purposes only and do not constitute medical advice. Always consult a healthcare professional 
          before starting new dietary supplements.
        </p>
      </div>
    </div>
  );
};

export default ComplianceSection;