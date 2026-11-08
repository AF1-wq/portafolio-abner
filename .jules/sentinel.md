## 2026-11-01 - CSRF Protection for Endpoints Handling Traditional Forms
**Vulnerability:** The `/api/send-message` endpoint lacked Cross-Site Request Forgery (CSRF) protection. Normally, an API might enforce a strict `Content-Type: application/json` as partial CSRF defense, but this endpoint also accepts `application/x-www-form-urlencoded` or `multipart/form-data` to support traditional HTML form submissions.
**Learning:** Forcing strict JSON on dual-use endpoints (API + Form submission) breaks legitimate traditional form functionality. CSRF can still be effectively mitigated by relying on standard Origin or Referer header validation when requests are made by modern browsers.
**Prevention:** When an endpoint handles both JSON and standard form submissions, validate the `Origin` or `Referer` headers against the server's `request.host` instead of strictly enforcing the Content-Type.

## 2026-11-08 - CSRF Bypass via URL Credentials in Origin/Referer Validation
**Vulnerability:** The CSRF validation logic in `/api/send-message` extracted the origin/referer hostname by manually parsing `.netloc.split(':')[0]`. An attacker could bypass this check by supplying a malicious URL with credentials, such as `http://localhost:pass@attacker.com`, where `localhost` would incorrectly be parsed as the netloc prefix, passing the validation against `request.host`.
**Learning:** Manual parsing of URL components is error-prone and can lead to security bypasses when edge cases like embedded URL credentials are used by an attacker.
**Prevention:** Always use safe and established built-in parsing functions like `urllib.parse.urlparse().hostname` which correctly handles embedded credentials and safely extracts the actual hostname.
