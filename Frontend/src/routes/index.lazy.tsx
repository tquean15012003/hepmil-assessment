import { CrawlPage } from '@/features/crawl/crawl';
import { createLazyFileRoute } from '@tanstack/react-router';

export const Route = createLazyFileRoute('/')({
  component: CrawlPage,
});
