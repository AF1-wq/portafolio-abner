## 2026-11-01 - CSRF Protection for Endpoints Handling Traditional Forms
**Vulnerability:** The `/api/send-message` endpoint lacked Cross-Site Request Forgery (CSRF) protection. Normally, an API might enforce a strict `Content-Type: application/json` as partial CSRF defense, but this endpoint also accepts `application/x-www-form-urlencoded` or `multipart/form-data` to support traditional HTML form submissions.
**Learning:** Forcing strict JSON on dual-use endpoints (API + Form submission) breaks legitimate traditional form functionality. CSRF can still be effectively mitigated by relying on standard Origin or Referer header validation when requests are made by modern browsers.
**Prevention:** When an endpoint handles both JSON and standard form submissions, validate the `Origin` or `Referer` headers against the server's `request.host` instead of strictly enforcing the Content-Type.

## 2026-11-04 - CSRF Hostname Extraction Bypass via URL Credentials
**Vulnerability:** The CSRF protection in `/api/send-message` extracted the origin/referer domain using `urlparse(origin).netloc.split(':')[0]`. An attacker could bypass this check by supplying a malicious URL with credentials matching the expected host, such as `http://localhost:pass@attacker.com`, because `.netloc` parses this as `localhost:pass@attacker.com` and `.split(':')[0]` incorrectly extracts `localhost`.
**Learning:** Extracting domain names from URLs for security checks using string manipulation on `netloc` is prone to bypasses because `netloc` can contain URL credentials (e.g., `user:pass@host:port`).
**Prevention:** Always use `urlparse().hostname` to extract the true hostname when verifying `Origin` or `Referer` headers to prevent bypasses via malicious URL formats.
