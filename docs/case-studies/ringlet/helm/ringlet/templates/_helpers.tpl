{{/*
Expand the name of the chart.
*/}}
{{- define "ringlet.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "ringlet.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "ringlet.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "ringlet.labels" -}}
helm.sh/chart: {{ include "ringlet.chart" . }}
{{ include "ringlet.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "ringlet.selectorLabels" -}}
app.kubernetes.io/name: {{ include "ringlet.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Django image
*/}}
{{- define "ringlet.django.image" -}}
{{- printf "%s:%s" .Values.django.image.repository .Values.django.image.tag }}
{{- end }}

{{/*
PostgreSQL connection string
*/}}
{{- define "ringlet.postgresql.host" -}}
{{- if .Values.postgresql.enabled }}
{{- .Values.postgresql.service.name }}
{{- else }}
{{- .Values.externalPostgresql.host }}
{{- end }}
{{- end }}

{{/*
Redis connection string
*/}}
{{- define "ringlet.redis.host" -}}
{{- if .Values.redis.enabled }}
{{- .Values.redis.service.name }}
{{- else }}
{{- .Values.externalRedis.host }}
{{- end }}
{{- end }}
