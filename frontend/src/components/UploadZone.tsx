import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { uploadFiles } from '../api/client';
import { Upload, X, FileText, FileImage, FileSpreadsheet, AlertCircle } from 'lucide-react';

export const UploadZone = ({ onUploadSuccess }: { onUploadSuccess: (jobId: string) => void }) => {
  const [files, setFiles] = useState<File[]>([]);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    setError(null);
    if (files.length + acceptedFiles.length > 5) {
      setError('Maximum 5 files allowed.');
      return;
    }
    setFiles(prev => [...prev, ...acceptedFiles]);
  }, [files]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ 
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'image/jpeg': ['.jpg', '.jpeg'],
      'image/png': ['.png'],
      'image/webp': ['.webp'],
      'text/csv': ['.csv'],
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx']
    },
    maxSize: 20 * 1024 * 1024 // 20MB
  });

  const removeFile = (index: number) => {
    setFiles(files.filter((_, i) => i !== index));
  };

  const handleSubmit = async () => {
    if (files.length === 0) return;
    setUploading(true);
    setError(null);
    try {
      const data = await uploadFiles(files);
      onUploadSuccess(data.job_id);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message);
    } finally {
      setUploading(false);
    }
  };

  const getFileIcon = (type: string) => {
    if (type.includes('pdf')) return <FileText className="w-6 h-6 text-red-500" />;
    if (type.includes('image')) return <FileImage className="w-6 h-6 text-blue-500" />;
    return <FileSpreadsheet className="w-6 h-6 text-green-500" />;
  };

  return (
    <div className="w-full max-w-2xl mx-auto mt-10">
      <div 
        {...getRootProps()} 
        className={`border-2 border-dashed rounded-xl p-10 text-center cursor-pointer transition-colors
          ${isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-gray-400 bg-white'}`}
      >
        <input {...getInputProps()} />
        <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
        <p className="text-lg font-medium text-gray-700">Drag & drop financial documents here</p>
        <p className="text-sm text-gray-500 mt-2">Supports PDF, JPG, PNG, WEBP, CSV, XLSX (Max 20MB/file, up to 5 files)</p>
      </div>

      {error && (
        <div className="mt-4 p-4 bg-red-50 text-red-700 rounded-lg flex items-center gap-2">
          <AlertCircle className="w-5 h-5" />
          {error}
        </div>
      )}

      {files.length > 0 && (
        <div className="mt-6">
          <h3 className="font-semibold text-gray-700 mb-3">Selected Files ({files.length}/5)</h3>
          <ul className="space-y-2">
            {files.map((file, idx) => (
              <li key={idx} className="flex items-center justify-between p-3 bg-white border border-gray-200 rounded-lg shadow-sm">
                <div className="flex items-center gap-3">
                  {getFileIcon(file.type)}
                  <div>
                    <p className="text-sm font-medium text-gray-700 truncate max-w-xs">{file.name}</p>
                    <p className="text-xs text-gray-500">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                  </div>
                </div>
                <button 
                  onClick={() => removeFile(idx)}
                  className="p-1 text-gray-400 hover:text-red-500 transition-colors"
                >
                  <X className="w-5 h-5" />
                </button>
              </li>
            ))}
          </ul>
          
          <button
            onClick={handleSubmit}
            disabled={uploading}
            className={`mt-6 w-full py-3 px-4 rounded-lg text-white font-medium shadow-sm transition-colors
              ${uploading ? 'bg-blue-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'}`}
          >
            {uploading ? 'Uploading & Starting Analysis...' : 'Analyze Documents'}
          </button>
        </div>
      )}
    </div>
  );
};
