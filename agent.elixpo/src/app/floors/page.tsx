import { LiveDashboard } from "@/components/live-dashboard";
import { pageMetadata } from "@/lib/site-metadata";

export const metadata = pageMetadata(
  "Agent Floor Directory",
  "Explore Elixpoo's repository activity, project-management workflow floor, and canonical community Discussions floor.",
  "/floors",
);

export default function FloorsPage() {
  return <LiveDashboard view="floors" />;
}
