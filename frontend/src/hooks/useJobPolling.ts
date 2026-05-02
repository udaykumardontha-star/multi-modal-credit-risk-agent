import useSWR from 'swr';
import { fetchJobStatus } from '../api/client';

export const useJobPolling = (jobId: string | null) => {
  const { data, error, isLoading } = useSWR(
    jobId ? jobId : null,
    fetchJobStatus,
    {
      refreshInterval: (data) => {
        if (data?.status === 'COMPLETE' || data?.status === 'FAILED') {
          return 0; // Stop polling
        }
        return 2000;
      },
      shouldRetryOnError: false,
    }
  );

  return {
    status: data?.status,
    result: data,
    currentNode: data?.current_node,
    error: error || (data?.status === 'FAILED' ? data.detail : null),
    isLoading
  };
};
