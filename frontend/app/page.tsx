// 'use client';

// import { useRouter } from 'next/navigation';
// import { useAuth } from '../hooks/useAuth';

// export default function HomePage() {
//   const router = useRouter();
//   const { isAuthenticated } = useAuth();

//   const handleGetStarted = () => {
//     if (isAuthenticated()) {
//       router.push('/tasks');
//     } else {
//       router.push('/login');
//     }
//   };

//   return (
//     <div className="container">
//       <div className="page-content text-center">
//         <div className="max-w-2xl mx-auto">
//           <h1 className="text-4xl font-bold mb-6">Welcome to Todo App</h1>
//           <p className="text-xl text-gray-600 mb-8">
//             A secure, productivity-focused todo application to help you manage your tasks efficiently.
//           </p>

//           <div className="space-y-4">
//             <button
//               onClick={handleGetStarted}
//               className="btn btn-primary text-lg px-8 py-3"
//             >
//               Get Started
//             </button>

//             <div className="mt-8 text-left bg-gray-50 p-6 rounded-lg">
//               <h2 className="text-xl font-semibold mb-4">Features</h2>
//               <ul className="list-disc pl-6 space-y-2 text-gray-700">
//                 <li>Create and manage your personal tasks</li>
//                 <li>Mark tasks as complete/incomplete</li>
//                 <li>Secure authentication with JWT</li>
//                 <li>Clean, intuitive user interface</li>
//                 <li>Responsive design for all devices</li>
//               </ul>
//             </div>
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// }

'use client';

import { useRouter } from 'next/navigation';
import { useAuth } from '../hooks/useAuth';

export default function HomePage() {
  const router = useRouter();
  const { isAuthenticated } = useAuth();

  const handleGetStarted = () => {
    if (isAuthenticated()) {
      router.push('/tasks');
    } else {
      router.push('/login');
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-gray-50 text-gray-900">
      {/* Header */}
      <header className="border-b bg-white">
        <div className="mx-auto max-w-6xl px-6 py-4 flex items-center justify-between">
          <span className="text-lg font-semibold">Todo App</span>
          <button
            onClick={handleGetStarted}
            className="rounded-md bg-gray-900 px-4 py-2 text-sm font-medium text-white hover:bg-gray-800"
          >
            Get Started
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1">
        {/* Hero Section */}
        <section className="mx-auto max-w-6xl px-6 py-20 text-center">
          <span className="inline-block rounded-full bg-gray-100 px-4 py-1 text-xs font-medium text-gray-600">
            Secure • Simple • Productive
          </span>

          <h1 className="mt-6 text-4xl font-bold tracking-tight sm:text-5xl">
            Organize your work.<br />
            <span className="text-gray-500">Focus on what matters.</span>
          </h1>

          <p className="mx-auto mt-6 max-w-2xl text-gray-600 text-lg">
            A secure, productivity-focused todo application designed to help you
            manage your tasks efficiently without distractions.
          </p>

          <div className="mt-10">
            <button
              onClick={handleGetStarted}
              className="rounded-md bg-gray-900 px-8 py-3 text-base font-medium text-white hover:bg-gray-800"
            >
              Start Managing Tasks
            </button>
          </div>
        </section>

        {/* Features */}
        {/* <section className="bg-white py-20">
          <div className="mx-auto max-w-6xl px-6">
            <h2 className="text-center text-2xl font-semibold mb-12">
              Built for clarity and control
            </h2>

            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
              {[
                'Create and manage your personal tasks',
                'Mark tasks as complete or incomplete',
                'Secure authentication using JWT',
                'Clean and intuitive user interface',
                'Responsive design for all devices',
                'Designed for focus and productivity',
              ].map((feature) => (
                <div
                  key={feature}
                  className="rounded-xl border bg-gray-50 p-6"
                >
                  <p className="text-sm text-gray-700">{feature}</p>
                </div>
              ))}
            </div>
          </div>
        </section> */}
        <section className="bg-gradient-to-b from-indigo-50 to-white py-20">
  <div className="mx-auto max-w-6xl px-6">
    <h2 className="mb-12 text-center text-3xl font-semibold text-gray-900">
      Built for clarity and control
    </h2>

    <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
      {[
        {
          text: 'Create and manage your personal tasks',
          icon: '📝',
        },
        {
          text: 'Mark tasks as complete or incomplete',
          icon: '✅',
        },
        {
          text: 'Secure authentication using JWT',
          icon: '🔐',
        },
        {
          text: 'Clean and intuitive user interface',
          icon: '🎨',
        },
        {
          text: 'Responsive design for all devices',
          icon: '📱',
        },
        {
          text: 'Designed for focus and productivity',
          icon: '⚡',
        },
      ].map((feature) => (
        <div
          key={feature.text}
          className="group rounded-2xl border border-gray-200 bg-white p-6 shadow-sm transition-all duration-300 hover:-translate-y-1 hover:border-indigo-300 hover:shadow-lg"
        >
          <div className="mb-4 text-3xl">{feature.icon}</div>

          <p className="text-sm text-gray-700 group-hover:text-gray-900">
            {feature.text}
          </p>
        </div>
      ))}
    </div>
  </div>
</section>

      </main>

      {/* Footer */}
      <footer className="border-t bg-white">
        <div className="mx-auto max-w-6xl px-6 py-6 flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
          <p className="text-sm text-gray-500">
            © {new Date().getFullYear()} Todo App
          </p>
          <p className="text-sm text-gray-500">
            Next.js • FastAPI • JWT Authentication
          </p>
        </div>
      </footer>
    </div>
  );
}
