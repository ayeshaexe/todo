'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

const SignupPage = () => {
  const router = useRouter();

  useEffect(() => {
    // Redirect to login page and simulate clicking the signup tab
    // Since we have a unified login/signup page, we just go to login
    router.push('/login');
  }, [router]);

  return (
    <div className="container">
      <div className="page-content text-center">
        <p>Redirecting to signup...</p>
      </div>
    </div>
  );
};

export default SignupPage;