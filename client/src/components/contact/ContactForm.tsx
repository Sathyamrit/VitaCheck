import React, { useState } from 'react';

interface FormState {
  name: string;
  email: string;
  subject: string;
  message: string;
}

const ContactForm: React.FC = () => {
  const [formData, setFormData] = useState<FormState>({ name: '', email: '', subject: '', message: '' });
  const [status, setStatus] = useState<'idle' | 'submitting' | 'success'>('idle');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus('submitting');
    // Simulated Node.js API call [1]
    setTimeout(() => setStatus('success'), 1500);
  };

  if (status === 'success') {
    return (
      <div className="p-12 bg-blue-50 rounded-[2.5rem] border border-blue-100 text-center">
        <div className="text-4xl mb-4">✅</div>
        <h3 className="text-2xl font-black tracking-tight text-blue-900 mb-2 uppercase">Message Received</h3>
        <p className="text-blue-700 font-bold">Our clinical support team will respond within 24 hours.</p>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid md:grid-cols-2 gap-6">
        <input 
          type="text" 
          placeholder="YOUR NAME" 
          required
          className="w-full bg-gray-50 border-none rounded-2xl py-5 px-8 font-black text-gray-900 placeholder-gray-400 focus:ring-4 focus:ring-[#f7a221]/20 outline-none uppercase tracking-widest text-xs"
          onChange={(e) => setFormData({...formData, name: e.target.value})}
        />
        <input 
          type="email" 
          placeholder="EMAIL ADDRESS" 
          required
          className="w-full bg-gray-50 border-none rounded-2xl py-5 px-8 font-black text-gray-900 placeholder-gray-400 focus:ring-4 focus:ring-[#f7a221]/20 outline-none uppercase tracking-widest text-xs"
          onChange={(e) => setFormData({...formData, email: e.target.value})}
        />
      </div>
      <input 
        type="text" 
        placeholder="SUBJECT" 
        className="w-full bg-gray-50 border-none rounded-2xl py-5 px-8 font-black text-gray-900 placeholder-gray-400 focus:ring-4 focus:ring-[#f7a221]/20 outline-none uppercase tracking-widest text-xs"
        onChange={(e) => setFormData({...formData, subject: e.target.value})}
      />
      <textarea 
        placeholder="HOW CAN WE ASSIST YOUR HEALTH JOURNEY?" 
        rows={6}
        required
        className="w-full bg-gray-50 border-none rounded-[2rem] py-6 px-8 font-bold text-gray-900 placeholder-gray-400 focus:ring-4 focus:ring-[#f7a221]/20 outline-none tracking-tight"
        onChange={(e) => setFormData({...formData, message: e.target.value})}
      />
      <button 
        disabled={status === 'submitting'}
        className="w-full bg-gray-900 text-white py-6 rounded-full font-black uppercase tracking-[0.2em] hover:bg-blue-600 transition-all shadow-xl disabled:opacity-50"
      >
        {status === 'submitting'? 'PROCESSING...' : 'SEND MESSAGE'}
      </button>
    </form>
  );
};

export default ContactForm;