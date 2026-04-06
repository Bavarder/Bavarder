name: Bug Report
description: File a bug report.
title: ""
labels: ["bug", "triage"]
type: bug
body:
  - type: markdown
    attributes:
      value: |
        Thanks for taking the time to fill out this bug report!
  - type: textarea
    id: what-happened
    attributes:
      label: What happened?
      description: Also tell us, what did you expect to happen?
      placeholder: Tell us what you see!
      value: "A bug happened!"
    validations:
      required: true
  - type: dropdown
    id: version
    attributes:
      label: Version
      description: What version of Bavarder are you running? (Must be >= 2.0)
      options:
        - 2.0 (Latest)
        - > 2.0 (Devel)
        - < 2.0 (UNSUPPORTED)
      default: 0
    validations:
      required: true
  - type: textarea
    id: logs
    attributes:
      label: Relevant log output
      description: Please copy and paste any relevant log output. This will be automatically formatted into code, so no need for backticks.
      render: shell
  - type: checkboxes
    id: terms
    attributes:
      label: Code of Conduct
      description: By submitting this issue, you agree to follow the GNOME Code of Conduct
      options:
        - label: I agree to follow the GNOME Code of Conduct
          required: true
  - type: upload
    id: screenshots
    attributes:
      label: Upload screenshots
      description: If applicable, add screenshots to help explain your problem.
    validations:
      required: false
