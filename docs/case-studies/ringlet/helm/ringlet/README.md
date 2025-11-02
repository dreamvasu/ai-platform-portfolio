# Ringlet Helm Chart

Official Helm chart for deploying Ringlet educational platform on Kubernetes.

## TL;DR

```bash
# Add your custom values
helm install ringlet ./ringlet \
  --namespace ringlet \
  --create-namespace \
  --set global.domain=ringlet.yourcompany.com \
  --set django.secrets.secretKey=YOUR_SECRET_KEY \
  --set django.secrets.dbPassword=YOUR_DB_PASSWORD
```

## Prerequisites

- Kubernetes 1.20+
- Helm 3.0+
- kubectl configured
- Container image pushed to registry

## Installing the Chart

### 1. Clone/Download the chart
```bash
cd /path/to/helm/charts
```

### 2. Create custom values file
```bash
cp values.yaml values-production.yaml
# Edit values-production.yaml with your settings
```

### 3. Install
```bash
helm install ringlet ./ringlet \
  --namespace ringlet \
  --create-namespace \
  --values values-production.yaml
```

### 4. Verify
```bash
helm status ringlet -n ringlet
kubectl get all -n ringlet
```

## Uninstalling the Chart

```bash
helm uninstall ringlet -n ringlet
kubectl delete namespace ringlet
```

## Configuration

### Key Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `global.domain` | Application domain | `ringlet.example.com` |
| `django.image.repository` | Django image repo | `gcr.io/YOUR_PROJECT_ID/ringlet` |
| `django.image.tag` | Django image tag | `latest` |
| `django.replicaCount` | Number of Django pods | `3` |
| `django.autoscaling.enabled` | Enable HPA | `true` |
| `django.autoscaling.maxReplicas` | Max replicas | `10` |
| `postgresql.enabled` | Deploy PostgreSQL | `true` |
| `postgresql.persistence.size` | DB storage size | `10Gi` |
| `redis.enabled` | Deploy Redis | `true` |
| `ingress.enabled` | Enable ingress | `true` |
| `ingress.className` | Ingress class | `gce` |

### Full Configuration

See [values.yaml](values.yaml) for all available options.

## Examples

### Production Deployment

```yaml
# values-production.yaml
global:
  projectId: "my-gcp-project"
  domain: "ringlet.mycompany.com"

django:
  image:
    repository: gcr.io/my-gcp-project/ringlet
    tag: "v1.2.3"
    pullPolicy: IfNotPresent

  replicaCount: 5

  resources:
    requests:
      memory: "1Gi"
      cpu: "1000m"
    limits:
      memory: "2Gi"
      cpu: "2000m"

  autoscaling:
    enabled: true
    minReplicas: 5
    maxReplicas: 20

  secrets:
    secretKey: "prod-secret-key-change-me"
    dbPassword: "prod-db-password"

postgresql:
  enabled: true
  persistence:
    size: 50Gi
    storageClass: "ssd-storage"

ingress:
  enabled: true
  className: "nginx"
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
  hosts:
    - host: ringlet.mycompany.com
      paths:
        - path: /
          pathType: Prefix
```

```bash
helm install ringlet ./ringlet \
  --namespace ringlet \
  --create-namespace \
  --values values-production.yaml
```

### Development Deployment

```yaml
# values-dev.yaml
django:
  image:
    tag: "dev"
  replicaCount: 1
  autoscaling:
    enabled: false
  env:
    DEBUG: "True"

postgresql:
  persistence:
    size: 5Gi

redis:
  resources:
    requests:
      memory: "64Mi"
      cpu: "50m"

ingress:
  enabled: false
```

### Using External Databases

```yaml
# values-external-db.yaml
postgresql:
  enabled: false  # Don't deploy PostgreSQL

externalPostgresql:
  host: "cloudsql-proxy"
  port: 5432

redis:
  enabled: false  # Don't deploy Redis

externalRedis:
  host: "redis.cache.example.com"
  port: 6379
```

## Upgrading

```bash
# Update image tag
helm upgrade ringlet ./ringlet \
  --namespace ringlet \
  --set django.image.tag=v1.2.3 \
  --reuse-values

# Or with values file
helm upgrade ringlet ./ringlet \
  --namespace ringlet \
  --values values-production.yaml
```

## Rollback

```bash
# List releases
helm history ringlet -n ringlet

# Rollback to previous
helm rollback ringlet -n ringlet

# Rollback to specific revision
helm rollback ringlet 2 -n ringlet
```

## Templating / Dry Run

```bash
# See generated manifests
helm template ringlet ./ringlet \
  --namespace ringlet \
  --values values-production.yaml

# Test installation
helm install ringlet ./ringlet \
  --namespace ringlet \
  --values values-production.yaml \
  --dry-run --debug
```

## Customization

### Adding Custom ConfigMaps

Create `templates/custom-config.yaml`:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ include "ringlet.fullname" . }}-custom
  namespace: {{ .Values.namespace }}
data:
  MY_CUSTOM_VAR: "value"
```

### Adding Init Containers

Edit `values.yaml`:
```yaml
django:
  initContainers:
    - name: custom-init
      image: busybox
      command: ['sh', '-c', 'echo Initializing...']
```

## Troubleshooting

### Check Helm status
```bash
helm status ringlet -n ringlet
```

### View manifests
```bash
helm get manifest ringlet -n ringlet
```

### View values
```bash
helm get values ringlet -n ringlet
```

### Check pods
```bash
kubectl get pods -n ringlet
kubectl describe pod <pod-name> -n ringlet
kubectl logs <pod-name> -n ringlet
```

### Debug deployment
```bash
helm install ringlet ./ringlet \
  --namespace ringlet \
  --values values-production.yaml \
  --dry-run --debug
```

## Best Practices

1. **Version Control**: Store values files in git
2. **Secrets Management**: Use external secret managers (Vault, Google Secret Manager)
3. **Image Tags**: Use specific tags, not `latest`
4. **Resource Limits**: Always set requests and limits
5. **Health Checks**: Configure liveness and readiness probes
6. **Monitoring**: Enable monitoring and alerting
7. **Backups**: Regular database backups

## Support

- **Issues**: https://github.com/dreamvasu/ringlet/issues
- **Documentation**: https://github.com/dreamvasu/ringlet/wiki
