## 2025-02-28 - Missing CSRF Protection on Form Submission Endpoint

**Vulnerability:** The `/api/send-message` endpoint lacked Cross-Site Request Forgery (CSRF) protection. It accepted form submissions directly without validating the request's origin.

**Learning:** While the endpoint accepted `application/json`, it also parsed standard form submissions via `request.form.to_dict()`. Since traditional form submissions don't trigger preflight requests, a malicious site could forge a POST request to this endpoint causing unwanted side effects. Standard token-based CSRF protection might break API clients, so an Origin/Referer-based check is a good compromise for API/Form hybrid endpoints.

**Prevention:** Always validate the `Origin` or `Referer` header against `request.host` on state-changing endpoints, especially those that accept standard form data types (`application/x-www-form-urlencoded` or `multipart/form-data`) which bypass CORS preflight checks. Ensure that in production, at least one of these headers is required.