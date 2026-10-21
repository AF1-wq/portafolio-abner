## 2024-10-18 - [CSRF Protection]
**Vulnerability:** The `/api/send-message` endpoint accepts simple form submissions via `request.form.to_dict()` as a fallback when JSON parsing fails, but does not implement CSRF protection.
**Learning:** This fallback allows cross-origin requests using standard HTML `<form>` submissions to hit the endpoint and add entries to the database, potentially enabling a Cross-Site Request Forgery (CSRF) attack.
**Prevention:** Strictly enforce `application/json` Content-Type for the endpoint or remove the form-data fallback. Since simple form POSTs don't require preflight CORS checks, requiring `application/json` mitigates CSRF attacks from basic HTML forms.
