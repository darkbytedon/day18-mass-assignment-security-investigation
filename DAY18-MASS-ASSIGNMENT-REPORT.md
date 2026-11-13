
# Day 18: API Mass Assignment Security Investigation

## 1. Objective

Investigate mass assignment in a locally developed Flask API, demonstrate privilege escalation, implement a security fix, and verify the fix through automated tests.

## 2. Lab Environment

- Operating system: Ubuntu WSL
- Programming language: Python
- Framework: Flask
- Testing: Python unittest
- HTTP testing: curl
- Target: Local application (127.0.0.1:5000)

## 3. Vulnerability Description

Mass assignment occurs when an application automatically assigns client-supplied request fields to internal objects without adequately restricting which fields can be modified.

The vulnerable implementation was:

```python
users["alice"].update(data)
```

This accepted both legitimate and privileged fields.

## 4. Exploitation

The following request was submitted:

```json
{
  "email": "attacker@example.com",
  "role": "admin",
  "is_admin": true
}
```

### Observed result

The API accepted the request and changed:

- role: user -> admin
- is_admin: false -> true
- email: attacker@example.com

This demonstrated mass assignment leading to vertical privilege escalation.

## 5. Root Cause

The API trusted client-supplied fields without enforcing an allowlist.

Sensitive properties such as role and is_admin were directly modifiable through the profile endpoint.

## 6. Remediation

The vulnerable dictionary update was replaced with an allowlist.

Only the email field is accepted for updates.

Unexpected fields are rejected with HTTP 400.

The implementation also validates that the email is a non-empty string.

## 7. Verification

The fixed API was manually tested.

| Test | Expected | Result |
|---|---|---|
| Malicious role update | HTTP 400 | Passed |
| is_admin modification | Rejected | Passed |
| Mixed legitimate and privileged fields | Entire request rejected | Passed |
| Legitimate email update | HTTP 200 | Passed |

## 8. Automated Testing

Five Python unittest cases were implemented:

1. Legitimate email update.
2. Role modification rejection.
3. Administrator privilege modification rejection.
4. Mixed request rejection.
5. Empty email rejection.

Result: 5/5 tests passed.

## 9. Security Lessons

- Never trust client-supplied privileged fields.
- Apply server-side allowlisting.
- Validate all input.
- Enforce authorisation on the server.
- Reject unauthorised changes to sensitive properties.
- Use automated tests to prevent regressions.

## 10. Limitations

This was a deliberately simplified local application.

It uses a single hardcoded user and in-memory storage. It does not implement real authentication, database persistence, or multi-user authorisation.

The exercise demonstrates mass assignment and its remediation, not a complete production API security assessment.

## 11. Conclusion

The investigation successfully demonstrated a mass-assignment vulnerability, reproduced its privilege-escalation impact, implemented an allowlist-based remediation, and verified the fix through five passing automated tests.

All testing was performed against a locally controlled application.
