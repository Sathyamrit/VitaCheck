import React from 'react';
import { GoogleLogin } from '@react-oauth/google';
import type { CredentialResponse } from '@react-oauth/google';
import { jwtDecode } from 'jwt-decode';

const GoogleAuthButton: React.FC = () => {
  const handleSuccess = (response: CredentialResponse) => {
    if (response.credential) {
      const userProfile: any = jwtDecode(response.credential);
      console.log('User Profile to Store:', {
        googleId: userProfile.sub,
        email: userProfile.email,
        name: userProfile.name,
        picture: userProfile.picture,
      });
      // ACTION: Send this payload to your Node.js API /api/auth/google
      // Store returned JWT in localStorage or secure cookies 
    }
  };

  return (
    <div className="w-full flex justify-center">
      <GoogleLogin 
        onSuccess={handleSuccess} 
        onError={() => console.log('Login Failed')}
        useOneTap
        shape="pill"
        theme="outline"
        text="continue_with"
        width="100%"
      />
    </div>
  );
};

export default GoogleAuthButton;