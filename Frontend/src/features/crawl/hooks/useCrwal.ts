import { TRedditPost } from '../types';

import { axiosClient } from '@/lib/axios';
import { useQuery } from '@tanstack/react-query';

const useCrawl = (id?: string) => {
  return useQuery({
    queryKey: ['crawl', id],
    queryFn: async () => {
      const { data } = await axiosClient.get<TRedditPost[]>(`/crawl/20/day`);
      return data;
    },
  });
};

export default useCrawl;
