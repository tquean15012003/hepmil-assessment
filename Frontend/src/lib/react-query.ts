import {
  QueryClient,
  DefaultOptions,
  UseMutationOptions,
} from '@tanstack/react-query';
import { AxiosError } from 'axios';

const queryConfig: DefaultOptions = {
  queries: {
    refetchOnMount: false,
    refetchOnWindowFocus: false,
    retry: false,
  },
};

export type DefaultMutationOptions<
  TMutationFnData = unknown,
  TMutationVariables = unknown,
  options extends keyof UseMutationOptions | undefined = undefined,
> = Pick<
  UseMutationOptions<
    TMutationFnData,
    AxiosError | Error,
    TMutationVariables,
    unknown
  >,
  | 'onSuccess'
  | 'onSettled'
  | 'onError'
  | (options extends keyof UseMutationOptions ? options : never)
>;

export const queryClient = new QueryClient({ defaultOptions: queryConfig });
