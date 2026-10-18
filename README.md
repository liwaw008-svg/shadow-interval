# Shadow Interval

The proposal arrives as a moving shadow, not a permit form.

Shadow Interval lets one person describe a temporary installation, a second person review it against a protected neighbouring use, and GenLayer validators agree on the exact part of the requested day that remains compatible. The output is deliberately narrow: `OPEN`, `TRIM`, or `CONFLICT`, a bounded interval, closed cause codes, mitigations, and references back to the three frozen input records.

## The solar sequence

1. `draft_interval` freezes the installation, protected use, requested hours, owner, and independent reviewer.
2. `screen_interval` is callable only by that reviewer. Validators compare the three records and return a fully bounded result.
3. Deterministic checks reject an `OPEN` result that trims time, a `TRIM` result shorter than 30 minutes, or a `CONFLICT` result without a cause.
4. The owner may `adopt_interval` only after a compatible screening. A draft may be cancelled before review.

The contract stores a canonical SHA-256 digest of the complete input, rejects duplicate IDs and duplicate records, and requires at least two source-slot references in every screening.

## Product boundary

This is a coordination record for low-stakes temporary uses. It is not a building permit, solar-rights certificate, engineering calculation, or personal-safety guarantee. The bundled scenario and network rehearsal are synthetic.

## Reproduce

```text
python -m pytest -q
genvm-lint lint contracts/contract.py
```

## StudioNet release

- App: [shadow-interval.pages.dev](https://shadow-interval.pages.dev/)
- Contract: [`0xbD2E7736246c2c45b5640B546424681F715Df4df`](https://explorer-studio.genlayer.com/address/0xbD2E7736246c2c45b5640B546424681F715Df4df)
- Deployment: [`0x13140fe7fa36a8d65869e28ff6a0e7ce2f4ebe91fa64a4a4e972d0975e71d2d5`](https://explorer-studio.genlayer.com/transactions/0x13140fe7fa36a8d65869e28ff6a0e7ce2f4ebe91fa64a4a4e972d0975e71d2d5)

The exact source digest and canonical lifecycle readback are recorded in `deployment.json` and `evidence/live-run.json`.
