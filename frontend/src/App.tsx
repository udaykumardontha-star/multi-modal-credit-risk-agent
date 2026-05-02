import React, { useState } from 'react';
import { UploadZone } from './components/UploadZone';
import { JobStatus } from './components/JobStatus';
import { ShieldCheck } from 'lucide-react';

function App() {
  const [jobId, setJobId] = useState<string | null>(null);

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <header className="bg-white border-b border-gray-200 py-4 px-6 sticky top-0 z-10 shadow-sm">
        <div className="max-w-6xl mx-auto flex items-center gap-3">
          <ShieldCheck className="w-8 h-8 text-blue-600" />
          <h1 className="text-xl font-bold text-gray-900 tracking-tight">Credit Risk Analyst Agent</h1>
        </div>
      </header>

      <main className="flex-1 w-full max-w-6xl mx-auto p-6">
        {!jobId ? (
          <div className="py-12">
            <div className="text-center max-w-2xl mx-auto mb-10">
              <h2 className="text-3xl font-bold text-gray-900 mb-4">Automated Financial Underwriting</h2>
              <p className="text-lg text-gray-600">
                Upload financial statements (PDFs, scans, or CSVs) to instantly extract data, compute key ratios, and generate a comprehensive credit memo with a decision recommendation.
              </p>
            </div>
            <UploadZone onUploadSuccess={setJobId} />
          </div>
        ) : (
          <JobStatus jobId={jobId} onReset={() => setJobId(null)} />
        )}
      </main>
      
      <footer className="py-6 text-center text-sm text-gray-500">
        &copy; {new Date().getFullYear()} AI Credit Risk Agent. For demonstration purposes.
      </footer>
    </div>
  );
}

export default App;
