import React, { useState } from 'react';

const SignupForm: React.FC = () => {
  const [loading, setLoading] = useState(false);

  const handleSignup = (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    // Data payload will be sent to the Node.js backend to initialize MongoDB profile [3, 4]
    setTimeout(() => setLoading(false), 1500);
  };

  return (
    <form onSubmit={handleSignup} className="space-y-4 animate-in slide-in-from-bottom-2 duration-500">
      <div className="space-y-1">
        <label className="text-[10px] font-black uppercase tracking-widest text-gray-400 ml-1">Full Name</label>
        <input 
          type="text" 
          required
          className="w-full bg-gray-50 border-2 border-transparent focus:border-[#f7a221] rounded-2xl py-4 px-6 font-bold text-gray-900 outline-none transition-all uppercase tracking-tight"
          placeholder="John Doe"
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-1">
          <label className="text-[10px] font-black uppercase tracking-widest text-gray-400 ml-1">Age</label>
          <input 
            type="number" 
            required
            className="w-full bg-gray-50 border-2 border-transparent focus:border-[#f7a221] rounded-2xl py-4 px-6 font-bold text-gray-900 outline-none transition-all"
            placeholder="25"
          />
        </div>
        <div className="space-y-1">
          <label className="text-[10px] font-black uppercase tracking-widest text-gray-400 ml-1">Gender</label>
          <select className="w-full bg-gray-50 border-2 border-transparent focus:border-[#f7a221] rounded-2xl py-4 px-6 font-bold text-gray-900 outline-none transition-all appearance-none cursor-pointer">
            <option value="male">MALE</option>
            <option value="female">FEMALE</option>
            <option value="other">OTHER</option>
          </select>
        </div>
      </div>

      <div className="space-y-1">
        <label className="text-[10px] font-black uppercase tracking-widest text-gray-400 ml-1">Email Address</label>
        <input 
          type="email" 
          required
          className="w-full bg-gray-50 border-2 border-transparent focus:border-[#f7a221] rounded-2xl py-4 px-6 font-bold text-gray-900 outline-none transition-all"
          placeholder="name@example.com"
        />
      </div>

      <div className="space-y-1">
        <label className="text-[10px] font-black uppercase tracking-widest text-gray-400 ml-1">Create Password</label>
        <input 
          type="password" 
          required
          className="w-full bg-gray-50 border-2 border-transparent focus:border-[#f7a221] rounded-2xl py-4 px-6 font-bold text-gray-900 outline-none transition-all"
          placeholder="••••••••"
        />
      </div>

      <div className="flex items-start gap-3 px-2 py-2">
        <input type="checkbox" required className="mt-1 accent-[#f7a221]" />
        <p className="text-[9px] font-bold text-gray-400 leading-tight">
          I CONSENT TO THE PROCESSING OF MY SYMPTOM DATA IN ACCORDANCE WITH GDPR & HIPAA PRIVACY STANDARDS. [4, 5]
        </p>
      </div>

      <button 
        disabled={loading}
        className="w-full bg-gray-900 text-white py-5 rounded-full font-black uppercase tracking-[0.2em] hover:bg-[#f7a221] hover:text-gray-900 transition-all shadow-xl disabled:opacity-50"
      >
        {loading? 'CREATING ACCOUNT...' : 'START YOUR MISSION'}
      </button>
    </form>
  );
};

export default SignupForm;