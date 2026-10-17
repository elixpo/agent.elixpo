import { LiveDashboard } from "@/components/live-dashboard";
import { pageMetadata } from "@/lib/site-metadata";

export const metadata = pageMetadata(
  "Capability Map",
  "Explore Elixpoo's repository signals, bounded project-management runtime, and canonical community protocol.",
  "/floors",
);

export default function FloorsPage() {
  return <LiveDashboard view="floors" />;
}
