import React from 'react';
import {
  Sparkles, ShieldCheck, Mail, ArrowRight,
  Mic, Lock, Bot, FileText, CheckCircle2
} from 'lucide-react';

export default function LandingPage({ onConnectGmail, onQuickAccess, theme, onToggleTheme }) {
  return (
    <div className="min-h-screen bg-[#070A12] text-white flex flex-col justify-between relative overflow-x-hidden font-sans select-none">
      {/* Dynamic Background Glow FX */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[1000px] h-[550px] bg-gradient-to-tr from-indigo-600/20 via-purple-600/20 to-blue-600/20 rounded-full blur-[140px] pointer-events-none" />
      <div className="absolute bottom-10 right-10 w-[450px] h-[450px] bg-indigo-500/10 rounded-full blur-[120px] pointer-events-none" />

      {/* Top Header */}
      <header className="p-5 max-w-7xl mx-auto w-full flex items-center justify-between relative z-20">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-indigo-500 via-purple-500 to-blue-500 p-0.5 flex items-center justify-center shadow-lg shadow-indigo-500/30">
            <div className="w-full h-full bg-[#0B0F1D] rounded-[14px] flex items-center justify-center">
              <Mail className="w-5 h-5 text-indigo-400" />
            </div>
          </div>
          <div>
            <span className="font-extrabold text-base tracking-tight text-white block">
              AI Email Assistant
            </span>
            <span className="text-[10px] text-slate-400 font-medium tracking-wide">
              Smart. Secure. Productive.
            </span>
          </div>
        </div>

        <div className="flex items-center space-x-3">
          <button
            onClick={onQuickAccess}
            className="text-xs font-semibold px-4 py-2 text-slate-300 hover:text-white transition"
          >
            Sign In
          </button>
          <button
            onClick={onConnectGmail}
            className="text-xs font-bold px-4 py-2 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white shadow-lg shadow-indigo-600/30 transition duration-200 transform hover:-translate-y-0.5"
          >
            Get Started
          </button>
        </div>
      </header>

      {/* Hero Section */}
      <main className="max-w-7xl mx-auto px-6 py-8 md:py-16 relative z-10 flex-1 flex flex-col justify-center">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          
          {/* Left Hero Text Column */}
          <div className="lg:col-span-7 space-y-6 text-left">
            <div className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-indigo-950/60 border border-indigo-800/60 text-indigo-300 text-xs font-semibold shadow-inner">
              <Sparkles className="w-3.5 h-3.5 text-indigo-400 animate-pulse" />
              <span>Next-Gen Gemini AI Email Engine</span>
            </div>

            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-black tracking-tight leading-[1.1] text-white">
              Your AI-Powered <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-indigo-300 to-purple-400">
                Smart Email Assistant
              </span>
            </h1>

            <p className="text-base sm:text-lg text-indigo-200/90 font-medium tracking-wide">
              Organize. Summarize. Prioritize. Respond.
            </p>

            <p className="text-sm sm:text-base text-slate-400 max-w-xl leading-relaxed">
              Let AI handle the noise. Get the right emails, at the right time, with smart summaries, security alerts and personalized replies.
            </p>

            {/* Action CTA Buttons */}
            <div className="flex flex-wrap items-center gap-4 pt-2">
              <button
                onClick={onConnectGmail}
                className="px-6 py-3.5 rounded-2xl bg-white hover:bg-slate-100 text-slate-900 font-extrabold text-sm flex items-center space-x-3 shadow-xl shadow-indigo-500/10 transition duration-200 transform hover:-translate-y-0.5 group"
              >
                <svg className="w-5 h-5 shrink-0" viewBox="0 0 24 24">
                  <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                  <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                  <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
                  <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
                </svg>
                <span>Connect with Gmail</span>
              </button>

              <button
                onClick={onQuickAccess}
                className="px-6 py-3.5 rounded-2xl bg-slate-900/90 hover:bg-slate-800 border border-slate-700/80 text-slate-200 font-bold text-sm flex items-center space-x-2 transition duration-200"
              >
                <span>Learn More</span>
                <ArrowRight className="w-4 h-4 text-indigo-400 group-hover:translate-x-1 transition" />
              </button>
            </div>
          </div>

          {/* Right Floating 3D Graphic Mockup */}
          <div className="lg:col-span-5 relative flex items-center justify-center">
            {/* Outer Glow backdrop */}
            <div className="w-72 h-72 sm:w-96 sm:h-96 rounded-full bg-gradient-to-tr from-indigo-500/30 to-purple-500/30 blur-2xl absolute"></div>

            {/* Central 3D Card Glass Graphic */}
            <div className="relative z-10 w-full max-w-md p-8 rounded-3xl bg-[#0F1528]/80 border border-indigo-500/30 backdrop-blur-2xl shadow-2xl shadow-indigo-950/60 flex flex-col items-center justify-center space-y-6 transform hover:scale-[1.02] transition duration-300">
              
              {/* Center Floating Icon Box */}
              <div className="relative w-28 h-28 rounded-3xl bg-gradient-to-tr from-indigo-600 via-purple-600 to-blue-500 p-1 shadow-2xl shadow-indigo-500/40 animate-pulse-slow">
                <div className="w-full h-full bg-[#0A0E1A] rounded-[22px] flex items-center justify-center">
                  <div className="relative">
                    <Mail className="w-12 h-12 text-indigo-400" />
                    <span className="absolute -bottom-1 -right-1 px-1.5 py-0.5 rounded-full bg-indigo-600 text-[10px] font-black text-white border border-indigo-400">AI</span>
                  </div>
                </div>
              </div>

              {/* Orbiting Satellite Badges */}
              <div className="grid grid-cols-3 gap-3 w-full pt-2">
                <div className="p-3 rounded-2xl bg-slate-900/80 border border-slate-800 flex flex-col items-center text-center">
                  <div className="w-8 h-8 rounded-xl bg-red-950/60 border border-red-800/60 flex items-center justify-center mb-1">
                    <span className="text-red-400 font-extrabold text-xs">M</span>
                  </div>
                  <span className="text-[10px] font-semibold text-slate-400">Gmail Sync</span>
                </div>

                <div className="p-3 rounded-2xl bg-slate-900/80 border border-slate-800 flex flex-col items-center text-center">
                  <div className="w-8 h-8 rounded-xl bg-indigo-950/60 border border-indigo-800/60 flex items-center justify-center mb-1">
                    <Mic className="w-4 h-4 text-indigo-400" />
                  </div>
                  <span className="text-[10px] font-semibold text-slate-400">Voice Control</span>
                </div>

                <div className="p-3 rounded-2xl bg-slate-900/80 border border-slate-800 flex flex-col items-center text-center">
                  <div className="w-8 h-8 rounded-xl bg-emerald-950/60 border border-emerald-800/60 flex items-center justify-center mb-1">
                    <ShieldCheck className="w-4 h-4 text-emerald-400" />
                  </div>
                  <span className="text-[10px] font-semibold text-slate-400">Phishing Shield</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom 4 Feature Cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-16 pt-8 border-t border-slate-800/80">
          <div className="p-4 rounded-2xl bg-slate-900/40 border border-slate-800/80 flex items-center space-x-3 text-left">
            <div className="w-10 h-10 rounded-xl bg-indigo-950/80 border border-indigo-800/60 flex items-center justify-center shrink-0">
              <Bot className="w-5 h-5 text-indigo-400" />
            </div>
            <div>
              <h4 className="text-xs font-bold text-white">Smart Summarization</h4>
              <p className="text-[11px] text-slate-400">3-bullet point executive key highlights</p>
            </div>
          </div>

          <div className="p-4 rounded-2xl bg-slate-900/40 border border-slate-800/80 flex items-center space-x-3 text-left">
            <div className="w-10 h-10 rounded-xl bg-rose-950/80 border border-rose-800/60 flex items-center justify-center shrink-0">
              <ShieldCheck className="w-5 h-5 text-rose-400" />
            </div>
            <div>
              <h4 className="text-xs font-bold text-white">Spam & Phishing Detection</h4>
              <p className="text-[11px] text-slate-400">Real-time domain & link safety verification</p>
            </div>
          </div>

          <div className="p-4 rounded-2xl bg-slate-900/40 border border-slate-800/80 flex items-center space-x-3 text-left">
            <div className="w-10 h-10 rounded-xl bg-purple-950/80 border border-purple-800/60 flex items-center justify-center shrink-0">
              <FileText className="w-5 h-5 text-purple-400" />
            </div>
            <div>
              <h4 className="text-xs font-bold text-white">Personalized Reply</h4>
              <p className="text-[11px] text-slate-400">Smart 1-click tone suggestions</p>
            </div>
          </div>

          <div className="p-4 rounded-2xl bg-slate-900/40 border border-slate-800/80 flex items-center space-x-3 text-left">
            <div className="w-10 h-10 rounded-xl bg-blue-950/80 border border-blue-800/60 flex items-center justify-center shrink-0">
              <Mic className="w-5 h-5 text-blue-400" />
            </div>
            <div>
              <h4 className="text-xs font-bold text-white">Voice Command</h4>
              <p className="text-[11px] text-slate-400">Search, read, and compose via voice</p>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="p-4 text-center text-xs text-slate-500 border-t border-slate-900 relative z-20">
        AI-Powered Smart Email Assistant • Google Workspace & Gemini NLP Integration
      </footer>
    </div>
  );
}
