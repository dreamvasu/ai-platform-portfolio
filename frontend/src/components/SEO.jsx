import { Helmet } from 'react-helmet-async';

export default function SEO({
  title = 'Vasu Kapoor - AI/ML Platform Engineer',
  description = 'AI/ML Platform Engineer specializing in Kubernetes, Terraform, RAG systems, and cloud-native architecture. Portfolio showcasing production deployments on GCP and Azure.',
  keywords = 'AI, ML, Platform Engineer, Kubernetes, Terraform, GCP, Azure, RAG, DevOps, Cloud Native',
  type = 'website',
  image = '/og-image.jpg',
  url = window.location.href,
}) {
  const siteName = 'Vasu Kapoor Portfolio';
  const twitterHandle = '@vasukapoor'; // Update with actual handle

  return (
    <Helmet>
      {/* Primary Meta Tags */}
      <title>{title}</title>
      <meta name="title" content={title} />
      <meta name="description" content={description} />
      <meta name="keywords" content={keywords} />
      <meta name="author" content="Vasu Kapoor" />

      {/* Canonical URL */}
      <link rel="canonical" href={url} />

      {/* Open Graph / Facebook */}
      <meta property="og:type" content={type} />
      <meta property="og:url" content={url} />
      <meta property="og:title" content={title} />
      <meta property="og:description" content={description} />
      <meta property="og:image" content={image} />
      <meta property="og:site_name" content={siteName} />

      {/* Twitter */}
      <meta property="twitter:card" content="summary_large_image" />
      <meta property="twitter:url" content={url} />
      <meta property="twitter:title" content={title} />
      <meta property="twitter:description" content={description} />
      <meta property="twitter:image" content={image} />
      <meta property="twitter:creator" content={twitterHandle} />

      {/* Additional SEO */}
      <meta name="robots" content="index, follow" />
      <meta name="language" content="English" />
      <meta name="revisit-after" content="7 days" />

      {/* Mobile */}
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <meta name="theme-color" content="#1f2937" />
    </Helmet>
  );
}
