# Search Console sync

`search-console-reusable.yml` resubmits a site's sitemap to Google Search
Console and writes a per-URL index report to the run summary. Site repos call it
through the thin caller in `distribution/workflows/search-console.yml`.

## One-time setup

1. In Google Cloud, enable the
   [Search Console API](https://console.cloud.google.com/apis/library/searchconsole.googleapis.com)
   and create a service account with a JSON key.
2. In [Search Console](https://search.google.com/search-console), add the
   service account's email as an **Owner** of each property. The
   `sc-domain:elixpo.com` domain property covers every `*.elixpo.com` site;
   other domains such as `lixrl.com` need their own property.
3. In the organization's Actions settings, add:
   - secret `GOOGLE_SERVICE_ACCOUNT_JSON`: the full key JSON;
   - variable `SEARCH_CONSOLE_SITE`: `sc-domain:elixpo.com`.

Without the secret the run logs a skip message and exits successfully.

## Adding a site

Copy `distribution/workflows/search-console.yml` into the site repository's
`.github/workflows/`, set `site-url`, and give the cron a minute no other site
uses. Pass `property` only when the site is not on `SEARCH_CONSOLE_SITE`.

## Inputs

| Input | Default | Purpose |
|---|---|---|
| `site-url` | required | Public origin, e.g. `https://me.elixpo.com` |
| `property` | `vars.SEARCH_CONSOLE_SITE`, then `<site-url>/` | Search Console property id |
| `sitemap-url` | `<site-url>/sitemap.xml` | Sitemap location |
| `inspect-limit` | `100` | URLs inspected per run; `0` submits the sitemap only |

## Quota

URL Inspection allows about 2,000 calls per day per property, and every site on
`sc-domain:elixpo.com` shares that budget. Keep each site's `inspect-limit`
times its runs per day well under it. Sitemap submission does not consume the
inspection quota.

`vars.ELIXPO_SEARCH_CONSOLE_REF` pins the script revision; it defaults to `main`.
