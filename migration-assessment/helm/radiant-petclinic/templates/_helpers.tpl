{{/*
Common labels and helpers for radiant-petclinic.
*/}}
{{- define "radiant-petclinic.labels" -}}
app.kubernetes.io/name: {{ include "radiant-petclinic.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}

{{- define "radiant-petclinic.name" -}}
{{ .Values.name }}
{{- end -}}
