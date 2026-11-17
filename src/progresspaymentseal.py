#!/usr/bin/env python3
"""
ProgressPaymentSeal — Local-first progress payment / pay application evidence sealer.
Offline. Deterministic. Pay once.
Compatible with QuantumGuard CONTRACT-v1 and the Operator Pages suite.
"""

import argparse
import json
import hashlib
import base64
import os
from datetime import datetime, timezone
from pathlib import Path

try:
    from cryptography.hazmat.primitives.asymmetric import ed25519
    from cryptography.hazmat.primitives import serialization
    CRYPTO = True
except ImportError:
    CRYPTO = False

CONTRACT_VERSION = "1"
ALG = "ed25519"

def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def load_or_generate_key(key_path: str = "progresspaymentseal_key.pem"):
    if os.path.exists(key_path):
        with open(key_path, "rb") as f:
            priv = serialization.load_pem_private_key(f.read(), password=None)
        return priv
    if not CRYPTO:
        raise SystemExit("cryptography package required for signing. pip install cryptography")
    priv = ed25519.Ed25519PrivateKey.generate()
    pem = priv.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    with open(key_path, "wb") as f:
        f.write(pem)
    print(f"Generated new key: {key_path}")
    return priv

def get_public_key_hex(priv):
    pub = priv.public_key()
    raw = pub.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    return raw.hex()

def sign_payload(priv, payload_hash: bytes) -> str:
    sig = priv.sign(payload_hash)
    return sig.hex()

def build_payload(record: dict) -> bytes:
    # Canonical JSON for determinism
    canonical = json.dumps(record, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return canonical

def seal_record(record: dict, priv, out_path: str):
    payload = build_payload(record)
    payload_hash = hashlib.sha256(payload).digest()
    payload_hash_hex = payload_hash.hex()
    signature = sign_payload(priv, payload_hash)
    public_key = get_public_key_hex(priv)

    bundle = {
        "version": CONTRACT_VERSION,
        "payload": base64.b64encode(payload).decode("ascii"),
        "payload_hash": payload_hash_hex,
        "signature": signature,
        "public_key": public_key,
        "alg": ALG,
    }
    with open(out_path, "w") as f:
        json.dump(bundle, f, indent=2)
    print(f"Sealed progress payment record written to {out_path}")
    print(f"Verify with: qg verify {out_path}")

def demo_record():
    return {
        "type": "progress_payment",
        "job_id": "JOB-2026-042",
        "site": "Site Alpha — Springfield, MO",
        "application_number": "PA-007",
        "period_from": "2026-10-01",
        "period_to": "2026-10-31",
        "contract_sum": 450000.00,
        "previous_payments": 125000.00,
        "current_payment_due": 67500.00,
        "retainage_percent": 5.0,
        "retainage_held": 3375.00,
        "net_due": 64125.00,
        "work_completed_description": "Completed structural steel erection for Building B columns C1-C12. Installed roof deck sections 1-4. Concrete pour for slab on grade Area 2.",
        "schedule_of_values": [
            {"item": "Structural Steel", "scheduled": 120000, "previous": 45000, "this_period": 35000, "to_date": 80000},
            {"item": "Roof Deck", "scheduled": 45000, "previous": 0, "this_period": 18000, "to_date": 18000},
            {"item": "Slab on Grade", "scheduled": 85000, "previous": 20000, "this_period": 14500, "to_date": 34500}
        ],
        "supporting_evidence": ["daily_reports_oct.json", "photos_hash_list.json", "inspector_signoff.pdf"],
        "media_hashes": ["a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456"],
        "notes": "Submitted with supporting DailySeal packs and MediaSeal hashes. Superintendent review complete.",
        "submitted_by": "Field Operator / GC",
        "submitted_at": "2026-11-05T16:00:00Z",
        "sealed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tool": "ProgressPaymentSeal/0.1.0"
    }

def main():
    parser = argparse.ArgumentParser(description="ProgressPaymentSeal — seal progress payment / pay application records into QuantumGuard packs.")
    parser.add_argument("--demo", action="store_true", help="Run demo and seal sample record")
    parser.add_argument("--json", help="Path to JSON progress payment record file to seal")
    parser.add_argument("--out", default="sealed-progress-payment.json", help="Output sealed bundle path")
    parser.add_argument("--key", default="progresspaymentseal_key.pem", help="Path to Ed25519 private key PEM")
    args = parser.parse_args()

    if args.demo:
        record = demo_record()
        print("Demo record:")
        print(json.dumps(record, indent=2))
    elif args.json:
        with open(args.json) as f:
            record = json.load(f)
    else:
        parser.print_help()
        return

    priv = load_or_generate_key(args.key)
    seal_record(record, priv, args.out)

if __name__ == "__main__":
    main()
