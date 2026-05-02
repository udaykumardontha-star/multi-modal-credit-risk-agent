import React from 'react';
import { Download, ChevronLeft, AlertTriangle } from 'lucide-react';

export const RiskDashboard = ({ result, onReset }: { result: any, onReset: () => void }) => {
  const { risk_score, computed_ratios, risk_flags, qualitative_commentary, memo_url, extracted_statements } = result;

  const decisionColor = {
    'APPROVE': 'bg-risk-approve text-white',
    'REFER': 'bg-risk-refer text-white',
    'REJECT': 'bg-risk-reject text-white'
  }[risk_score.decision as 'APPROVE' | 'REFER' | 'REJECT'];

  const getRatioStatus = (value: number | null, good: number, bad: number, higherIsBetter = true) => {
    if (value === null) return 'text-gray-500';
    if (higherIsBetter) {
      if (value >= good) return 'text-green-600';
      if (value <= bad) return 'text-red-600';
      return 'text-yellow-600';
    } else {
      if (value <= good) return 'text-green-600';
      if (value >= bad) return 'text-red-600';
      return 'text-yellow-600';
    }
  };

  const downloadMemo = () => {
    // API URL is relative, need absolute if not proxied, but Vite proxy handles this in dev.
    // Assuming backend is at http://localhost:8000
    const baseUrl = import.meta.env.VITE_API_URL ? import.meta.env.VITE_API_URL.replace('/api/v1', '') : 'http://localhost:8000';
    window.open(`${baseUrl}${memo_url}`, '_blank');
  };

  return (
    <div className="max-w-6xl mx-auto mt-8 mb-20 px-4">
      <button onClick={onReset} className="flex items-center text-blue-600 hover:text-blue-800 mb-6 font-medium">
        <ChevronLeft className="w-5 h-5 mr-1" /> New Analysis
      </button>

      {/* Header / Score Section */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="col-span-1 md:col-span-2 bg-white rounded-2xl shadow-sm border border-gray-200 p-8 flex flex-col justify-center">
          <div className="flex justify-between items-start">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                {extracted_statements?.[0]?.company_name || 'Unknown Company'}
              </h1>
              <p className="text-gray-500 text-lg">Period: {extracted_statements?.[0]?.period || 'N/A'}</p>
            </div>
            <div className={`px-6 py-2 rounded-full font-bold text-xl tracking-wide ${decisionColor}`}>
              {risk_score.decision}
            </div>
          </div>
          <p className="mt-6 text-gray-700 bg-gray-50 p-4 rounded-lg border border-gray-100">
            <strong>Rationale:</strong> {risk_score.rationale}
          </p>
        </div>

        <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-8 flex flex-col items-center justify-center text-center">
          <h3 className="text-gray-500 font-medium mb-2">Composite Score</h3>
          <div className="text-6xl font-bold text-gray-900 mb-2">
            {risk_score.composite_score.toFixed(0)}
            <span className="text-2xl text-gray-400">/100</span>
          </div>
          <p className="text-sm text-gray-500 mt-2">Data Confidence: {risk_score.confidence.toFixed(0)}%</p>
        </div>
      </div>

      {/* Ratios Grid */}
      <h2 className="text-2xl font-bold text-gray-900 mb-4">Key Financial Ratios</h2>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <RatioCard name="Current Ratio" value={computed_ratios.current_ratio} status={getRatioStatus(computed_ratios.current_ratio, 1.5, 1.0)} />
        <RatioCard name="Debt to Equity" value={computed_ratios.debt_to_equity} status={getRatioStatus(computed_ratios.debt_to_equity, 1.0, 3.0, false)} />
        <RatioCard name="Interest Coverage" value={computed_ratios.interest_coverage} status={getRatioStatus(computed_ratios.interest_coverage, 3.0, 1.0)} />
        <RatioCard name="Net Margin" value={computed_ratios.net_margin} isPercent status={getRatioStatus(computed_ratios.net_margin, 0.1, 0.02)} />
      </div>

      {/* Altman Z-Score & Flags */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-bold text-gray-900 mb-4">Altman Z-Score</h3>
          <div className="flex items-center">
            <div className={`text-4xl font-bold mr-4 ${getRatioStatus(computed_ratios.altman_z_score, 2.99, 1.81)}`}>
              {computed_ratios.altman_z_score?.toFixed(2) ?? 'N/A'}
            </div>
            <div className="text-sm text-gray-600">
              <p>Safe Zone: &gt; 2.99</p>
              <p>Grey Zone: 1.81 - 2.99</p>
              <p>Distress Zone: &lt; 1.81</p>
            </div>
          </div>
        </div>

        <div className="bg-red-50 rounded-xl border border-red-200 p-6">
          <div className="flex items-center gap-2 mb-4">
            <AlertTriangle className="w-6 h-6 text-red-600" />
            <h3 className="text-lg font-bold text-red-900">Risk Flags</h3>
          </div>
          {risk_flags.length > 0 ? (
            <ul className="list-disc pl-5 space-y-2 text-red-800">
              {risk_flags.map((flag: string, idx: number) => (
                <li key={idx}>{flag}</li>
              ))}
            </ul>
          ) : (
            <p className="text-green-700 font-medium">No major risk flags identified.</p>
          )}
        </div>
      </div>

      {/* Commentary */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8 mb-8">
        <h3 className="text-xl font-bold text-gray-900 mb-4">Analyst Commentary</h3>
        <div className="prose max-w-none text-gray-700 whitespace-pre-line">
          {qualitative_commentary}
        </div>
      </div>

      {/* Actions */}
      <div className="flex justify-center">
        <button 
          onClick={downloadMemo}
          className="flex items-center gap-2 px-8 py-4 bg-blue-600 text-white rounded-xl hover:bg-blue-700 font-bold text-lg shadow-md transition-transform hover:-translate-y-0.5"
        >
          <Download className="w-6 h-6" /> Download Full Credit Memo (PDF)
        </button>
      </div>

    </div>
  );
};

const RatioCard = ({ name, value, status, isPercent = false }: { name: string, value: number | null, status: string, isPercent?: boolean }) => (
  <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
    <h4 className="text-sm font-medium text-gray-500 mb-1">{name}</h4>
    <div className={`text-2xl font-bold ${status}`}>
      {value !== null ? (isPercent ? `${(value * 100).toFixed(1)}%` : value.toFixed(2)) : 'N/A'}
    </div>
  </div>
);
