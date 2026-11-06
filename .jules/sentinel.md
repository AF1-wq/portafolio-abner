## 2026-11-01 - CSRF Protection for Endpoints Handling Traditional Forms
**Vulnerability:** The `/api/send-message` endpoint lacked Cross-Site Request Forgery (CSRF) protection. Normally, an API might enforce a strict `Content-Type: application/json` as partial CSRF defense, but this endpoint also accepts `application/x-www-form-urlencoded` or `multipart/form-data` to support traditional HTML form submissions.
**Learning:** Forcing strict JSON on dual-use endpoints (API + Form submission) breaks legitimate traditional form functionality. CSRF can still be effectively mitigated by relying on standard Origin or Referer header validation when requests are made by modern browsers.
**Prevention:** When an endpoint handles both JSON and standard form submissions, validate the `Origin` or `Referer` headers against the server's `request.host` instead of strictly enforcing the Content-Type.

## 2026-11-01 - CSRF Protection Bypass via URL Credentials
**Vulnerability:** The CSRF protection mechanism in `/api/send-message` extracted the hostname from the `Origin` and `Referer` headers using `urlparse(url).netloc.split(':')[0]`. An attacker could bypass this check by supplying a malicious origin such as `http://localhost:password@attacker.com`, because `netloc` would return `localhost:password@attacker.com`, which after splitting by `:` yields `localhost`, successfully matching the expected host.
**Learning:** Using `.netloc` from `urllib.parse.urlparse` directly when extracting hostnames is unsafe if the URL might contain authentication credentials (`user:password@`).
**Prevention:** Always use `.hostname` from the parsed URL object instead of parsing `.netloc` directly when comparing hostnames for security purposes.
