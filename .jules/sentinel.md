## 2023-10-24 - Cross-Site Request Forgery (CSRF) in form endpoint
**Vulnerability:** The `/api/send-message` endpoint accepted `application/x-www-form-urlencoded` payloads, allowing for a simple request CSRF attack without triggering a CORS preflight.
**Learning:** Accepting traditional form submissions on an API endpoint bypassing CORS protections allows attackers to submit forms on behalf of the user, potentially leading to spam or unwanted actions.
**Prevention:** Enforce `application/json` Content-Type on the API endpoint, as cross-origin JSON requests trigger a CORS preflight which the server will reject if no permissive CORS headers are set.
