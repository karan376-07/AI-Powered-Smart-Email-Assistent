import React, { useState } from 'react';
import {
  Search, RefreshCw, Plus, Bell, Sparkles, AlertCircle,
  Sliders, ShieldCheck, Mail, LogOut, Sun, Moon, Mic, Globe
} from 'lucide-react';

export default function Navbar({
  searchQuery,
  setSearchQuery,
  onSync,
  isSyncing,
  onOpenCompose,
  onOpenSettings,
  unreadCount = 12,
  urgentCount = 5,
  user,
  onLogout,
  theme,
  onToggleTheme,
  language = 'en',
  onToggleLanguage,
  onOpenVoiceCommand
}) {
  const [showNotifications, setShowNotifications] = useState(false);
  const [showUserMenu, setShowUserMenu] = useState(false);

  const userName = user?.name || "Karan Elumalai";

  return (
    <header className="h-16 border-b border-slate-200 dark:border-slate-800 bg-white dark:bg-[#0C101B] px-4 lg:px-6 flex items-center justify-between z-30 sticky top-0 transition-colors select-none">
      
      {/* Brand & Logo */}
      <div className="flex items-center space-x-3 w-64">
        <div className="w-9 h-9 rounded-xl bg-indigo-600 text-white flex items-center justify-center shadow-md shadow-indigo-600/30">
          <Mail className="w-5 h-5" />
        </div>
        <div>
          <span className="font-extrabold text-base tracking-tight text-slate-900 dark:text-white block">
            AI Email Assistant
          </span>
        </div>
      </div>

      {/* Global Search Bar */}
      <div className="flex-1 max-w-xl mx-4">
        <div className="relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search emails, senders, subject..."
            className="w-full bg-slate-100 dark:bg-slate-900/90 border border-slate-200 dark:border-slate-800 rounded-xl pl-10 pr-4 py-2 text-xs text-slate-800 dark:text-slate-100 placeholder-slate-400 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition shadow-2xs font-medium"
          />
          {searchQuery && (
            <button
              onClick={() => setSearchQuery('')}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-[11px] text-slate-400 hover:text-slate-600 dark:hover:text-slate-200"
            >
              Clear
            </button>
          )}
        </div>
      </div>

      {/* Action Buttons & Profile */}
      <div className="flex items-center space-x-3">
        {/* Voice Command Button */}
        <button
          onClick={onOpenVoiceCommand}
          className="p-2 rounded-xl border border-indigo-200 dark:border-indigo-800 bg-indigo-50 dark:bg-indigo-950/60 text-indigo-600 dark:text-indigo-400 hover:bg-indigo-100 dark:hover:bg-indigo-900 transition flex items-center space-x-1 font-bold text-xs"
          title="Voice Command Assistant"
        >
          <Mic className="w-4 h-4 text-indigo-500 animate-pulse" />
          <span className="hidden md:inline">Voice</span>
        </button>

        {/* Tamil / English Language Switcher */}
        <button
          onClick={onToggleLanguage}
          className="px-2.5 py-1.5 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-100 dark:bg-slate-800 text-xs font-bold text-slate-700 dark:text-slate-200 hover:border-indigo-400 transition flex items-center space-x-1"
          title="Switch Language (English / தமிழ்)"
        >
          <Globe className="w-3.5 h-3.5 text-indigo-500" />
          <span>{language === 'ta' ? 'தமிழ் (TA)' : 'English (EN)'}</span>
        </button>

        {/* Sync Button */}
        <button
          onClick={onSync}
          disabled={isSyncing}
          className={`p-2 rounded-xl border border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition ${
            isSyncing ? 'animate-spin text-indigo-600' : ''
          }`}
          title="Sync Emails"
        >
          <RefreshCw className="w-4 h-4" />
        </button>

        {/* Theme Toggle */}
        <button
          onClick={onToggleTheme}
          className="p-2 rounded-xl border border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition"
          title={`Switch to ${theme === 'dark' ? 'Light' : 'Dark'} Mode`}
        >
          {theme === 'dark' ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4 text-indigo-600" />}
        </button>

        {/* Notifications */}
        <div className="relative">
          <button
            onClick={() => setShowNotifications(!showNotifications)}
            className="p-2 rounded-xl border border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition relative"
          >
            <Bell className="w-4 h-4" />
            <span className="absolute -top-1 -right-1 w-4 h-4 bg-rose-500 text-[10px] font-bold text-white rounded-full flex items-center justify-center">
              5
            </span>
          </button>
        </div>

        {/* User Profile Pill matching diagram "Karan Elumalai v" */}
        <div className="relative">
          <button
            onClick={onOpenSettings}
            className="flex items-center space-x-2.5 p-1 pl-2 pr-3 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-800 transition"
          >
            <img
              src={user?.avatar || user?.picture || `https://api.dicebear.com/7.x/bottts/svg?seed=Karan`}
              alt="Avatar"
              className="w-7 h-7 rounded-full bg-indigo-100 dark:bg-indigo-950 p-0.5 border border-indigo-300 dark:border-indigo-700"
            />
            <span className="text-xs font-bold text-slate-800 dark:text-slate-100 hidden sm:inline">
              {userName}
            </span>
          </button>
        </div>
      </div>
    </header>
  );
}
