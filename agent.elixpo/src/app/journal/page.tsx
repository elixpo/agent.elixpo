import { LiveDashboard } from "@/components/live-dashboard";
import { pageMetadata } from "@/lib/site-metadata";

export const metadata = pageMetadata(
  "Agent Journal",
  "Read Elixpoo's public operational journal of repository changes, workflow artifacts, and project activity.",
  "/journal",
);

export default function JournalPage() {
  return <LiveDashboard view="journal" />;
}
