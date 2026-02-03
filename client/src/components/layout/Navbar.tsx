import React from 'react';

export type Page = 'home' | 'about-vitacheck' | 'about-us' | 'support' | 'contact' | 'privacy' | 'auth';

interface NavbarProps {
  onNavigate: (page: Page) => void;
  activePage: Page;
}

const Navbar: React.FC<NavbarProps> = ({ onNavigate, activePage }) => {
  const navLinks: { name: string; id: Page }[] = [
    { name: 'Home', id: 'home' },
    { name: 'About VitaCheck', id: 'about-vitacheck' },
    { name: 'About Us', id: 'about-us' },
    { name: 'Support', id: 'support' },
    { name: 'Contact', id: 'contact' },
    { name: 'Privacy', id: 'privacy' },
  ];

  return (
    <nav className="flex justify-between items-center px-6 md:px-12 py-4 bg-white sticky top-0 z-50 border-b border-gray-100 shadow-sm">
      <div 
        className="flex items-center gap-2 cursor-pointer group"
        onClick={() => onNavigate('home')}
      >
        <span className="text-gray-900 font-bold text-2xl tracking-tighter">
          VitaCheck
        </span>
      </div>

      {/* Navigation */}
      <div className="hidden md:flex items-center gap-8">
        <div className="flex gap-6 text-sm font-bold uppercase tracking-tight text-gray-500">
          {navLinks.map((link) => (
            <button
              key={link.id}
              onClick={() => onNavigate(link.id)}
              className={`hover:text-blue-600 transition-colors cursor-pointer ${
                activePage === link.id? 'text-blue-600 border-b-2 border-blue-600' : ''
              }`}
            >
              {link.name}
            </button>
          ))}
        </div>

        <div className="flex items-center gap-4 border-l border-gray-200 pl-8">
           <button 
            onClick={() => onNavigate('auth')}
            className="text-sm font-black text-gray-900 hover:text-blue-600 transition-colors uppercase tracking-widest"
          >
            Login/Signup
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;