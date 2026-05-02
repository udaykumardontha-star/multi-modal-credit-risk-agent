import React from 'react';

export const MemoViewer = ({ memoUrl }: { memoUrl: string }) => {
  const baseUrl = import.meta.env.VITE_API_URL ? import.meta.env.VITE_API_URL.replace('/api/v1', '') : 'http://localhost:8000';
  const fullUrl = `${baseUrl}${memoUrl}`;
  
  return (
    <div className="w-full h-screen max-h-[800px] bg-gray-100 rounded-xl overflow-hidden border border-gray-200 mt-8">
      <iframe 
        src={fullUrl} 
        className="w-full h-full border-none"
        title="Credit Memo PDF"
      />
    </div>
  );
};
