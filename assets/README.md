# Assets Enterprise Version Resource Usage Guide

Due to limitations of the Mintlify documentation framework, configuration files stored in the `/assets` directory cannot be referenced or downloaded using relative paths. Configuration files will be provided for download through independent online links, with each link potentially corresponding to different versions of configuration files. For easier distinction, this file is used to record different file versions.

## Directory Structure

Configuration files refer to all files under the `/assets` directory, including: `values.yaml`, `values-no-infra-for-prod.yaml`, and other files.

The directory structure is as follows:

```text
- assets
  - {date-folder} # Manage file versions by date
    - helm-values
        - values-no-infra-for-prod.yaml
        - values-no-infra-for-testing.yaml
    - ingress-nginx-controller-v1.10.1.yaml
    - values.yaml
- configs
- deploy.sh
- README.md
```

Version numbers corresponding to each configuration file:

### 01.29

- `values.yaml` → <https://assets-docs.dify.ai/2025/01/e3d53c6c7d979c77d0a1809670fbf211.yaml >
- `values-no-infra-for-prod.yaml` → <https://assets-docs.dify.ai/2025/01/309efe405120571ee99b961d02341ab8.yaml >
- `values-no-infra-for-testing.yaml` → <https://assets-docs.dify.ai/2025/01/cf9ebbdd263fae8d7a6dc558afae0e66.yaml >
- `ingress-nginx-controller-v1.10.1.yaml` → <https://assets-docs.dify.ai/2024/12/88d4cee27ae27fb0f0e31ad3d5165290.yaml >
- `ingress-nginx-controller-v1.12.1.yaml` → <https://assets-docs.dify.ai/2025/03/7dbf0f8a76522c80b306c68a70adbfce.yaml >
