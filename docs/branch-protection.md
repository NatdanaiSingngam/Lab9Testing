# Main branch protection — Lab 9

GitHub branch protection was enabled for `main` on 2026-09-27. The GitHub API returned:

```json
{
  "enforce_admins": true,
  "required_status_checks": ["lint", "test"]
}
```

Both `lint` and `test` passed on [PR #1](https://github.com/NatdanaiSingngam/Lab9Testing/pull/1). This API result records the setting; the requested settings-page screenshot is not included because an authenticated browser was unavailable in this environment.
