import React from 'react';

const ContactDetails: React.FC = () => {
  return (
    <aside className="space-y-12">
      <div>
        <h3 className="text-sm font-black text-[#f7a221] uppercase tracking-[0.3em] mb-4">Direct Lines</h3>
        <div className="space-y-4">
          <p className="text-3xl font-black tracking-tighter text-gray-900 underline decoration-[#f7a221] decoration-4">
            support@vitacheck.ai
          </p>
          <p className="text-xl font-bold text-gray-500">1-800-VITA-HELP</p>
        </div>
      </div>

      <div className="p-10 bg-gray-900 rounded-[3rem] text-white">
        <h3 className="text-xl font-black tracking-tighter mb-6 uppercase">Privacy & Data</h3>
        <p className="text-gray-400 font-bold leading-relaxed mb-8 text-sm">
          Your communications are protected. We utilize end-to-end AES-256 encryption 
          for all messages containing symptom descriptions to ensure HIPAA compliance.[2, 3]
        </p>
        <div className="flex gap-4">
          <div className="w-12 h-12 rounded-full border border-gray-700 flex items-center justify-center font-black text-[10px]">GDPR</div>
          <div className="w-12 h-12 rounded-full border border-gray-700 flex items-center justify-center font-black text-[10px]">HIPAA</div>
          <div className="w-12 h-12 rounded-full border border-gray-700 flex items-center justify-center font-black text-[10px]">AES</div>
        </div>
      </div>
      
      <div className="pt-6 border-t border-gray-100">
        <h4 className="font-black text-gray-900 uppercase tracking-widest text-xs mb-2">Office Hours</h4>
        <p className="font-bold text-gray-500 text-sm italic underline">Mon — Fri: 9:00 AM - 6:00 PM EST</p>
      </div>
    </aside>
  );
};

export default ContactDetails;