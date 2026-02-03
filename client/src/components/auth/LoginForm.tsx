import React, { useState } from 'react';

const LoginForm: React.FC = () => {
  const [loading, setLoading] = useState(false);

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    // Simulating Node.js API Gateway authentication 
    setTimeout(() => setLoading(false), 1500);
  };

  return (
    <form onSubmit={handleLogin} className="space-y-4 animate-in slide-in-from-bottom-2 duration-500">
      <div className="space-y-1">
        <label className="text-[10px] font-black uppercase tracking-widest text-gray-400 ml-1">Email Address</label>
        <input 
          type="email" 
          required
          className="w-full bg-gray-50 border-2 border-transparent focus:border-[#f7a221] rounded-2xl py-4 px-6 font-bold text-gray-900 outline-none transition-all placeholder:text-gray-300"
          placeholder="name@example.com"
        />
      </div>
      
      <div className="space-y-1">
        <div className="flex justify-between items-center px-1">
          <label className="text-[10px] font-black uppercase tracking-widest text-gray-400">Password</label>
          <button type="button" className="text-[10px] font-black uppercase tracking-widest text-blue-600 hover:underline">Forgot?</button>
        </div>
        <input 
          type="password" 
          required
          className="w-full bg-gray-50 border-2 border-transparent focus:border-[#f7a221] rounded-2xl py-4 px-6 font-bold text-gray-900 outline-none transition-all placeholder:text-gray-300"
          placeholder="••••••••"
        />
      </div>

      <button 
        disabled={loading}
        className="w-full bg-gray-900 text-white py-5 rounded-full font-black uppercase tracking-[0.2em] hover:bg-[#f7a221] hover:text-gray-900 transition-all shadow-xl disabled:opacity-50 mt-4"
      >
        {loading? 'Verifying...' : 'Sign In'}
      </button>
    </form>
  );
};

export default LoginForm;