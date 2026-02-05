'use client';

import { useState } from 'react';
import Link from 'next/link';
import LoginForm from '../../components/auth/LoginForm';
import SignupForm from '../../components/auth/SignupForm';

const LoginPage = () => {
  const [showLogin, setShowLogin] = useState(true);

  return (
    <div className="min-h-screen flex flex-col bg-gray-50 text-gray-900">
      {/* Header */}
      <header className="border-b bg-white">
        <div className="mx-auto max-w-6xl px-6 py-4 flex items-center justify-between">
          <Link href="/" className="text-lg font-semibold">Todo App</Link>
          <Link
            href="/"
            className="rounded-md bg-gray-900 px-4 py-2 text-sm font-medium text-white hover:bg-gray-800"
          >
            Back to Home
          </Link>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 flex items-center justify-center py-12">
        <div className="mx-auto max-w-md w-full px-6">
          <div className="bg-white rounded-xl border border-gray-200 p-8 shadow-sm">
            <h1 className="text-2xl font-bold mb-6 text-center">
              {showLogin ? 'Welcome Back' : 'Create Account'}
            </h1>

            {showLogin ? (
              <>
                <LoginForm
                  onSwitchToSignup={() => setShowLogin(false)}
                />
                <div className="mt-6 text-center">
                  <p className="text-sm text-gray-600">
                    By signing in, you agree to our Terms of Service and Privacy Policy.
                  </p>
                </div>
              </>
            ) : (
              <>
                <SignupForm
                  onSwitchToLogin={() => setShowLogin(true)}
                />
                <div className="mt-6 text-center">
                  <p className="text-sm text-gray-600">
                    By creating an account, you agree to our Terms of Service and Privacy Policy.
                  </p>
                </div>
              </>
            )}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t bg-white py-6">
        <div className="mx-auto max-w-6xl px-6 text-center">
          <p className="text-sm text-gray-500">
            © {new Date().getFullYear()} Todo App
          </p>
        </div>
      </footer>
    </div>
  );
};

export default LoginPage;