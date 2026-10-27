## Issue Documentation Table

| Issue | Type | Original Location | Description | Fix Approach |
|---|---|---|---|---|
| Hardcoded ERP API key | Security | Global configuration | API key was stored directly in source code. | Read the key from the `ERP_API_KEY` environment variable. |
| Disabled TLS verification | Security | `syncToErp()` | `verify=False` disabled HTTPS certificate verification. | Use default certificate verification. |
| Shell command execution | Security | `backupReports()` | `subprocess.Popen()` used `shell=True`. | Replace shell execution with Python's `tarfile` module. |
| Unsafe reminder command | Security | `scheduleReminders()` | Command string was configured for shell execution. | Use a list of arguments with `shell=False`. |
| Mutable default argument | Bug | `markAttendance()` | `register={}` could share state across calls. | Use `None` and initialize a new dictionary. |
| Incorrect eligibility boundary | Logic Bug | `isEligible()` | Exactly 75% attendance was rejected. | Change `>` to `>=`. |
| Division by zero | Reliability | `attendancePercentage()` | Empty records could cause division by zero. | Return `0.0` when no records exist. |
| Unsafe CSV handling | Reliability | `exportCsv()` | File handling lacked a context manager and explicit encoding. | Use `with open(...)` and UTF-8 encoding. |
| Spreadsheet formula injection | Security | `main()` / `exportCsv()` | Formula-like student names could be interpreted as spreadsheet formulas. | Sanitize potentially dangerous CSV cell values. |
| Deprecated TLS protocol | Security | `legacyChannel()` | TLS 1.0 was used as the default protocol. | Remove deprecated TLS usage. |
| Poor naming and formatting | Code Quality | Multiple functions | CamelCase names and inconsistent formatting reduced readability. | Use snake_case and consistent formatting. |
| Empty attendance history | Reliability | `latestDate()` | Finding the maximum date could fail for empty records. | Return `None` when there are no records. |


