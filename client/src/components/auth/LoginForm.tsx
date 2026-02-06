import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

const LoginForm: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  // Get the redirect path from Hero or default to dashboard
  const from = (location.state as any)?.from || "/dashboard";

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    
    // Simulate API call to your Node.js backend
    setTimeout(() => {
      localStorage.setItem('token', 'fake-jwt-token'); // Save session
      setLoading(false);
      navigate(from, { replace: true });
    }, 1500);
  };

  const handleGoogleLogin = () => {
    // This is where the COOP error usually happens
    // Make sure your Google Developer Console has 'http://localhost:3000' (or your port) 
    // in the "Authorized JavaScript origins"
    console.log("Triggering Google OAuth...");
  };

  return (
    <div className="space-y-6">
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
          {loading ? 'Verifying...' : 'Sign In'}
        </button>
      </form>

      <div className="relative flex items-center py-2">
        <div className="flex-grow border-t border-gray-200"></div>
        <span className="flex-shrink mx-4 text-[10px] font-black text-gray-400 uppercase">OR</span>
        <div className="flex-grow border-t border-gray-200"></div>
      </div>

      {/* Google Login Button */}
      <button 
        onClick={handleGoogleLogin}
        className="w-full bg-white border-2 border-gray-100 text-gray-900 py-4 rounded-full font-black uppercase tracking-widest hover:bg-gray-50 transition-all flex items-center justify-center gap-3 shadow-sm"
      >
        <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" className="w-5 h-5" alt="Google" />
        Continue with Google
      </button>
    </div>
  );
};

export default LoginForm;