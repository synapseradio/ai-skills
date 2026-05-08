```
kapp - deploy and manage Kubernetes applications

usage: kapp <command> [<args>]

These are the common kapp commands:

  deploy     Apply a manifest to a cluster
  delete    Remove a deployed application
  status    Show the current state of a deployment
  logs      Stream logs from a deployed application
  version   Print kapp version information

Flags:
  -h, --help       Show help for a command
      --context    Override the active kubeconfig context

Environment:
  KAPP_NAMESPACE   Default namespace if --namespace is not set
  KAPP_CONTEXT     Default kubeconfig context
  KUBECONFIG       Path to kubeconfig (standard)

Run 'kapp <command> --help' for more information on a specific command.
Docs: https://docs.example.internal/kapp
```

```
kapp deploy - apply a manifest to a cluster

usage: kapp deploy <manifest> [flags]

Applies the resources in <manifest> to the target cluster. <manifest> is a
path to a YAML file, or '-' to read from stdin.

Deploys to namespaces marked as production (resolved from KAPP_PROD_NAMESPACES,
defaulting to 'prod', 'production', and any namespace prefixed with 'prod-')
prompt for confirmation before applying. Use --yes to skip the prompt in
non-interactive contexts such as CI; pipelines should set KAPP_ASSUME_YES=1
instead so the intent is visible in the workflow file.

Flags:
  -n, --namespace <name>   Namespace to deploy into (default: $KAPP_NAMESPACE, then 'default')
      --dry-run            Render and validate without applying. Prints the
                           server-side diff and exits non-zero on drift.
      --wait               Block until all resources reach a ready state, or
                           until --timeout elapses
      --timeout <duration> Maximum time to wait when --wait is set
                           (default: 10m). Accepts Go duration syntax: 30s, 5m, 1h.
      --yes                Skip the production confirmation prompt
  -h, --help               Show this help

Examples:
  # Deploy a manifest to the current namespace
  kapp deploy ./manifests/web.yaml

  # Deploy to a specific namespace and wait for rollout
  kapp deploy -n payments --wait ./manifests/api.yaml

  # Render from a templating tool and pipe in
  helm template ./chart | kapp deploy -

  # Validate a change without touching the cluster
  kapp deploy --dry-run ./manifests/web.yaml

  # Non-interactive deploy from CI
  KAPP_ASSUME_YES=1 kapp deploy -n production --wait --timeout=15m ./manifests/web.yaml

Exit codes:
  0  Deploy succeeded (or --dry-run found no drift)
  1  Deploy failed
  2  Invalid arguments or manifest
  3  Confirmation declined
  4  --wait timed out before resources became ready

See also:
  kapp status, kapp logs, kapp delete
  https://docs.example.internal/kapp/deploy
```
