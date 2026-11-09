## 2026-11-01 - CSRF Protection for Endpoints Handling Traditional Forms
**Vulnerability:** The `/api/send-message` endpoint lacked Cross-Site Request Forgery (CSRF) protection. Normally, an API might enforce a strict `Content-Type: application/json` as partial CSRF defense, but this endpoint also accepts `application/x-www-form-urlencoded` or `multipart/form-data` to support traditional HTML form submissions.
**Learning:** Forcing strict JSON on dual-use endpoints (API + Form submission) breaks legitimate traditional form functionality. CSRF can still be effectively mitigated by relying on standard Origin or Referer header validation when requests are made by modern browsers.
**Prevention:** When an endpoint handles both JSON and standard form submissions, validate the `Origin` or `Referer` headers against the server's `request.host` instead of strictly enforcing the Content-Type.

## 2026-11-01 - CSRF Bypass via Incorrect Netloc Parsing
**Vulnerability:** The `/api/send-message` endpoint used `.netloc.split(':')[0]` from `urllib.parse.urlparse` to validate the `Origin` and `Referer` headers against `request.host`. This is vulnerable to bypass if an attacker uses URL credentials (e.g., `http://localhost:5000@attacker.com`), where the netloc parses to `localhost:5000@attacker.com`, and `.split(':')[0]` yields `localhost`, bypassing the validation.
**Learning:** Parsing `.netloc` directly is error-prone because it can include credentials (`user:pass@host:port`). `urlparse` provides a `.hostname` attribute specifically designed to safely extract just the hostname.
**Prevention:** Always use `urllib.parse.urlparse().hostname` instead of parsing `.netloc` directly when comparing host headers for security validations.
