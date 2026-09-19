import React, { useState, useEffect } from 'react';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, Legend
} from 'recharts';
import {
  Sparkles, Clock, ShieldCheck, MailCheck, AlertCircle,
  TrendingUp, Users, ArrowLeft, RefreshCw
} from 'lucide-react';
import { analyticsAPI } from '../services/api';

const COLORS = ['#4F46E5', '#059669', '#D97706', '#9333EA', '#DB2777', '#E11D48', '#0284C7'];

export default function AnalyticsDashboard({ onBack }) {
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  const loadAnalytics = async () => {
    setIsLoading(true);
    try {
      const res = await analyticsAPI.getSummary();
      setData(res);
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadAnalytics();
  }, []);

  if (isLoading || !data) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center p-12 text-slate-500 bg-white dark:bg-[#0A0E18]">
        <RefreshCw className="w-8 h-8 text-indigo-600 dark:text-indigo-400 animate-spin mb-3" />
        <p className="text-xs font-semibold">Computing AI inbox efficiency analytics...</p>
      </div>
    );
  }

  const pieData = Object.entries(data.category_distribution || {}).map(([name, value]) => ({
    name,
    value
  }));

  return (
    <div className="flex-1 flex flex-col h-full bg-white dark:bg-[#0A0E18] overflow-y-auto p-4 lg:p-8 transition-colors">
      {/* Header */}
      <div className="flex items-center justify-between pb-4 border-b border-slate-200 dark:border-slate-800/80 mb-6">
        <div className="flex items-center space-x-3">
          {onBack && (
            <button
              onClick={onBack}
              className="p-2 rounded-xl text-slate-500 hover:text-slate-900 hover:bg-slate-100 dark:hover:bg-slate-800 transition"
            >
              <ArrowLeft className="w-5 h-5" />
            </button>
          )}
          <div>
            <h1 className="text-xl font-bold text-slate-900 dark:text-white tracking-tight flex items-center space-x-2">
              <TrendingUp className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
              <span>AI Email Intelligence & Analytics</span>
            </h1>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
              Live metrics on email triage speed, NLP classification breakdown, and AI workload savings.
            </p>
          </div>
        </div>

        <button
          onClick={loadAnalytics}
          className="flex items-center space-x-1.5 px-3 py-1.5 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-xs font-bold text-slate-700 dark:text-slate-200 border border-slate-200 dark:border-transparent transition shadow-xs"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Refresh</span>
        </button>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {/* Card 1 */}
        <div className="p-4 rounded-2xl bg-gradient-to-br from-indigo-50 to-white dark:from-indigo-950/40 dark:to-slate-900 border border-indigo-200 dark:border-indigo-500/20 shadow-xs">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">Total Processed</span>
            <div className="p-2 rounded-xl bg-indigo-100 dark:bg-indigo-500/20 text-indigo-600 dark:text-indigo-400">
              <MailCheck className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-extrabold text-slate-900 dark:text-white tracking-tight">{data.total_emails}</div>
          <p className="text-[11px] text-indigo-700 dark:text-indigo-300/80 mt-1 font-semibold flex items-center space-x-1">
            <span>100% NLP indexed</span>
          </p>
        </div>

        {/* Card 2 */}
        <div className="p-4 rounded-2xl bg-gradient-to-br from-emerald-50 to-white dark:from-emerald-950/40 dark:to-slate-900 border border-emerald-200 dark:border-emerald-500/20 shadow-xs">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">Time Saved by AI</span>
            <div className="p-2 rounded-xl bg-emerald-100 dark:bg-emerald-500/20 text-emerald-600 dark:text-emerald-400">
              <Clock className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-extrabold text-emerald-700 dark:text-emerald-300 tracking-tight">{data.time_saved_hours} hrs</div>
          <p className="text-[11px] text-emerald-800 dark:text-emerald-400/80 mt-1 font-semibold">~5.2 mins saved per email</p>
        </div>

        {/* Card 3 */}
        <div className="p-4 rounded-2xl bg-gradient-to-br from-rose-50 to-white dark:from-rose-950/40 dark:to-slate-900 border border-rose-200 dark:border-rose-500/20 shadow-xs">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">Spam Shielded</span>
            <div className="p-2 rounded-xl bg-rose-100 dark:bg-rose-500/20 text-rose-600 dark:text-rose-400">
              <ShieldCheck className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-extrabold text-rose-700 dark:text-rose-300 tracking-tight">{data.spam_blocked}</div>
          <p className="text-[11px] text-rose-800 dark:text-rose-400/80 mt-1 font-semibold">Phishing & malicious filters</p>
        </div>

        {/* Card 4 */}
        <div className="p-4 rounded-2xl bg-gradient-to-br from-amber-50 to-white dark:from-amber-950/40 dark:to-slate-900 border border-amber-200 dark:border-amber-500/20 shadow-xs">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">Urgent Pending</span>
            <div className="p-2 rounded-xl bg-amber-100 dark:bg-amber-500/20 text-amber-600 dark:text-amber-400">
              <AlertCircle className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-extrabold text-amber-700 dark:text-amber-300 tracking-tight">{data.urgent_count}</div>
          <p className="text-[11px] text-amber-800 dark:text-amber-400/80 mt-1 font-semibold">Requires user attention</p>
        </div>
      </div>

      {/* Visual Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 mb-6">
        {/* Weekly Email Sync & AI Volume */}
        <div className="lg:col-span-7 p-5 rounded-2xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 shadow-xs">
          <h3 className="text-xs font-bold text-slate-800 dark:text-slate-200 uppercase tracking-wider mb-4 flex items-center space-x-2">
            <Sparkles className="w-4 h-4 text-indigo-600 dark:text-indigo-400" />
            <span>Weekly Email Volume & AI Summarization Load</span>
          </h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data.daily_volume}>
                <XAxis dataKey="day" stroke="#94A3B8" fontSize={11} tickLine={false} />
                <YAxis stroke="#94A3B8" fontSize={11} tickLine={false} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#1E293B', borderColor: '#334155', borderRadius: '12px', fontSize: '11px', color: '#F8FAFC' }}
                />
                <Bar dataKey="received" name="Total Inbound" fill="#4F46E5" radius={[4, 4, 0, 0]} />
                <Bar dataKey="urgent" name="High Priority" fill="#E11D48" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Category Share Donut */}
        <div className="lg:col-span-5 p-5 rounded-2xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 shadow-xs">
          <h3 className="text-xs font-bold text-slate-800 dark:text-slate-200 uppercase tracking-wider mb-4">
            Inbox Category Share
          </h3>
          <div className="h-64 flex items-center justify-center">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  innerRadius={55}
                  outerRadius={80}
                  paddingAngle={4}
                  dataKey="value"
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{ backgroundColor: '#1E293B', borderColor: '#334155', borderRadius: '12px', fontSize: '11px', color: '#F8FAFC' }}
                />
                <Legend wrapperStyle={{ fontSize: '11px' }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Top Senders Table */}
      <div className="rounded-2xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 p-5 shadow-xs">
        <h3 className="text-xs font-bold text-slate-800 dark:text-slate-200 uppercase tracking-wider mb-4 flex items-center space-x-2">
          <Users className="w-4 h-4 text-purple-600 dark:text-purple-400" />
          <span>Top Senders & Urgency Heatmap</span>
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-200 dark:border-slate-800 text-slate-500 dark:text-slate-400 font-bold">
                <th className="pb-3">Sender Contact</th>
                <th className="pb-3">Email Address</th>
                <th className="pb-3">Frequency</th>
                <th className="pb-3">Urgent Ratio</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200/60 dark:divide-slate-800/50 text-slate-700 dark:text-slate-300">
              {data.top_senders.map((sender, idx) => (
                <tr key={idx} className="hover:bg-slate-100/80 dark:hover:bg-slate-800/40 transition">
                  <td className="py-3 font-bold text-slate-900 dark:text-white">{sender.name}</td>
                  <td className="py-3 text-slate-500 dark:text-slate-400 font-medium">{sender.email}</td>
                  <td className="py-3 font-medium">{sender.count} messages</td>
                  <td className="py-3">
                    <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-indigo-100 dark:bg-indigo-500/20 text-indigo-800 dark:text-indigo-300 border border-indigo-200 dark:border-indigo-500/30">
                      {sender.urgent_ratio}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
