import React from 'react';

const Footer: React.FC = () => {
  const currentYear = new Date().getFullYear();

  const footerLinks = [
    { name: 'Home', href: '/' },
    { name: 'About', href: '/about' },
    { name: 'Services', href: '/services' },
    { name: 'Contact', href: '/contact' },
    { name: 'Privacy', href: '/privacy' },
    { name: 'Terms', href: '/terms' },
  ];

  return (
    <footer className="bg-[#f7a221] py-12 px-6 md:px-12 mt-auto">
      <div className="max-w-7xl mx-auto">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-8 border-b border-black/10 pb-10">
          {/* Logo Section */}
          <div className="flex items-center gap-2">
            <div className="bg-transparent border-2 border-gray-900 rounded-lg p-1.5 flex items-center justify-center">
               <span className="font-bold text-2xl text-gray-900">V</span>
            </div>
            <h2 className="text-3xl font-bold tracking-tighter text-gray-900">
              ita Check
            </h2>
          </div>

          {/* Links Grid */}
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-x-8 gap-y-4 text-sm font-medium text-gray-900">
            {footerLinks.map((link) => (
              <a 
                key={link.name} 
                href={link.href} 
                className="hover:underline whitespace-nowrap"
              >
                {link.name}
              </a>
            ))}
          </div>
        </div>

        {/* Legal and Powered By */}
        <div className="flex flex-col md:flex-row justify-between items-center mt-6 text-[10px] md:text-xs text-gray-800 font-medium tracking-wide">
          <p>© {currentYear} All Rights Reserved</p>
          <p className="mt-2 md:mt-0 uppercase tracking-widest">
            Powered by AI for Good
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;