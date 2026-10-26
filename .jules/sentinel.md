
## 2026-10-26 - Enforce application/json for API endpoints to prevent CSRF
**Vulnerability:** The `/api/send-message` endpoint previously accepted form data (`application/x-www-form-urlencoded` via `request.form.to_dict()`). This made the application vulnerable to Cross-Site Request Forgery (CSRF) via simple cross-origin form submissions without preflight checks.
**Learning:** Permitting simple form data (`application/x-www-form-urlencoded` or `multipart/form-data`) on state-changing API endpoints bypasses CORS preflight requests (OPTIONS), allowing malicious sites to submit data on behalf of a user.
**Prevention:** Strictly enforce `application/json` Content-Type using `request.is_json` and reject unsupported content types with a 415 HTTP status. This forces the browser to send a CORS preflight request, protecting the endpoint from simple CSRF attacks.
