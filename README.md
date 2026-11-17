# ProgressPaymentSeal

**Local-first progress payment / pay application evidence sealer for field operators.**

Offline. Deterministic. Pay once. Compatible with QuantumGuard CONTRACT-v1, DailySeal, MediaSeal, FieldSeal, JobSeal, InvoiceSeal, and the Operator Pages suite.

## Why ProgressPaymentSeal?

Progress payments are where disputes, delays, and cash-flow problems happen most. Clients or owners challenge the amount of work completed, the supporting documentation, or the timing of the application.  

ProgressPaymentSeal captures a structured pay application (schedule of values, amounts this period, retainage, supporting evidence hashes, narrative) and seals it into a client-verifiable QuantumGuard evidence bundle.

- No SaaS. No subscription. Runs completely offline after key setup.
- Owners, lenders, or auditors verify the pack with the free QuantumGuard verifier (`qg verify`).
- Pairs with DailySeal for daily progress, MediaSeal for photo evidence, InvoiceSeal for final billing, and CloseSeal for project close-out.
- Deterministic: same inputs → same sealed pack.

## Quick Start

```bash
# Recommended for real Ed25519 signatures
pip install cryptography

python3 src/progresspaymentseal.py --demo
python3 src/progresspaymentseal.py --json samples/progress-payment-001.json --out sealed-progress-payment.json
```

Verify the output with the QuantumGuard CLI (from the quantumguard repo):

```bash
qg verify sealed-progress-payment.json
```

Expected verdict: **PASS**.

## What you can sell

| SKU       | Price | Includes                                      |
|-----------|-------|-----------------------------------------------|
| Operator  | $79   | CLI + sample templates + key setup guide + 1-year email support |
| Command   | $199  | + batch mode + HTML logger + reseller rights for client packs |
| Agency    | $499  | + white-label + multi-site key management + design partner onboarding |

Purchase / access: danpennic@gmail.com  
Or use the Operator Pages Stripe checkout flow (create a dedicated Payment Link).

Source remains free under Apache-2.0 OR MIT. Commercial Operator Pack sold separately.

## Stack Fit

- Python CLI (same family as DailySeal, SubmittalSeal, InvoiceSeal, FieldSeal)
- Emits QuantumGuard CONTRACT-v1 bundles (Ed25519, deterministic canonical JSON)
- Local key storage (PEM)
- Designed to drop into the Operator Pages field stack
- Ready for future HTML/JS logger and integration with schedule-of-values worksheets

## License

Apache-2.0 OR MIT
