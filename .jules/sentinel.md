## 2026-11-01 - CSRF Protection for Endpoints Handling Traditional Forms
**Vulnerability:** The `/api/send-message` endpoint lacked Cross-Site Request Forgery (CSRF) protection. Normally, an API might enforce a strict `Content-Type: application/json` as partial CSRF defense, but this endpoint also accepts `application/x-www-form-urlencoded` or `multipart/form-data` to support traditional HTML form submissions.
**Learning:** Forcing strict JSON on dual-use endpoints (API + Form submission) breaks legitimate traditional form functionality. CSRF can still be effectively mitigated by relying on standard Origin or Referer header validation when requests are made by modern browsers.
**Prevention:** When an endpoint handles both JSON and standard form submissions, validate the `Origin` or `Referer` headers against the server's `request.host` instead of strictly enforcing the Content-Type.

## 2024-11-11 - URL Parsing bypass for CSRF mitigation
**Vulnerability:** CSRF protection in `app.py` incorrectly relied on `urlparse(origin).netloc.split(':')[0]`. An attacker could construct an Origin like `http://localhost:password@attacker.com`, which `.netloc` parses as `localhost:password@attacker.com`, and splitting on `:` returns `localhost`, bypassing the validation against `request.host` (`localhost`).
**Learning:** `urllib.parse.urlparse().netloc` includes basic auth credentials (`user:password`). Directly parsing `.netloc` to extract the host is vulnerable to bypasses because an attacker can inject the expected hostname into the credentials part of a malicious domain.
**Prevention:** When validating URLs or domains in Python, always use `urlparse().hostname` which correctly ignores credentials and ports, safely returning just the host.
