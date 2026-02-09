import React, { useState } from 'react';
import LoginForm from '../components/auth/LoginForm';
import SignupForm from '../components/auth/SignupForm';
import GoogleAuthButton from '../components/auth/GoogleAuthButton';

const Auth: React.FC = () => {
  const [isLogin, setIsLogin] = useState(true);

  return (
    <div className="min-h-screen bg-white flex flex-col md:flex-row animate-in fade-in duration-700">
      {/* Visual Side - Brand Identity */}
      <div className="md:w-1/2 bg-[#f7a221] p-12 flex flex-col justify-between min-h-[300px] md:min-h-screen">
        <div className="flex items-center gap-3">
          <h2 className="text-4xl font-black tracking-tighter text-gray-900 uppercase">VitaCheck</h2>
        </div>
        
        <div className="max-w-md">
          <h1 className="text-5xl md:text-7xl font-black text-gray-900 tracking-tighter leading-none mb-6 uppercase">
            {isLogin? 'WELCOME BACK.' : 'JOIN THE MISSION.'}
          </h1>
          <p className="text-xl text-gray-900 font-bold leading-tight">
            Securely access your AI-driven health assessments and personalized recovery roadmaps.
          </p>
        </div>
        
        {/* <div className="text-[10px] font-black uppercase tracking-[0.2em] text-gray-900 opacity-60">
          HIPAA & GDPR COMPLIANT INFRASTRUCTURE 
        </div> */}
      </div>

      {/* Form Side */}
      <div className="md:w-1/2 flex items-center justify-center p-8 md:p-24 bg-white">
        <div className="w-full max-w-sm space-y-8">
          <div className="space-y-2">
            <h2 className="text-3xl font-black tracking-tighter text-gray-900 uppercase">
              {isLogin? 'Sign In' : 'Create Account'}
            </h2>
            <p className="text-gray-500 font-bold text-sm">
              {isLogin? "Don't have an account?" : "Already have an account?"} 
              <button 
                onClick={() => setIsLogin(!isLogin)}
                className="ml-2 text-blue-600 hover:underline underline-offset-4"
              >
                {isLogin? 'Sign up for free' : 'Log in here'}
              </button>
            </p>
          </div>

          {/* Social Auth */}
          <GoogleAuthButton />

          <div className="relative">
            <div className="absolute inset-0 flex items-center"><span className="w-full border-t border-gray-100"></span></div>
            <div className="relative flex justify-center text-xs uppercase font-black text-gray-400">
              <span className="bg-white px-4 tracking-widest">Or continue with</span>
            </div>
          </div>

          {/* Manual Auth Forms */}
          {isLogin? <LoginForm /> : <SignupForm />}
        </div>
      </div>
    </div>
  );
};

export default Auth;