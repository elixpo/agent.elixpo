import { BookOpen, ExternalLink, GitPullRequest, MessageSquare, ShieldCheck, Tags } from "lucide-react";
import { pageMetadata } from "@/lib/site-metadata";

export const metadata = pageMetadata(
  "Elixpoo v1 documentation",
  "The capabilities, authorization boundary, deployment model, and read-only rollout audit for Elixpo's GitHub project-management agent.",
  "/docs",
);

const capabilities = [
  [Tags, "Automatic triage", "Classifies issues and pull requests, applies centrally allowed labels, and creates one Project V2 record."],
  [MessageSquare, "Exact mentions", "Answers @elixpoo or performs one typed metadata action after deterministic permission checks."],
  [GitPullRequest, "PR review", "Uses API-grounded diffs and repository guidance to leave deduplicated COMMENT-only reviews."],
  [BookOpen, "Merge memory", "Stores one compact, schema-versioned record in the approved Gist after a pull request merges."],
] as const;

export default function DocsPage() {
  return (
    <main className="docs-shell">
      <section className="docs-main">
        <header className="docs-hero">
          <span className="docs-kicker">Elixpoo v1 · project management</span>
          <h1>One central runtime.<br /><em>Bounded GitHub actions.</em></h1>
          <p>Elixpoo keeps project administration consistent across participating Elixpo repositories. It does not implement product code, create solution commits, or open solving pull requests.</p>
          <div className="docs-hero-actions">
            <a href="https://github.com/elixpo/agent.elixpo/blob/main/docs/elixpoo-v1.md" target="_blank" rel="noreferrer">Read the source contract <ExternalLink size={14} /></a>
            <a href="https://github.com/elixpo/agent.elixpo/tree/main/distribution/workflows" target="_blank" rel="noreferrer">Caller templates <ExternalLink size={14} /></a>
          </div>
        </header>

        <section className="docs-section">
          <div className="docs-section-heading"><small>Capabilities</small><h2>What v1 may do</h2></div>
          <div className="docs-api-grid">
            {capabilities.map(([Icon, title, copy]) => <article key={title}><Icon size={22} /><h3>{title}</h3><p>{copy}</p></article>)}
          </div>
        </section>

        <section className="docs-section">
          <div className="docs-section-heading"><small>Safety boundary</small><h2>Models propose; policy decides</h2></div>
          <div className="docs-note"><ShieldCheck size={20} /><p>Repository content is untrusted evidence. Typed schemas, actor permissions, GitHub assignability, label and Project-field allowlists, idempotency markers, Gist revision checks, and the public safety gate are deterministic.</p></div>
          <p className="docs-prose">Anyone may ask questions, request summaries, propose rewrites, or request a review. Authors may update their own title or body. Labels, Project fields, state changes, and other-user assignments require repository triage permission or stronger. Self-assignment also requires GitHub assignability.</p>
        </section>

        <section className="docs-section">
          <div className="docs-section-heading"><small>Rollout</small><h2>Thin callers, pinned runtime</h2></div>
          <p className="docs-prose">Participating repositories install only the event callers from <code>distribution/workflows</code>. Each caller pins a reusable workflow in <code>elixpo/agent.elixpo</code> at <code>v1</code>. The canonical Discussions responder remains centralized and is not copied to every repository.</p>
          <pre className="code-block"><code>python -m agents.rollout_prs{`\n`}python -m agents.rollout_prs --repo lixrl.com --apply{`\n`}python -m agents.rollout_audit</code></pre>
          <p className="docs-prose">Rollout is dry-run by default. Apply mode opens one reviewable, idempotent pull request in each eligible repository; it never merges that PR. The separate audit reports missing, stale, excluded, and unexpected callers.</p>
        </section>

        <section className="docs-section">
          <div className="docs-section-heading"><small>History</small><h2>The autonomous contributor is archived</h2></div>
          <p className="docs-prose">The former Scout → Triage → Pick → Vet → Solve → Submit direction is preserved for research and implementation history, but it is not part of the supported v1 runtime.</p>
          <div className="docs-hero-actions">
            <a href="https://github.com/elixpo/agent.elixpo/tree/legacy-autonomous-contributor-v1" target="_blank" rel="noreferrer">Open the frozen legacy snapshot <ExternalLink size={14} /></a>
          </div>
        </section>
      </section>
    </main>
  );
}
