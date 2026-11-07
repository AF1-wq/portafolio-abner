## 2026-11-01 - CSRF Protection for Endpoints Handling Traditional Forms
**Vulnerability:** The `/api/send-message` endpoint lacked Cross-Site Request Forgery (CSRF) protection. Normally, an API might enforce a strict `Content-Type: application/json` as partial CSRF defense, but this endpoint also accepts `application/x-www-form-urlencoded` or `multipart/form-data` to support traditional HTML form submissions.
**Learning:** Forcing strict JSON on dual-use endpoints (API + Form submission) breaks legitimate traditional form functionality. CSRF can still be effectively mitigated by relying on standard Origin or Referer header validation when requests are made by modern browsers.
**Prevention:** When an endpoint handles both JSON and standard form submissions, validate the `Origin` or `Referer` headers against the server's `request.host` instead of strictly enforcing the Content-Type.

## 2026-11-07 - Insecure URL parsing in CSRF protection
**Vulnerability:** The CSRF protection mechanism compared `request.host.split(':')[0]` against `urlparse(origin).netloc.split(':')[0]`. Because `.netloc` includes credentials (e.g. `user:pass@host`), an attacker could craft an Origin like `https://example.com:pass@attacker.com` which might bypass the check if the logic parses `.netloc` improperly, leading to a CSRF bypass.
**Learning:** Parsing `.netloc` to extract the hostname is unsafe when URLs can contain credentials. The built-in `urlparse().hostname` correctly isolates the hostname from credentials and ports.
**Prevention:** Always use `urllib.parse.urlparse().hostname` to extract the hostname from a URL when comparing hosts for security validation.
