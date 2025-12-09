import React, { useEffect, useState } from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, BarChart, Bar, Legend } from 'recharts';
import { Activity, Globe, Shield } from 'lucide-react';

interface Stats {
    total_attacks: number;
    country_stats: Record<string, number>;
    type_stats: Record<string, number>;
    attacks_over_time: { time: string; count: number }[];
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8', '#ef4444'];

const AnalyticsDashboard: React.FC = () => {
    const [stats, setStats] = useState<Stats | null>(null);

    useEffect(() => {
        fetch('/api/stats')
            .then(res => res.json())
            .then(data => setStats(data))
            .catch(err => console.error("Failed to fetch stats", err));
    }, []);

    if (!stats) return (
        <div className="w-full h-64 flex items-center justify-center text-white/50 font-mono animate-pulse">
            INITIALIZING ANALYTICS MODULE...
        </div>
    );

    const typeData = Object.entries(stats.type_stats).map(([name, value]) => ({ name, value }));
    const countryData = Object.entries(stats.country_stats)
        .map(([name, value]) => ({ name, value }))
        .sort((a, b) => b.value - a.value)
        .slice(0, 5);

    return (
        <div className="w-full text-white">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div className="bg-white/5 p-6 rounded-xl border border-white/10 backdrop-blur-sm">
                    <div className="flex items-center gap-4 mb-2">
                        <Shield className="text-[#4fb7b3]" />
                        <h3 className="text-lg font-bold uppercase tracking-widest text-gray-400 text-xs">Total Intrusions</h3>
                    </div>
                    <p className="text-4xl font-mono font-bold text-white">{stats.total_attacks.toLocaleString()}</p>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">

                {/* Attacks Over Time */}
                <div className="bg-black/40 p-6 rounded-xl border border-white/10 backdrop-blur-sm">
                    <h3 className="text-xl font-heading font-bold mb-6 flex items-center gap-2">
                        <Activity className="text-red-500" /> Attack Volume (24h)
                    </h3>
                    <div className="h-[300px] w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <AreaChart data={stats.attacks_over_time}>
                                <defs>
                                    <linearGradient id="colorCount" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="#ef4444" stopOpacity={0.8} />
                                        <stop offset="95%" stopColor="#ef4444" stopOpacity={0} />
                                    </linearGradient>
                                </defs>
                                <CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
                                <XAxis dataKey="time" stroke="#666" tick={{ fill: '#666', fontSize: 12 }} />
                                <YAxis stroke="#666" tick={{ fill: '#666', fontSize: 12 }} />
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#000', border: '1px solid #333', borderRadius: '8px' }}
                                    itemStyle={{ color: '#fff', fontFamily: 'monospace' }}
                                />
                                <Area type="monotone" dataKey="count" stroke="#ef4444" fillOpacity={1} fill="url(#colorCount)" />
                            </AreaChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* Attack Types */}
                <div className="bg-black/40 p-6 rounded-xl border border-white/10 backdrop-blur-sm">
                    <h3 className="text-xl font-heading font-bold mb-6 flex items-center gap-2">
                        <Shield className="text-orange-500" /> Attack Vectors
                    </h3>
                    <div className="h-[300px] w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <PieChart>
                                <Pie
                                    data={typeData}
                                    cx="50%"
                                    cy="50%"
                                    innerRadius={60}
                                    outerRadius={100}
                                    fill="#8884d8"
                                    paddingAngle={5}
                                    dataKey="value"
                                >
                                    {typeData.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                    ))}
                                </Pie>
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#000', border: '1px solid #333', borderRadius: '8px' }}
                                    itemStyle={{ color: '#fff', fontFamily: 'monospace' }}
                                />
                                <Legend wrapperStyle={{ fontSize: '12px', fontFamily: 'monospace' }} />
                            </PieChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* Top Countries */}
                <div className="bg-black/40 p-6 rounded-xl border border-white/10 lg:col-span-2 backdrop-blur-sm">
                    <h3 className="text-xl font-heading font-bold mb-6 flex items-center gap-2">
                        <Globe className="text-blue-500" /> Top Attacking Countries
                    </h3>
                    <div className="h-[300px] w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={countryData} layout="vertical" margin={{ left: 20 }}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#333" horizontal={false} />
                                <XAxis type="number" stroke="#666" tick={{ fill: '#666', fontSize: 12 }} />
                                <YAxis dataKey="name" type="category" stroke="#fff" width={120} tick={{ fill: '#fff', fontSize: 12, fontFamily: 'monospace' }} />
                                <Tooltip
                                    cursor={{ fill: 'transparent' }}
                                    contentStyle={{ backgroundColor: '#000', border: '1px solid #333', borderRadius: '8px' }}
                                    itemStyle={{ color: '#fff', fontFamily: 'monospace' }}
                                />
                                <Bar dataKey="value" fill="#4fb7b3" radius={[0, 4, 4, 0]} barSize={20} />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>

            </div>
        </div>
    );
};

export default AnalyticsDashboard;
