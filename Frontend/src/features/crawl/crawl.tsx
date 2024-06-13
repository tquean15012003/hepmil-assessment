import {
  Box,
  Image,
  Text,
  Link,
  Heading,
  SimpleGrid,
  Button,
  Spinner,
} from '@chakra-ui/react';

import useCrawl from './hooks/useCrwal';
import useReport from './hooks/useReport';

import { formatDate } from './utils';

export const CrawlPage: React.FC = () => {
  const { data: redditPosts, isLoading: isCrawling } = useCrawl();
  const { mutate: generateReport, isPending: isGeneratingReport } = useReport();

  if (isCrawling || !redditPosts) {
    return 'Loading';
  }
  return (
    <Box p={5}>
      <Button
        colorScheme="purple"
        onClick={generateReport}
        disabled={isGeneratingReport}
      >
        Generate report
        {isGeneratingReport && <Spinner colorScheme="purple" />}
      </Button>
      <SimpleGrid columns={3} alignItems="center" justifyItems="center">
        {redditPosts.map((post) => (
          <Box
            key={post.id}
            borderWidth="1px"
            borderRadius="lg"
            overflow="hidden"
            p={5}
            maxW="md"
            boxShadow="lg"
          >
            <Heading size="md" mb={3}>
              {post.title}
            </Heading>
            <Image height="400px" src={post.link} alt={post.title} mb={3} />
            {post.body.length !== 0 && <Text mb={3}>Body: {post.body}</Text>}
            <Text mb={3}>Comments: {post.no_comments}</Text>
            <Text mb={3}>Upvotes: {post.upvotes}</Text>
            <Text mb={3}>Created at: {formatDate(post.created_at)}</Text>
            <Link href={post.link} color="teal.500" isExternal>
              View Image
            </Link>
          </Box>
        ))}
      </SimpleGrid>
    </Box>
  );
};
