### `kapp --help`

```
kapp - deploy and manage Kubernetes manifests

USAGE
  kapp <command> [flags]

COMMANDS
  deploy     Apply a manifest to a cluster
  delete     Remove resources defined by a manifest
  status     Show rollout and resource health for a deployment
  logs       Stream logs from pods managed by a deployment
  version    Print client and server version

FLAGS
  -n, --namespace <name>   Kubernetes namespace (default: $KAPP_NAMESPACE or "default")
      --context <name>     Kubeconfig context (default: current-context)
      --no-input           Never prompt; fail if input would be required
      --no-color           Disable color output (also honors NO_COLOR)
  -q, --quiet              Suppress non-error output
  -h, --help               Show help for any command
      --version            Print version and exit

ENVIRONMENT
  KAPP_NAMESPACE   Default namespace when --namespace is not set
  KAPP_CONTEXT     Default kubeconfig context
  KAPP_ENV         Cluster environment label (dev|staging|prod); prod triggers
                   confirmation prompts on mutating commands
  NO_COLOR         Disable color output
  KUBECONFIG       Path to kubeconfig (standard)

EXAMPLES
  Deploy a manifest to the current namespace:
    $ kapp deploy ./manifests/api.yaml

  Deploy from stdin in CI:
    $ helm template ./chart | kapp deploy - --namespace api --wait

  Watch a rollout:
    $ kapp status api --namespace api

  Tail logs from every pod in a deployment:
    $ kapp logs api --namespace api --follow

Run `kapp <command> --help` for command-specific flags.
Docs:  https://docs.example.internal/kapp
Bugs:  https://docs.example.internal/kapp/support
```

---

### `kapp deploy --help`

```
kapp deploy - apply a manifest to a cluster

USAGE
  kapp deploy <manifest> [flags]
  kapp deploy -          [flags]   # read manifest from stdin

ARGUMENTS
  <manifest>   Path to a YAML manifest file. Use "-" to read from stdin.

FLAGS
  -n, --namespace <name>   Namespace to deploy into
                           (default: $KAPP_NAMESPACE or "default")
      --dry-run            Print the diff that would be applied; change nothing
      --wait               Block until all resources reach Ready, or --timeout
                           elapses (default: false)
      --timeout <duration> Max time to wait when --wait is set
                           (default: 10m; e.g. 30s, 5m, 1h)
      --context <name>     Kubeconfig context to target
      --confirm <name>     Pre-confirm a prod deploy non-interactively; value
                           must equal the target namespace
      --no-input           Never prompt; required for prod deploys in CI when
                           --confirm is not supplied (deploy will fail)
  -q, --quiet              Suppress progress output; errors still go to stderr
  -h, --help               Show this help

CONFIRMATION
  When KAPP_ENV=prod (or the resolved context maps to a prod cluster), kapp
  will prompt you to type the target namespace before applying. To deploy to
  prod from a non-interactive context (e.g. GitHub Actions), pass
  --confirm=<namespace>. --no-input alone will not bypass the check.

EXIT CODES
  0   Apply succeeded (or --dry-run produced a clean diff)
  1   Apply failed
  2   Invalid arguments or manifest could not be parsed
  3   Confirmation required but not provided (prod safeguard)
  4   --wait timed out before resources became Ready

EXAMPLES
  Apply a manifest to a non-prod namespace:
    $ kapp deploy ./manifests/api.yaml --namespace api-staging

  Preview the change without touching the cluster:
    $ kapp deploy ./manifests/api.yaml --dry-run

  Deploy and wait up to five minutes for rollout:
    $ kapp deploy ./manifests/api.yaml --wait --timeout=5m

  Pipe a rendered chart into kapp from CI:
    $ helm template ./chart -f values.prod.yaml \
        | kapp deploy - --namespace api --wait

  Deploy to prod from GitHub Actions (pre-confirmed):
    $ kapp deploy ./manifests/api.yaml \
        --namespace api \
        --confirm=api \
        --wait --timeout=10m

Docs: https://docs.example.internal/kapp/deploy
```
