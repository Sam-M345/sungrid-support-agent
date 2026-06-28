# SunGrid Solutions — Customer Support Standard Operating Procedure (Internal)

> **Demo note:** This is a synthetic portfolio project using fictional company documents. Not real solar, warranty, safety, or financial advice.

**Document ID:** SG-SOP-2024-01  
**Effective date:** January 1, 2024  
**Audience:** Customer Support (Tier 1), AI Assist Reviewers  
**Related documents:** Warranty Policy (SG-WAR-2024-01), Installation Troubleshooting Guide (SG-TSG-2024-01), Safety Escalation Policy (SG-SAF-2024-01), Financing FAQ (SG-FIN-2024-01)

---

## 1.0 Purpose

This SOP defines how SunGrid support representatives classify inquiries, gather information, decide when to answer vs. escalate, document cases, and communicate uncertainty. AI-assisted drafts must follow the same rules as human agents.

## 2.0 Support Principles

1. **Safety first** — Any hazard signal overrides all other workflows (SG-SAF-2024-01).
2. **Ground answers in policy** — Do not invent coverage, timelines, or financial terms.
3. **Separate customer vs. internal voice** — Customer responses are plain language; internal notes are structured for CRM.
4. **Document before promising** — No commitment without ticket number or policy citation.

## 3.0 Question Classification

### 3.1 Primary Categories

| Category | Examples | Primary reference |
|----------|----------|-------------------|
| **Warranty** | “Is this covered?” “Claim status” | SG-WAR-2024-01 |
| **Troubleshooting** | Low production, app offline, error codes | SG-TSG-2024-01 |
| **Safety** | Smell, shock, exposed wires, fire | SG-SAF-2024-01 |
| **Financing** | Payments, lease, cancellation, tax credits | SG-FIN-2024-01 |
| **Multi-topic** | Production + warranty | Both SG-TSG + SG-WAR |

Classify **safety** if **any** safety keyword appears, even if the customer also asks about warranty or billing.

### 3.2 Secondary Tags

Add tags for routing: `monitoring`, `storm`, `billing-confusion`, `new-customer`, `escalated-previously`.

## 4.0 Follow-Up Questions

### 4.1 Minimum Information by Category

**Troubleshooting / warranty (non-safety):**

- Account ID or service address  
- Date issue started  
- Monitoring online? (Y/N)  
- Recent weather or storm?  
- Error codes or photos if available  

**Safety:**

- Exact location of hazard (inverter, battery, roof, conduit)  
- Active smoke/fire? (If yes → 911 script per SG-SAF-2024-01)  
- Is anyone injured?  

**Financing:**

- Loan vs. lease vs. cash (from account)  
- Contract date and PTO date  
- **Do not** discuss tax advice — use SG-FIN-2024-01 disclaimers  

### 4.2 When to Ask vs. When to Escalate First

Ask follow-ups when the situation is **low or medium risk** and information is missing.

Escalate **first** when:

- Safety trigger (Section 3.1).  
- Customer requests legal interpretation of contract.  
- Customer disputes amount owed (Financing team).  
- Three failed troubleshooting attempts on same issue (supervisor review).

## 5.0 When to Answer Directly vs. Escalate

### 5.1 Answer Directly (Tier 1)

- Explaining general policy terms with citations.  
- Walking through approved troubleshooting steps (SG-TSG-2024-01).  
- Clarifying monitoring vs. equipment failure (Section 3.1 of TSG).  
- Listing warranty claim **documentation** requirements (SG-WAR-2024-01 Section 5.0).  

### 5.2 Escalate to Specialist Queues

| Queue | When |
|-------|------|
| **Safety Dispatch** | SG-SAF-2024-01 triggers |
| **Warranty Review** | SG-WAR-2024-01 Section 6.2 |
| **Tier 2 Technical** | Persistent faults, ARC codes, dispatch decision |
| **Financing Operations** | Cancellation, credit, payment disputes, tax questions |
| **Supervisor** | Threats, legal threats, media inquiries |

### 5.3 Warranty + Troubleshooting Combined Cases

Standard path:

1. Confirm no safety issue.  
2. Complete Low Energy Output Checklist (SG-TSG-2024-01 Section 2.1).  
3. If thresholds met (SG-WAR-2024-01 Section 3.2), explain **may qualify** for review — open ticket.  
4. Internal note must list checklist steps completed.

## 6.0 Documenting the Case

Every interaction requires CRM notes with:

- Classification tags (Section 3.0)  
- Policy sections referenced  
- Customer statements (quoted briefly)  
- Actions taken and next steps  
- Escalation ticket ID if applicable  

**AI assist:** Paste internal note template — Issue type, Risk level, Confidence, Sources used, Recommended action, Escalation needed (Y/N).

## 7.0 Communicating Uncertainty

### 7.1 Approved Uncertainty Language

- “Based on the information provided, the next step is…”  
- “I can’t confirm warranty approval until Review assesses your monitoring data.”  
- “I’m not able to advise on tax credits — our Financing FAQ summarizes what’s in your agreement.”  
- “I want to make sure we keep you safe, so I’m escalating this to a specialist.”  

### 7.2 Prohibited Language

- Guarantees of coverage, savings, or repair dates not in policy.  
- Legal or tax advice.  
- DIY electrical instructions.  
- Dismissing safety reports as “probably normal.”  

### 7.3 Confidence and Risk (AI Assist)

When using AI-generated drafts:

- **High risk + safety** → Always escalate; customer message uses SG-SAF-2024-01 script.  
- **Medium risk** → Warranty/financing ambiguity, incomplete data — answer with conditions + follow-ups.  
- **Low risk** → General FAQ aligned to retrieved policy sections.  

If retrieved documents do not support a statement, **remove the statement** or escalate — never fill gaps with model knowledge alone.

## 8.0 AI Assist Workflow (Internal)

1. Rep enters homeowner question.  
2. System classifies intent and retrieves policy sections.  
3. Draft customer reply + internal note.  
4. Rep reviews, edits if needed, sends.  
5. Log sources in CRM.  

Rep remains accountable for final message. AI does not close safety tickets without human send.

---

**Document owner:** SunGrid Customer Experience  
**Last reviewed:** January 2024
