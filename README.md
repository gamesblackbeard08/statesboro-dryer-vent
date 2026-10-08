# Digital Real Estate Property #1 — Statesboro Dryer Vent

Static SEO-first site with a simple Python build step.

## Editing workflow
1. Open `content/site.json` in GitHub to change the working brand, final domain, phone, email, or site-wide details.
2. Open a file in `content/pages/` to edit page titles, descriptions, headings, copy, FAQs, or related links.
3. Commit the change in GitHub.
4. Cloudflare Pages automatically runs the build and publishes the update.

## Cloudflare Pages settings
- Framework preset: None
- Build command: `python build.py`
- Build output directory: `dist`
- Root directory: `/`

## Important prelaunch safety
The starter config has `production_ready: false`.
That does two things:
- adds `noindex,nofollow` to every page
- blocks crawling in `robots.txt`

Use the temporary `*.pages.dev` URL for QA without intentionally launching SEO.

Before serious indexing:
1. Buy/connect the final domain.
2. Replace `https://YOUR-FINAL-DOMAIN.com` in `content/site.json`.
3. Add verified contact information if the site will accept inquiries.
4. Review every claim and page.
5. Set `production_ready` to `true`.
6. Commit.
7. Verify the custom domain in Google Search Console.
8. Submit `/sitemap.xml`.

## Images
This build intentionally ships without stock photos so no unverified asset is accidentally published. Add only legally reusable images whose license/source has been checked. Suggested free-image sources identified during research:
- Unsplash residential laundry photo: https://unsplash.com/photos/a-laundry-room-with-a-washer-and-dryer-Qw1I3E6iAso
- Unsplash laundromat photo: https://unsplash.com/photos/row-of-washing-machines-in-a-laundromat-jKlrXl_Ur7s

Store downloaded, optimized assets in `assets/images/` and keep a source/license log.

## Notes
- No fake address, technicians, reviews, years in business, licenses, or service history are included.
- The site is written as an independent local information resource until a verified operator is attached.
- Canonical URLs come from `site_url` in `content/site.json`.
