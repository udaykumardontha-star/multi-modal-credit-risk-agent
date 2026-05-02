import React from 'react';
import { useJobPolling } from '../hooks/useJobPolling';
import { RiskDashboard } from './RiskDashboard';
import { AlertCircle, Loader2 } from 'lucide-react';

export const JobStatus = ({ jobId, onReset }: { jobId: string, onReset: () => void }) => {
  const { status, result, currentNode, error } = useJobPolling(jobId);

  if (error) {
    return (
      <div className="max-w-2xl mx-auto mt-10 p-6 bg-red-50 border border-red-200 rounded-xl text-center">
        <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-4" />
        <h2 className="text-xl font-semibold text-red-700 mb-2">Analysis Failed</h2>
        <p className="text-red-600 mb-6">{error}</p>
        <button 
          onClick={onReset}
          className="px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 font-medium"
        >
          Try Again
        </button>
      </div>
    );
  }

  if (status === 'COMPLETE' && result) {
    return <RiskDashboard result={result} onReset={onReset} />;
  }

  return (
    <div className="max-w-xl mx-auto mt-20 text-center">
      <Loader2 className="w-16 h-16 text-blue-600 animate-spin mx-auto mb-6" />
      <h2 className="text-2xl font-semibold text-gray-800 mb-2">Analyzing Documents</h2>
      <p className="text-gray-500">Please wait while the AI agent processes the financial data...</p>
      
      <div className="mt-8">
        <div className="flex justify-between text-sm font-medium text-gray-600 mb-2">
          <span>Current Step:</span>
          <span className="capitalize text-blue-600">{currentNode?.replace(/_/g, ' ') || 'Initializing'}</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2.5">
          <div className="bg-blue-600 h-2.5 rounded-full w-full animate-pulse"></div>
        </div>
      </div>
    </div>
  );
};
