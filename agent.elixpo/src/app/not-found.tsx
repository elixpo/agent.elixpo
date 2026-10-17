import Link from "next/link";
import { Activity, ArrowLeft, BookOpen, ExternalLink, GitBranch, Grid3X3, SearchX } from "lucide-react";

const destinations = [
  { href: "/", label: "Overview", description: "Return to live project operations", icon: Activity },
  { href: "/floors", label: "Capabilities", description: "Browse bounded capability domains", icon: Grid3X3 },
  { href: "/docs", label: "Elixpoo docs", description: "Read the v1 project-management contract", icon: BookOpen },
];

export default function NotFound() {
  return (
    <main className="not-found-page">
      <section className="not-found-card">
        <div className="not-found-visual" aria-hidden="true">
          <span className="not-found-code">404</span>
          <div className="not-found-orbit orbit-one" />
          <div className="not-found-orbit orbit-two" />
          <div className="not-found-node"><SearchX size={29} /></div>
          <i className="not-found-packet packet-one" />
          <i className="not-found-packet packet-two" />
        </div>

        <div className="not-found-copy">
          <span className="not-found-eyebrow"><GitBranch size={14} /> Route not registered</span>
          <h1>This route does not exist.</h1>
          <p>No capability claims this address. Pick a registered destination or return to the live operations overview.</p>
          <Link className="not-found-primary" href="/"><ArrowLeft size={15} /> Back to overview</Link>
        </div>
      </section>

      <section className="not-found-destinations" aria-label="Available destinations">
        {destinations.map(({ href, label, description, icon: Icon }) => (
          <Link href={href} key={href}>
            <span><Icon size={18} /></span>
            <strong>{label}</strong>
            <small>{description}</small>
          </Link>
        ))}
      </section>

      <a className="not-found-source" href="https://github.com/elixpo/agent.elixpo" target="_blank" rel="noreferrer">
        Check the source repository <ExternalLink size={13} />
      </a>
    </main>
  );
}
