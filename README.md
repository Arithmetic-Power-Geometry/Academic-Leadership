# Academic Leadership Dashboard

A foundation for an academic leadership and institutional quality-assurance dashboard, including KPI reporting, IQAC and accreditation evidence workflows, research output, placements, budgets, and governance records.

## Source materials

The original source materials are a leadership-toolkit JSON export and a two-page printout of a single-file dashboard. **The PDF is a printout, not the original executable HTML/JavaScript source.** This repository currently contains an application starter, not a deployed or functionally complete version of the original dashboard.

The original JSON contains organization branding, internal meeting material, example document paths, KPI records, governance data, and possibly personal data; therefore, it should **not** be committed verbatim to a public repository. Keep original data in a private location, and do not treat example entries as verified institutional facts.

## Run the prototype

Open `index.html` in a modern browser. The sample KPIs and graph are illustrative. You can import a local JSON export: select **Import JSON**. The application reads it locally and does not upload the file to GitHub or to a server. It intentionally displays only the top-level `kpis` array (name, value, status) and the `orgName` field from the original export format. It does not store the imported dataset or expose the remaining sensitive fields.

## Best deployment path

1. Start with this mobile-friendly static web app on GitHub Pages for demonstration using **only synthetic/redacted data**.
2. Later make it a PWA with offline support and installability.
3. For real institutional use, move data to an authenticated backend (such as Supabase/PostgreSQL), with role-based permissions, audit trails, data retention rules, backups, and restricted evidence uploads. GitHub Pages is public; do not use it to store confidential academic data.
4. Validate each metric against its source evidence; distinguish targets, achievements, reporting periods, and data owners.

## Proposed modules

- Leadership and institutional KPI dashboard
- IQAC/NAAC/NIRF evidence matrix with ownership and due dates
- Research, patents, innovation and consultancy tracking
- OBE and CO-PO attainment
- Placements, internships, student progression
- Governance minutes, tasks, compliance and follow-up
- Budget, utilization, projects, and risk register

## License

No license has yet been granted for this repository's content. Select a license before inviting outside contributions.
