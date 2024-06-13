import { Box, Flex, HStack, Text } from '@chakra-ui/react';
import { Link, Outlet, createRootRoute } from '@tanstack/react-router';
import { TanStackRouterDevtools } from '@tanstack/router-devtools';

export const Route = createRootRoute({
  component: () => (
    <Box maxHeight="100dvh">
      <Box as="nav">
        <Flex justify="space-between" align="center" maxW="1800px" px={8}>
          <Link to="/">
            <Text fontWeight="bold">HEPMIL Singapore Assessment</Text>
          </Link>
          <HStack gap={8} py={4}>
            <Link to="/">Home</Link>
          </HStack>
        </Flex>
      </Box>
      <Outlet />
      <TanStackRouterDevtools />
    </Box>
  ),
});
