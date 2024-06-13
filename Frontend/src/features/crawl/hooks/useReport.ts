import { axiosClient } from '@/lib/axios';
import { DefaultMutationOptions } from '@/lib/react-query';

import { useToast } from '@chakra-ui/react';
import { useMutation } from '@tanstack/react-query';

const useReport = ({ onSettled, ...options }: DefaultMutationOptions = {}) => {
  const toast = useToast();

  return useMutation({
    mutationKey: ['generateReport'],
    mutationFn: async () => {
      const { data } = await axiosClient.get<string>('/report');
      return data;
    },
    onSettled: async (...params) => {
      const data = params[0];
      toast({
        title: 'Report',
        description: data,
        status: 'success',
        isClosable: true,
      });
      if (onSettled) {
        onSettled(...params);
      }
    },
    ...options,
  });
};

export default useReport;
