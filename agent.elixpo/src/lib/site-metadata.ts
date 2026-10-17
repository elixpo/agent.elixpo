import type { Metadata } from "next";

export const SITE_URL = "https://agent.elixpo.com";
export const SITE_NAME = "Elixpoo";
export const SITE_TITLE = "Elixpoo · Live Project Operations";
export const SITE_DESCRIPTION =
  "Follow Elixpo's public GitHub project-management agent: live triage, mentions, reviews, Project records, discussions, merge history, and safety activity.";

export const SOCIAL_IMAGE = {
  url: "/default.png",
  width: 1280,
  height: 720,
  type: "image/png",
  alt: "Elixpoo live project operations dashboard",
};

export function absoluteUrl(path = "/") {
  return new URL(path, SITE_URL).toString();
}

export function pageMetadata(title: string, description: string, path: string): Metadata {
  const socialTitle = `${title} | ${SITE_NAME}`;

  return {
    title,
    description,
    alternates: { canonical: path },
    openGraph: {
      title: socialTitle,
      description,
      url: path,
      siteName: SITE_NAME,
      locale: "en_US",
      type: "website",
      images: [SOCIAL_IMAGE],
    },
    twitter: {
      card: "summary_large_image",
      title: socialTitle,
      description,
      images: [SOCIAL_IMAGE.url],
    },
  };
}
