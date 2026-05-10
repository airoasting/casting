# Privacy Policy

## Summary

**We never collect content.** Anonymous metadata only, opt-in by default OFF.

## What we collect (only if user opts in)

| Field | Example |
|---|---|
| user_id | UUID generated locally on first opt-in |
| skill_version | "0.1.0" |
| case_id | "p1" |
| final_score | 9.5 |
| round_count | 2 |
| slide_template_id | "tpl-consulting-firm" |
| total_cost_usd | 0.36 |
| anti_patterns_detected | {"VAGUE_CTA": 1} |
| debate_triggered | true |
| completion_status | "passed" |
| timestamp | ISO 8601 |

## What we never collect

- Your input prompt (the task description you give `/roasting`)
- BLACK draft content
- RGSB scoring comments or debate transcripts
- Slide template HTML rendered output
- File paths, IP addresses, system info beyond the fields listed above

## How to control

```bash
# Disable telemetry (default)
echo '{"telemetry": false}' > ~/.claude/roasting/config.json

# Enable
echo '{"telemetry": true}' > ~/.claude/roasting/config.json
```

## Backend

Supabase project owned by AI ROASTING. Row-level security: anonymous role
can INSERT only — no SELECT/UPDATE/DELETE access from the client.

## Beta data retention

Data collected during open beta v0.1.x is retained for v1.0 evolution analysis.
After v1.0 release, retention policy will be updated. To request deletion of
your anonymous user_id's records, open a GitHub Issue with the user_id.
