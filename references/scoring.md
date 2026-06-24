# CRO Scoring Rubric

## Page-Level Scores

Each page is scored across 4 dimensions. All scores are 0–100.

### AIDA Score (weight: 30%)
| Score | Meaning |
|-------|---------|
| 90–100 | Textbook execution. Every stage is handled perfectly. |
| 70–89 | Strong. One or two stages are weak but overall solid. |
| 50–69 | Average. Missing critical AIDA elements that bleed conversions. |
| 30–49 | Weak. Funnel has major holes. Visitors are leaving confused. |
| 0–29 | No visible structure. Page feels random or corporate. |

**AIDA Subscores:**
- Attention: 25 pts (first 3 seconds experience)
- Interest: 25 pts (value proposition clarity)
- Desire: 25 pts (emotional triggers, social proof)
- Action: 25 pts (CTA clarity, friction level)

### Cialdini Score (weight: 25%)
Sum of all 7 principles × max 3 pts each = max 21 raw pts → normalized to 100.

| Raw | Score |
|-----|-------|
| 18–21 | 90–100 — Highly persuasive |
| 12–17 | 60–85 — Moderately persuasive |
| 7–11 | 35–55 — Weak persuasion |
| 0–6 | 0–30 — Little to no persuasion |

### Nielsen Score (weight: 25%)
10 heuristics × max 3 pts each = max 30 raw pts → normalized to 100.

| Raw | Score |
|-----|-------|
| 26–30 | 90–100 — Excellent UX |
| 18–25 | 60–85 — Good UX with gaps |
| 10–17 | 35–55 — Noticeable friction |
| 0–9 | 0–30 — High friction, users struggle |

### 4Ps Score (weight: 20%)
Applies to the full site (not per page). Score each P from 0–25.

| P | Max Points |
|---|-----------|
| Product | 25 |
| Price | 25 |
| Place | 25 |
| Promotion | 25 |

---

## Overall Site CRO Score

```
Page scores with weights:
- Checkout (all steps): 40% of site score
- PDP (average of all PDPs): 30% of site score
- Home: 20% of site score
- PLP/Category: 10% of site score

Site CRO Score = Σ(page_score × page_weight)
```

## Score Interpretation

| Score | Rating | Business Impact |
|-------|--------|----------------|
| 85–100 | Elite | Top 5% of e-commerce. Marginal gains possible. |
| 70–84 | Strong | Above average. Focus on data-driven A/B testing. |
| 55–69 | Average | Significant room to improve. 20-40% CVR uplift likely. |
| 40–54 | Weak | Critical issues costing revenue daily. Act now. |
| <40 | Poor | Fundamental problems. Major redesign/restructure needed. |

---

## Impact Estimation Methodology

Use these benchmarks to estimate conversion impact:

### High-Impact Levers (per lever, if fixed)
| Issue | Typical CVR Impact |
|-------|------------------|
| Mobile CTA not visible above fold | +8–15% mobile CVR |
| No guest checkout option | +15–25% checkout CVR |
| Slow checkout form (>5 fields step 1) | +10–20% checkout completion |
| No product reviews | +15–30% PDP CVR |
| No free shipping communication | +5–10% AOV |
| Poor mobile experience | +20–40% if traffic is >60% mobile |
| No urgency signals | +5–12% PDP CVR |
| Confusing navigation | +5–15% engagement |
| Slow page load (>3s) | -7% CVR per additional second |
| No trust badges at checkout | +5–10% checkout completion |
| Multiple competing CTAs on PDP | +10–20% (focus = clarity) |
| Auto-playing video with sound | -5–10% (annoying, leaves) |

### AOV Levers
| Lever | Typical AOV Impact |
|-------|------------------|
| Free shipping threshold messaging | +10–20% AOV |
| Bundle offers on PDP | +15–25% AOV |
| Cart cross-sell ("frequently bought with") | +8–15% AOV |
| Post-purchase upsell (thank you page) | +5–10% revenue |
| Volume discounts | +10–30% AOV (for replenishable goods) |

---

## Priority Classification

### 🔴 Critical (Fix within 1 week)
- Checkout errors that block purchases
- Mobile breakage (buttons, forms, images)
- Missing price or ATC button
- Load time >5 seconds
- Security warnings or SSL errors
- Forms that don't work

### 🟡 High (Fix within 30 days)
- No guest checkout
- No social proof on PDP
- Confusing checkout flow
- No mobile optimization
- Poor product photography
- Hidden or unclear pricing

### 🟢 Medium (Fix within 60–90 days)
- Improve copywriting
- Add urgency signals
- Improve email capture
- Add trust badges
- Enhance navigation
- Add cross-sell/upsell

### ⚡ Quick Wins (Low effort, measurable in 7–14 days)
- Add free shipping bar to header
- Add "Only X left" to top 20 products
- Enable express checkout (Apple Pay, Google Pay)
- Add countdown timer to promotions
- Add security badge to checkout
- Display review stars next to product name on PLP
