#!/usr/bin/env python3
import argparse
import csv
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import yaml


def find_yaml_files(paths: List[Path]) -> List[Path]:
    files = []
    for path in paths:
        if path.is_dir():
            for ext in ("*.yaml", "*.yml", "*.yaml.template", "*.yml.template"):
                files.extend(sorted(path.rglob(ext)))
        elif path.is_file():
            files.append(path)
    return sorted(files)


def load_yaml_documents(path: Path) -> List[Dict[str, Any]]:
    docs = []
    text = path.read_text()
    for doc in yaml.safe_load_all(text):
        if doc is None:
            continue
        if isinstance(doc, dict):
            docs.append(doc)
    return docs


def get_field(obj: Dict[str, Any], keys: List[str], default=None):
    for key in keys:
        if isinstance(obj, dict) and key in obj:
            obj = obj[key]
        else:
            return default
    return obj


def summarize_labels(labels: Optional[Dict[str, Any]]) -> str:
    if not labels:
        return ""
    return ";".join(f"{k}={v}" for k, v in sorted(labels.items()))


def flatten_list(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return ";".join(str(x) for x in value if x is not None)
    return str(value)


def extract_metadata(doc: Dict[str, Any], source: str) -> Dict[str, Any]:
    metadata = doc.get("metadata", {}) or {}
    name = metadata.get("name", "")
    namespace = metadata.get("namespace", "default")
    labels = metadata.get("labels", {}) or {}
    annotations = metadata.get("annotations", {}) or {}
    return {
        "source_file": source,
        "kind": doc.get("kind", ""),
        "name": name,
        "namespace": namespace,
        "labels": labels,
        "annotations": annotations,
        "app_label": labels.get("app") or labels.get("app.kubernetes.io/name", ""),
    }


def extract_deployment(doc: Dict[str, Any], source: str) -> Dict[str, Any]:
    spec = doc.get("spec", {}) or {}
    template = get_field(spec, ["template"]) or {}
    pod_spec = get_field(template, ["spec"]) or {}
    containers = pod_spec.get("containers", []) or []
    images = [c.get("image", "") for c in containers]
    ports = []
    for c in containers:
        for p in c.get("ports", []) or []:
            ports.append(p.get("containerPort"))
    return {
        **extract_metadata(doc, source),
        "replicas": spec.get("replicas", 1),
        "container_images": images,
        "container_ports": ports,
        "resources": [c.get("resources", {}) for c in containers],
        "readiness_probe": [c.get("readinessProbe") for c in containers if c.get("readinessProbe")],
        "liveness_probe": [c.get("livenessProbe") for c in containers if c.get("livenessProbe")],
    }


def extract_service(doc: Dict[str, Any], source: str) -> Dict[str, Any]:
    spec = doc.get("spec", {}) or {}
    ports = spec.get("ports", []) or []
    port_pairs = [f"{p.get('port')}->{p.get('targetPort')}" for p in ports]
    return {
        **extract_metadata(doc, source),
        "service_type": spec.get("type", "ClusterIP"),
        "service_ports": port_pairs,
        "selector": spec.get("selector", {}),
    }


def extract_ingress(doc: Dict[str, Any], source: str) -> Dict[str, Any]:
    spec = doc.get("spec", {}) or {}
    hosts = []
    for rule in spec.get("rules", []) or []:
        host = rule.get("host")
        if host:
            hosts.append(host)
    return {
        **extract_metadata(doc, source),
        "ingress_class": spec.get("ingressClassName", ""),
        "hosts": hosts,
    }


def extract_hpa(doc: Dict[str, Any], source: str) -> Dict[str, Any]:
    spec = doc.get("spec", {}) or {}
    target = spec.get("scaleTargetRef", {}) or {}
    return {
        **extract_metadata(doc, source),
        "target_kind": target.get("kind", ""),
        "target_name": target.get("name", ""),
        "min_replicas": spec.get("minReplicas"),
        "max_replicas": spec.get("maxReplicas"),
        "metrics": spec.get("metrics", []),
    }


def extract_pdb(doc: Dict[str, Any], source: str) -> Dict[str, Any]:
    spec = doc.get("spec", {}) or {}
    return {
        **extract_metadata(doc, source),
        "min_available": spec.get("minAvailable"),
        "max_unavailable": spec.get("maxUnavailable"),
    }


def extract_networkpolicy(doc: Dict[str, Any], source: str) -> Dict[str, Any]:
    spec = doc.get("spec", {}) or {}
    return {
        **extract_metadata(doc, source),
        "policy_types": spec.get("policyTypes", []),
        "pod_selector": spec.get("podSelector", {}),
        "ingress": spec.get("ingress", []),
        "egress": spec.get("egress", []),
    }


def create_inventory_item(doc: Dict[str, Any], source: str) -> Dict[str, Any]:
    kind = doc.get("kind", "")
    if kind in {"Deployment", "StatefulSet", "DaemonSet", "Job", "CronJob"}:
        return extract_deployment(doc, source)
    if kind == "Service":
        return extract_service(doc, source)
    if kind == "Ingress":
        return extract_ingress(doc, source)
    if kind == "HorizontalPodAutoscaler":
        return extract_hpa(doc, source)
    if kind == "PodDisruptionBudget":
        return extract_pdb(doc, source)
    if kind == "NetworkPolicy":
        return extract_networkpolicy(doc, source)
    return {
        **extract_metadata(doc, source),
        "details": doc.get("spec", {}),
    }


def generate_inventory(source_paths: List[Path]) -> List[Dict[str, Any]]:
    yaml_files = find_yaml_files(source_paths)
    inventory = []
    for path in yaml_files:
        for doc in load_yaml_documents(path):
            item = create_inventory_item(doc, str(path))
            inventory.append(item)
    return inventory


def write_json(items: List[Dict[str, Any]], output_path: Path) -> None:
    output_path.write_text(json.dumps(items, indent=2))


def write_csv(items: List[Dict[str, Any]], output_path: Path) -> None:
    if not items:
        output_path.write_text("")
        return
    headers = [
        "source_file",
        "kind",
        "name",
        "namespace",
        "app_label",
        "labels",
        "annotations",
        "replicas",
        "container_images",
        "container_ports",
        "service_type",
        "service_ports",
        "ingress_class",
        "hosts",
        "target_kind",
        "target_name",
        "min_replicas",
        "max_replicas",
        "policy_types",
        "pod_selector",
        "selector",
    ]
    with output_path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        for item in items:
            row = {
                "source_file": item.get("source_file", ""),
                "kind": item.get("kind", ""),
                "name": item.get("name", ""),
                "namespace": item.get("namespace", ""),
                "app_label": item.get("app_label", ""),
                "labels": summarize_labels(item.get("labels")),
                "annotations": summarize_labels(item.get("annotations")),
                "replicas": item.get("replicas", ""),
                "container_images": flatten_list(item.get("container_images", [])),
                "container_ports": flatten_list(item.get("container_ports", [])),
                "service_type": item.get("service_type", ""),
                "service_ports": flatten_list(item.get("service_ports", [])),
                "ingress_class": item.get("ingress_class", ""),
                "hosts": flatten_list(item.get("hosts", [])),
                "target_kind": item.get("target_kind", ""),
                "target_name": item.get("target_name", ""),
                "min_replicas": item.get("min_replicas", ""),
                "max_replicas": item.get("max_replicas", ""),
                "policy_types": flatten_list(item.get("policy_types", [])),
                "pod_selector": summarize_labels(item.get("pod_selector", {})),
                "selector": summarize_labels(item.get("selector", {})),
            }
            writer.writerow(row)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a Kubernetes inventory from YAML manifests or Helm rendered output."
    )
    parser.add_argument(
        "paths",
        nargs="+",
        help="File or directory paths to scan for YAML manifests."
    )
    parser.add_argument(
        "--output-json",
        default="migration-assessment/discovery/workload_inventory_yaml.json",
        help="Path to write JSON inventory."
    )
    parser.add_argument(
        "--output-csv",
        default="migration-assessment/discovery/workload_inventory_yaml.csv",
        help="Path to write CSV inventory."
    )
    args = parser.parse_args()

    sources = [Path(p) for p in args.paths]
    items = generate_inventory(sources)

    write_json(items, Path(args.output_json))
    write_csv(items, Path(args.output_csv))
    print(f"Wrote {len(items)} inventory items to {args.output_json} and {args.output_csv}")


if __name__ == "__main__":
    main()
