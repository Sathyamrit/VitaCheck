import React from 'react';
import { Link, useLocation } from 'react-router-dom';

// restored exactly as requested
export type Page = 'home' | 'about-vitacheck' | 'about-us' | 'support' | 'contact' | 'privacy' | 'auth';

const Navbar: React.FC = () => {
  const location = useLocation();

  const navLinks: { name: string; path: string; id: Page }[] = [
    { name: 'Home', path: '/', id: 'home' },
    { name: 'About VitaCheck', path: '/about-vitacheck', id: 'about-vitacheck' },
    { name: 'About Us', path: '/about-us', id: 'about-us' },
    { name: 'Support', path: '/support', id: 'support' },
    { name: 'Contact', path: '/contact', id: 'contact' },
    { name: 'Privacy', path: '/privacy', id: 'privacy' },
  ];

  // Helper to check if a path is active to apply your original UI/UX styles
  const isActive = (path: string) => location.pathname === path;

  return (
    <nav className="flex justify-between items-center px-6 md:px-12 py-4 bg-white sticky top-0 z-50 border-b border-gray-100 shadow-sm">
      {/* Brand Logo - restored to plain text as per your original design */}
      <Link 
        to="/" 
        className="flex items-center gap-2 cursor-pointer group"
      >
        <span className="text-gray-900 font-bold text-2xl tracking-tighter">
          VitaCheck
        </span>
      </Link>

      {/* Navigation */}
      <div className="hidden md:flex items-center gap-8">
        <div className="flex gap-6 text-sm font-bold uppercase tracking-tight text-gray-500">
          {navLinks.map((link) => (
            <Link
              key={link.id}
              to={link.path}
              className={`hover:text-blue-600 transition-colors cursor-pointer pb-1 ${
                isActive(link.path)? 'text-blue-600 border-b-2 border-blue-600' : ''
              }`}
            >
              {link.name}
            </Link>
          ))}
        </div>

        <div className="flex items-center gap-4 border-l border-gray-200 pl-8">
          <Link 
            to="/auth"
            className="text-sm font-black text-gray-900 hover:text-blue-600 transition-colors uppercase tracking-widest"
          >
            Login/Signup
          </Link>
        </div>
      </div>

      {/* Mobile Indicator - keeping the UX consistent */}
      <div className="md:hidden flex items-center gap-2 text-[10px] font-black uppercase text-blue-600 bg-blue-50 px-3 py-1 rounded-full">
        Menu
      </div>
    </nav>
  );
};

export default Navbar;