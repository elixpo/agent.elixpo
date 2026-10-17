import { LiveDashboard } from "@/components/live-dashboard";
import { pageMetadata } from "@/lib/site-metadata";

export const metadata = pageMetadata(
  "Repository Work",
  "Follow issues and pull requests represented in Elixpoo's GitHub project-management workflows.",
  "/work",
);

export default function WorkPage() {
  return <LiveDashboard view="work" />;
}
