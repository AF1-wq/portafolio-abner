## 2024-05-16 - Enforce application/json to Prevent CSRF
**Vulnerability:** The `/api/send-message` endpoint allowed simple cross-origin form submissions to bypass CSRF protections because it fell back to processing `request.form.to_dict()` if `request.get_json(silent=True)` failed.
**Learning:** By allowing standard form URL-encoded data (`application/x-www-form-urlencoded`), simple GET/POST cross-origin requests could be used by attackers to submit data to the endpoint. `application/json` is not a simple request type in CORS and requires a preflight `OPTIONS` request.
**Prevention:** Always enforce `request.is_json` and reject non-JSON payloads for sensitive endpoints or data-modifying endpoints that do not implement other CSRF mitigation strategies like anti-CSRF tokens.
