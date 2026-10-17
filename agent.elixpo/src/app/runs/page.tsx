import { LiveDashboard } from "@/components/live-dashboard";
import { pageMetadata } from "@/lib/site-metadata";

export const metadata = pageMetadata(
  "Workflow Runs",
  "Track recent Elixpoo GitHub workflow runs, statuses, actors, branches, and project-management activity.",
  "/runs",
);

export default function RunsPage() {
  return <LiveDashboard view="runs" />;
}
