# Lab 5: Static Code Analysis — Reflection

## 1. What is static code analysis?

Static code analysis is the process of examining source code without executing the program. It helps developers identify potential programming errors, security vulnerabilities, and style violations before deployment.

## 2. What is the difference between Pylint, Bandit, and Flake8?

Pylint checks Python code quality, naming conventions, and possible programming errors. Bandit identifies common security vulnerabilities and unsafe coding patterns. Flake8 checks formatting, whitespace, and compliance with Python style conventions, including many PEP 8 rules.

## 3. What issues did you identify and fix during this lab?

I addressed multiple issues in the attendance tracker. These included a hardcoded ERP API key, disabled TLS certificate verification, shell-based command execution, a mutable default argument, and an incorrect attendance eligibility condition. I also improved empty-record handling, CSV file management, spreadsheet formula injection protection, and code formatting.

These changes helped make the program more secure, reliable, and maintainable.

## 4. How does static code analysis improve software quality?

Static code analysis helps detect potential defects early in development. It improves security, encourages consistent coding practices, makes code easier to read, and reduces maintenance effort. However, static analysis should be combined with program execution and functional testing because it cannot detect every possible runtime or logical problem.


