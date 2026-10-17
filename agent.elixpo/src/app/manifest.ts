import type { MetadataRoute } from "next";
import { SITE_DESCRIPTION, SITE_NAME } from "@/lib/site-metadata";


export const dynamic = "force-static";
export default function manifest(): MetadataRoute.Manifest {
  return {
    name: `${SITE_NAME} · GitHub Project Management Agent`,
    short_name: SITE_NAME,
    description: SITE_DESCRIPTION,
    start_url: "/",
    display: "standalone",
    background_color: "#f4f5f1",
    theme_color: "#0b0d0c",
    icons: [
      {
        src: "/logo.png",
        sizes: "1024x1024",
        type: "image/png",
      },
    ],
  };
}
