## 2026-11-01 - CSRF Protection for Endpoints Handling Traditional Forms
**Vulnerability:** The `/api/send-message` endpoint lacked Cross-Site Request Forgery (CSRF) protection. Normally, an API might enforce a strict `Content-Type: application/json` as partial CSRF defense, but this endpoint also accepts `application/x-www-form-urlencoded` or `multipart/form-data` to support traditional HTML form submissions.
**Learning:** Forcing strict JSON on dual-use endpoints (API + Form submission) breaks legitimate traditional form functionality. CSRF can still be effectively mitigated by relying on standard Origin or Referer header validation when requests are made by modern browsers.
**Prevention:** When an endpoint handles both JSON and standard form submissions, validate the `Origin` or `Referer` headers against the server's `request.host` instead of strictly enforcing the Content-Type.

## 2026-11-05 - URL Credentials CSRF Bypass Protection
**Vulnerability:** The CSRF protection in `/api/send-message` validated the `Origin` or `Referer` headers using `.netloc.split(':')[0]`. An attacker could bypass this by using URL credentials (e.g., `http://target_host:password@attacker.com`), which parses the target host as the username but correctly reaches the attacker's server, tricking the validation into accepting the request.
**Learning:** Extracting the host from `.netloc` directly is unsafe if URL credentials are present. Using standard URL parsing fields like `.hostname` safely extracts the domain ignoring authentication portions.
**Prevention:** Always use `.hostname` from `urlparse` rather than manually manipulating `.netloc` to extract the host securely.
