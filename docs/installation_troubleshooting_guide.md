# SunGrid Solutions — Installation Troubleshooting Guide (Internal)

> **Demo note:** This is a synthetic portfolio project using fictional company documents. Not real solar, warranty, safety, or financial advice.

**Document ID:** SG-TSG-2024-01  
**Effective date:** January 1, 2024  
**Audience:** Customer Support, Tier 1 Technical Support  
**Related documents:** Warranty Policy (SG-WAR-2024-01), Safety Escalation Policy (SG-SAF-2024-01), Customer Support SOP (SG-SOP-2024-01)

---

## 1.0 Purpose

This guide provides standardized troubleshooting steps for common post-installation issues. Complete applicable sections **before** recommending warranty review or a truck roll. If any step indicates a safety hazard, **stop** and follow SG-SAF-2024-01 — do not continue remote troubleshooting.

## 2.0 Low Energy Output

### 2.1 Low Energy Output Checklist

Work through in order. Document each step in the case notes.

1. **Confirm monitoring is online** — See Section 3.0. A offline monitor does not prove low production.
2. **Compare to expected model** — Pull site expected production from the SunGrid portal (account → Production → Expected vs. Actual).
3. **Check for shading** — New tree growth, chimney shadow, or construction next door? Note time-of-day patterns.
4. **Weather normalization** — Review last 60–90 days vs. prior year if available. Single rainy weeks are not defects.
5. **Soiling** — Pollen, dust, or bird activity in customer region? Recommend gentle rinse only if **safe roof access**; never ask customer to climb roof.
6. **Inverter status** — Online? Any fault codes? See Section 4.0.
7. **Recent storms** — See Section 5.0.
8. **Utility curtailment / export limits** — Confirm program enrollment did not change export caps.

If output remains **>20% below expected** for 60+ days after steps 1–8, see Warranty Policy Section 3.2 for review criteria.

### 2.2 Customer-Facing Explanation (Low Output)

Explain that solar production varies by season and weather. Offer to review monitoring data together. Avoid guaranteeing a specific kWh month-over-month unless citing the production model.

## 3.0 Monitoring App and Data Issues

### 3.1 App Not Showing Production Data

A blank or stale app **does not automatically mean** the solar system is broken. Common causes:

| Cause | Support action |
|-------|----------------|
| Wi-Fi or gateway offline | Walk customer through gateway LED status (green = normal) |
| App login / wrong site | Verify account email and site selection |
| Firmware update in progress | Wait 24 hours; escalate if still offline |
| Inverter communicating but portal lag | Up to 4-hour reporting delay is normal |
| Inverter fault | Check Section 4.0; may need technician |

**Key message:** “Loss of app data is often a communication issue. We’ll check whether your inverter is producing before assuming equipment failure.”

### 3.2 When Monitoring Loss Requires Technician Visit

Schedule Tier 2 remote diagnostics first. Dispatch a technician if:

- Gateway offline >72 hours after basic resets (power-cycle gateway only — **not** main service panel unless qualified).
- Inverter shows fault codes persisting after Section 4.1 steps.
- Production is zero on inverter display **and** communication is healthy.

## 4.0 Inverter Alerts and Error Codes

### 4.1 General Reset Guidance

**Before any reset:** Confirm no safety symptoms (smell, smoke, sparking, heat, exposed conductors). If present → SG-SAF-2024-01 immediately.

For **non-safety** communication or recoverable faults:

1. Photograph inverter display (customer or video call).
2. Note exact error code (e.g., `COMM-07`, `GRID-12`, `ARC-01`).
3. Check storm date if customer mentions recent weather (Section 5.0).
4. **Approved remote step:** Power-cycle inverter per manufacturer label (DC disconnect off → wait 60 seconds → on). Only if customer confirms clear access and no hazard.

**Do not** instruct customers to open inverter covers, touch bus bars, or reset main breakers.

### 4.2 Post-Storm Error Codes

After verified storm or grid outage:

- `GRID-12` (grid voltage abnormal): Often clears after utility stabilizes; wait 24 hours, one approved power-cycle.
- `COMM-07` (communication): Usually gateway/Wi-Fi; Section 3.1.
- `ARC-01` (arc fault): **Do not** repeated reset. Escalate to Tier 2 same day — potential safety review per SG-SAF-2024-01 Section 3.4.

### 4.3 When Not to Reset

Never recommend reset when:

- Burning odor, buzzing with heat, or visible damage.
- Customer reports shock or tingling.
- Error code is `ARC-01` or repeated `ISOL-05` (isolation fault).
- Water ingress visible on equipment.

## 5.0 Shading, Weather, and Storm Checks

### 5.1 Shading and Seasonal Effects

Document shade source and hours affected. Shading remediation is **not** a warranty item unless install error is documented by Site Audit.

### 5.2 Recent Storm Protocol

If customer reports storm within last **14 days**:

1. Ask about visible damage (modules cracked, conduit pulled, roof leaks).
2. Ask if utility reported outages.
3. Check portal event log for grid trips.
4. If **physical damage or roof leak** → Safety Escalation Policy Section 4.6 (roof damage) and dispatch inspection.

Storm-related production dips without equipment damage typically resolve within one clear week — not warranty alone.

## 6.0 Technician Visit Criteria

Dispatch field service when:

| Priority | Condition |
|----------|-----------|
| **Emergency** | Any SG-SAF-2024-01 trigger |
| **High** | Zero production + confirmed inverter fault >48 hrs |
| **Medium** | Persistent error after one approved reset + Tier 2 review |
| **Standard** | Monitoring hardware replacement, non-urgent comms fix |

Support cannot waive dispatch fees on out-of-warranty service; refer to account contract.

## 7.0 Escalation Summary

- **Safety** → SG-SAF-2024-01 (immediate).
- **Warranty** → SG-WAR-2024-01 Section 6.2 after checklist complete.
- **Financing / billing** → SG-FIN-2024-01 (not technical support).
- **Uncertainty** → Customer Support SOP Section 4.3.

---

**Document owner:** SunGrid Technical Support  
**Last reviewed:** January 2024
