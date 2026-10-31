## 2026-10-31 - [High] Fix CSRF vulnerability in API endpoints
**Vulnerability:** Missing CSRF (Cross-Site Request Forgery) protection on the `/api/*` endpoints allowed cross-origin form submissions to mutate state and send emails without user consent.
**Learning:** API endpoints handling traditional POST requests (often triggered by form submissions) that do not enforce strict Content-Type requirements (e.g. `application/json`) can be bypassed by an attacker submitting a form from an external origin. Standard REST API patterns don't always protect against traditional web form vectors.
**Prevention:** Always validate the `Origin` or `Referer` headers against `request.host` for state-changing endpoints in a `before_request` hook, failing securely by returning a `403 Forbidden` status.
