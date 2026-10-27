## 2024-10-27 - CSRF Vulnerability in API Endpoint
**Vulnerability:** The `/api/send-message` endpoint allowed processing simple form submissions without validating the `Content-Type`.
**Learning:** This lack of validation enabled Cross-Site Request Forgery (CSRF) via simple cross-origin form POSTs, which bypass CORS preflight checks.
**Prevention:** Strictly enforce `application/json` Content-Type on API endpoints, as browsers require a preflight `OPTIONS` request for cross-origin JSON payloads, effectively mitigating CSRF.
