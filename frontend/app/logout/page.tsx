'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '../../hooks/useAuth';
import Link from 'next/link';

const LogoutPage = () => {
  const router = useRouter();
  const { logout } = useAuth();

  useEffect(() => {
    // Perform logout automatically when the component mounts
    logout();

    // Optionally redirect after a delay to show a logout message
    const timer = setTimeout(() => {
      router.push('/');
    }, 2000);

    return () => clearTimeout(timer);
  }, [logout, router]);

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
          <div className="bg-white rounded-xl border border-gray-200 p-8 shadow-sm text-center">
            <h1 className="text-2xl font-bold mb-4">Logging Out</h1>
            <p className="text-gray-600 mb-6">
              You are being securely logged out of your account.
            </p>
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900 mx-auto"></div>
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

export default LogoutPage;