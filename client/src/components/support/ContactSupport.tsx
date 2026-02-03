import React from 'react';

const ContactSupport: React.FC = () => {
  return (
    <div className="space-y-6">
      <h2 className="text-4xl font-black tracking-tighter text-gray-900 uppercase">Get in Touch</h2>
      <div className="grid gap-4">
        <button className="flex items-center justify-between p-6 bg-gray-900 text-white rounded-2xl hover:bg-blue-600 transition-colors w-full group">
          <span className="font-black tracking-widest uppercase">Live Chat</span>
          <span className="opacity-50 group-hover:opacity-100 group-hover:translate-x-1 transition-all">→</span>
        </button>
        <button className="flex items-center justify-between p-6 border-2 border-gray-900 text-gray-900 rounded-2xl hover:bg-gray-900 hover:text-white transition-colors w-full group">
          <span className="font-black tracking-widest uppercase">Submit Ticket</span>
          <span className="opacity-50 group-hover:opacity-100 group-hover:translate-x-1 transition-all">→</span>
        </button>
      </div>
    </div>
  );
};

export default ContactSupport;