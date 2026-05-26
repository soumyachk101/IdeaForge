import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import Link from "next/link";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "IdeaForge - Micro-SaaS Idea Discovery Engine",
  description:
    "Multi-agent AI system that discovers, analyzes, and proposes monetizable micro-SaaS ideas",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col bg-zinc-50 dark:bg-zinc-950 text-zinc-900 dark:text-zinc-100">
        {/* Navigation */}
        <nav className="border-b border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between h-16">
              <Link href="/" className="flex items-center gap-2">
                <span className="text-2xl">&#9889;</span>
                <span className="text-xl font-bold tracking-tight">IdeaForge</span>
              </Link>
              <div className="flex items-center gap-6">
                <Link
                  href="/"
                  className="text-sm font-medium text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-100 transition-colors"
                >
                  Generate
                </Link>
                <Link
                  href="/ideas"
                  className="text-sm font-medium text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-100 transition-colors"
                >
                  Ideas
                </Link>
                <Link
                  href="/trends"
                  className="text-sm font-medium text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-100 transition-colors"
                >
                  Trends
                </Link>
                <Link
                  href="/knowledge"
                  className="text-sm font-medium text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-100 transition-colors"
                >
                  Knowledge Base
                </Link>
                <a
                  href="http://127.0.0.1:8000/docs"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-sm font-medium text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-100 transition-colors"
                >
                  API Docs
                </a>
              </div>
            </div>
          </div>
        </nav>

        {/* Main Content */}
        <main className="flex-1">{children}</main>

        {/* Footer */}
        <footer className="border-t border-zinc-200 dark:border-zinc-800 py-4 text-center text-sm text-zinc-500">
          IdeaForge v0.1.0 &mdash; Multi-Agent Micro-SaaS Idea Discovery Engine
        </footer>
      </body>
    </html>
  );
}
