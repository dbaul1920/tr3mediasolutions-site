# TR3 MEDIA SOLUTIONS — PIPELINE TRACKER & NETWORKING SYSTEM

---

## PART 2: PIPELINE TRACKER

### Why This Exists

You don't need a giant CRM. You need a tracker that shows:
- Who is in motion
- What kind of lead they are
- Next step
- Money potential
- Last contact date

---

### CORE COLUMNS

| Column | Type | Purpose |
|--------|------|---------|
| Name | Text | Contact name |
| Business | Text | Their company/business |
| Lead Source | Dropdown | Where they came from |
| Relationship Warmth | Dropdown | How warm the connection is |
| Opportunity Type | Dropdown | What you're selling into |
| Estimated Value | Currency | Dollar value of the opportunity |
| Current Stage | Dropdown | Where they are in your process |
| Next Step | Text | The one specific thing that happens next |
| Next Step Date | Date | When it happens |
| Last Contact Date | Date | Last time you talked or messaged |
| Notes | Long text | Context, quotes, details |
| Probability | Percent | Auto-filled or manual based on stage |
| Expected Value | Currency (formula) | Estimated Value x Probability |

---

### DROPDOWN OPTIONS

**Relationship Warmth:**
- Hot — Active conversation, mutual interest, ready to move
- Warm — Good rapport, some back-and-forth, not yet in motion
- Lukewarm — Met once, light connection, needs nurturing
- Cold — No prior relationship

**Opportunity Type:**
- Paid Audit
- Warm Intro Call
- Referral Conversation
- Networking Follow-Up
- Strategy Project
- Execution Project

**Lead Source:**
- Referral
- Networking Event
- Community Group
- Social Media (DM/Comment)
- Inbound (Website/Form)
- Existing Client
- Other

**Current Stage:**
- Identified
- Reached Out
- Conversation Scheduled
- Audit Completed
- Proposal Sent
- Verbal Yes
- Closed Won
- Closed Lost
- Nurture

---

### PROBABILITY BY STAGE

| Stage | Probability |
|-------|------------|
| Identified | 10% |
| Reached Out | 15% |
| Conversation Scheduled | 30% |
| Audit Completed | 50% |
| Proposal Sent | 60% |
| Verbal Yes | 85% |
| Closed Won | 100% |
| Closed Lost | 0% |
| Nurture | 20% |

**Expected Value Formula:** `Estimated Value x Probability`

This shows your real pipeline, not just your hopes.

---

### GOOGLE SHEETS SETUP

#### Sheet 1: Pipeline

**Headers (Row 1):**
```
A: Name
B: Business
C: Lead Source
D: Relationship Warmth
E: Opportunity Type
F: Estimated Value
G: Current Stage
H: Next Step
I: Next Step Date
J: Last Contact Date
K: Notes
L: Probability
M: Expected Value
```

**Key Formulas:**

**Probability (Column L) — auto-fill based on stage:**
```
=IFS(
  G2="Identified", 0.10,
  G2="Reached Out", 0.15,
  G2="Conversation Scheduled", 0.30,
  G2="Audit Completed", 0.50,
  G2="Proposal Sent", 0.60,
  G2="Verbal Yes", 0.85,
  G2="Closed Won", 1.00,
  G2="Closed Lost", 0.00,
  G2="Nurture", 0.20,
  TRUE, 0
)
```

**Expected Value (Column M):**
```
=F2*L2
```

**Data Validation for Dropdowns:**
- Select column C > Data > Data Validation > List of items:
  `Referral,Networking Event,Community Group,Social Media,Inbound,Existing Client,Other`
- Select column D > List of items:
  `Hot,Warm,Lukewarm,Cold`
- Select column E > List of items:
  `Paid Audit,Warm Intro Call,Referral Conversation,Networking Follow-Up,Strategy Project,Execution Project`
- Select column G > List of items:
  `Identified,Reached Out,Conversation Scheduled,Audit Completed,Proposal Sent,Verbal Yes,Closed Won,Closed Lost,Nurture`

#### Sheet 2: Dashboard

**Total Pipeline Value (all active deals):**
```
=SUMIFS(Pipeline!F:F, Pipeline!G:G, "<>Closed Won", Pipeline!G:G, "<>Closed Lost")
```

**Expected Revenue (weighted):**
```
=SUMIFS(Pipeline!M:M, Pipeline!G:G, "<>Closed Won", Pipeline!G:G, "<>Closed Lost")
```

**Closed Won Revenue:**
```
=SUMIF(Pipeline!G:G, "Closed Won", Pipeline!F:F)
```

**Leads by Stage — count per stage:**
```
=COUNTIF(Pipeline!G:G, "Identified")
=COUNTIF(Pipeline!G:G, "Reached Out")
=COUNTIF(Pipeline!G:G, "Conversation Scheduled")
=COUNTIF(Pipeline!G:G, "Audit Completed")
=COUNTIF(Pipeline!G:G, "Proposal Sent")
=COUNTIF(Pipeline!G:G, "Verbal Yes")
=COUNTIF(Pipeline!G:G, "Closed Won")
=COUNTIF(Pipeline!G:G, "Closed Lost")
=COUNTIF(Pipeline!G:G, "Nurture")
```

**Follow-Ups Due Today or Overdue:**
```
=COUNTIFS(Pipeline!I:I, "<="&TODAY(), Pipeline!G:G, "<>Closed Won", Pipeline!G:G, "<>Closed Lost")
```

**Follow-Ups Due This Week:**
```
=COUNTIFS(Pipeline!I:I, ">="&TODAY(), Pipeline!I:I, "<="&TODAY()+7, Pipeline!G:G, "<>Closed Won", Pipeline!G:G, "<>Closed Lost")
```

**Average Deal Size:**
```
=AVERAGEIFS(Pipeline!F:F, Pipeline!G:G, "<>Closed Lost", Pipeline!F:F, ">0")
```

**Conversion Rate (Closed Won / Total excluding active):**
```
=COUNTIF(Pipeline!G:G, "Closed Won") / (COUNTIF(Pipeline!G:G, "Closed Won") + COUNTIF(Pipeline!G:G, "Closed Lost"))
```

#### Dashboard Layout (Sheet 2)

```
═══════════════════════════════════════════════════════
PIPELINE DASHBOARD
═══════════════════════════════════════════════════════

KEY NUMBERS
───────────────────────────────────────────────────────
Total Pipeline Value:        [formula]
Expected Revenue:            [formula]
Closed Won Revenue:          [formula]
Active Deals:                [formula]
Average Deal Size:           [formula]
Follow-Ups Due:              [formula]

LEADS BY STAGE
───────────────────────────────────────────────────────
Identified:                  [count]
Reached Out:                 [count]
Conversation Scheduled:      [count]
Audit Completed:             [count]
Proposal Sent:               [count]
Verbal Yes:                  [count]
Closed Won:                  [count]
Closed Lost:                 [count]
Nurture:                     [count]

FOLLOW-UPS DUE THIS WEEK
───────────────────────────────────────────────────────
(Use FILTER or QUERY formula below to auto-populate)

═══════════════════════════════════════════════════════
```

**Follow-Ups Due This Week (auto-populated list):**
```
=QUERY(Pipeline!A:I, "SELECT A, B, G, H, I WHERE I <= date '"&TEXT(TODAY()+7,"yyyy-mm-dd")&"' AND G <> 'Closed Won' AND G <> 'Closed Lost' ORDER BY I ASC", 1)
```

---

### NOTION SETUP

**Database Properties:**

| Property | Type | Config |
|----------|------|--------|
| Name | Title | — |
| Business | Text | — |
| Lead Source | Select | Options: Referral, Networking Event, Community Group, Social Media, Inbound, Existing Client, Other |
| Relationship Warmth | Select | Options: Hot, Warm, Lukewarm, Cold |
| Opportunity Type | Select | Options: Paid Audit, Warm Intro Call, Referral Conversation, Networking Follow-Up, Strategy Project, Execution Project |
| Estimated Value | Number (USD) | — |
| Current Stage | Select | Options: Identified, Reached Out, Conversation Scheduled, Audit Completed, Proposal Sent, Verbal Yes, Closed Won, Closed Lost, Nurture |
| Next Step | Text | — |
| Next Step Date | Date | — |
| Last Contact Date | Date | — |
| Notes | Text (long) | — |
| Probability | Formula | `if(prop("Current Stage") == "Identified", 0.1, if(prop("Current Stage") == "Reached Out", 0.15, if(prop("Current Stage") == "Conversation Scheduled", 0.3, if(prop("Current Stage") == "Audit Completed", 0.5, if(prop("Current Stage") == "Proposal Sent", 0.6, if(prop("Current Stage") == "Verbal Yes", 0.85, if(prop("Current Stage") == "Closed Won", 1, if(prop("Current Stage") == "Closed Lost", 0, if(prop("Current Stage") == "Nurture", 0.2, 0)))))))))` |
| Expected Value | Formula | `prop("Estimated Value") * prop("Probability")` |

**Views to create:**
1. **All Leads** — Table view, sorted by Next Step Date
2. **Active Pipeline** — Table view, filtered to exclude Closed Won, Closed Lost
3. **Follow-Ups Due** — Table view, filtered to Next Step Date <= Today + 7 days
4. **By Stage** — Board view, grouped by Current Stage
5. **Won Deals** — Table view, filtered to Closed Won

---

### AIRTABLE SETUP

**Field Configuration:**

| Field | Type | Config |
|-------|------|--------|
| Name | Single line text | Primary field |
| Business | Single line text | — |
| Lead Source | Single select | Same options as above |
| Relationship Warmth | Single select | Color code: Hot=Red, Warm=Orange, Lukewarm=Yellow, Cold=Blue |
| Opportunity Type | Single select | Same options as above |
| Estimated Value | Currency (USD) | — |
| Current Stage | Single select | Color code each stage |
| Next Step | Single line text | — |
| Next Step Date | Date | — |
| Last Contact Date | Date | — |
| Notes | Long text | Enable rich text |
| Probability | Formula | Same IFS logic |
| Expected Value | Formula | `{Estimated Value} * {Probability}` |

**Views:**
1. **Grid: Active Pipeline** — Filter: Current Stage is not Closed Won/Lost
2. **Kanban: By Stage** — Stack by Current Stage
3. **Calendar: Follow-Ups** — By Next Step Date
4. **Grid: This Week** — Filter: Next Step Date is within the next 7 days

---

### YOUR CURRENT PIPELINE

| Name | Type | Stage | Next Step | Date |
|------|------|-------|-----------|------|
| Heather | Paid Audit | Conversation Scheduled | Follow-up call | April 6 |
| Julia | Warm Intro Call | Conversation Scheduled | Discovery conversation | Next week |
| Bring Your Work | Networking Follow-Up | Identified | Coaching call — positioning & accountability | April 2 |
| TechTown Event | Networking Follow-Up | Identified | Live prospecting & relationship building | April 2 |
| Wealth Walks Meetup | Networking Follow-Up | Identified | Relationship building & referral room | TBD |
| Future Wealth Walks Pairings | Referral Conversation | Identified | Warm intros & ecosystem growth | TBD |

**That is a real pipeline.** Not huge yet, but real. Two conversations in motion, four rooms to work. That's enough to hit your 5 audits/month target if you work the rooms consistently.

---

## PART 3: NETWORKING SUPPORT

### ONE-PAGE CHEAT SHEET FOR EVENTS

Print this. Keep it in your phone notes. Review it in the car before you walk in.

---

### 3 CLEAN WAYS TO DESCRIBE WHAT YOU DO

Pick one based on the room. Rotate based on who you're talking to.

**1. The Direct Version:**
> "I help business owners figure out where their marketing is wasting money — and fix it so it actually drives revenue."

**2. The Story Version:**
> "Most of my clients come to me spending money on marketing but can't tell you what's working. I help them stop guessing and start seeing a return."

**3. The Curiosity Version:**
> "I do marketing audits for business owners. I look at everything they're doing and show them exactly where they're leaking money. It's kind of like a financial audit, but for your marketing."

**Rule:** Say it in under 15 seconds. Then ask them a question. Don't monologue.

---

### 5 OPENING LINES

Use these to start real conversations, not transactional ones.

1. "What brought you to this event? Is this your first time here?"
2. "I love your [specific thing — their jewelry, bag, shirt, business card design]. Where's that from?"
3. "What do you do? And more importantly — do you actually like it?" *(Use this one sparingly. It's disarming and people love it.)*
4. "Have you been to any events like this that you actually got something out of?"
5. "I'm [Your Name]. I don't know a single person here — which is kind of the point, right?"

---

### 5 FOLLOW-UP QUESTIONS

Use these to go deeper after the opener. The goal is to get them talking about their business problems.

1. "What's working really well in your business right now?"
2. "What's the biggest thing on your plate this quarter?"
3. "How do most of your customers find you?"
4. "Are you doing anything specific for marketing, or is it mostly word of mouth?"
5. "What would make this year a great year for your business?"

**Listen for:** Marketing frustration, growth ambitions, feeling stuck, spending money without results. These are all openings.

---

### 3 CLEAN WAYS TO EXIT A CONVERSATION

Don't ghost. Don't linger. Exit with warmth and intention.

**1. The Connector Exit:**
> "I really enjoyed talking with you. Let me grab your card — I'd love to connect on LinkedIn after this."

**2. The Intentional Exit:**
> "I want to be respectful of your time and go meet a few more people. But let's definitely stay in touch — can I text you this week?"

**3. The Warm Handoff Exit:**
> "You should meet [someone else at the event]. I think you two would really get along. Let me introduce you."

---

### SAME-NIGHT FOLLOW-UP TEMPLATES

Send these the same night. Not the next day. Same night. While they still remember your face.

**LinkedIn Message:**

> Hi [Name] — it was great meeting you at [event] tonight. I really enjoyed our conversation about [specific thing you talked about]. Would love to stay connected and keep the conversation going. Let me know if there's ever anything I can help with on the marketing side.

**Text Message (if you exchanged numbers):**

> Hey [Name], this is [Your Name] from [event] tonight. Really glad we connected. Loved what you said about [specific thing]. Let's grab coffee or hop on a call sometime soon — I think there's some good overlap between what we're both building.

**If they mentioned a marketing problem:**

> Hey [Name] — great meeting you tonight at [event]. You mentioned [specific problem — e.g., "not knowing if your social media is doing anything"]. That's actually something I help business owners sort out. If you ever want a second set of eyes on it, I'd be happy to chat. No pressure — just thought of you when I got home.

---

### NETWORKING RULES FOR YOURSELF

1. **Go with a number.** Aim to have 3–5 real conversations per event. Not 15 surface-level ones.
2. **Ask more than you talk.** You learn more and they remember you better.
3. **Don't pitch.** If they ask what you do, give the 15-second version and pivot back to them.
4. **Follow up the same night.** The fortune is in the follow-up, and most people don't do it.
5. **Track every contact.** If they go in your pipeline tracker, they exist. If they don't, they don't.
6. **Bring business cards or have a clean way to share contact info.** QR code to your LinkedIn works.
7. **Dress like you're worth what you charge.** You're a creative strategist. Look the part.

---

## MONTHLY TARGETS & SCORECARD

Track these numbers monthly to know if your system is working.

```
═══════════════════════════════════════════════════════
MONTHLY SCORECARD — [Month]
═══════════════════════════════════════════════════════

ACTIVITY
───────────────────────────────────────────────────────
Networking events attended:        _____ / 4 target
New contacts added to tracker:     _____ / 15 target
Follow-up messages sent:           _____ / 20 target
Discovery conversations held:      _____
Audit calls completed:             _____ / 5 target

REVENUE
───────────────────────────────────────────────────────
Proposals sent:                    _____
Engagements closed:                _____ / 2 target
Revenue closed:                    $_____
Pipeline value added:              $_____
Expected pipeline value:           $_____

CONVERSION RATES
───────────────────────────────────────────────────────
Contact → Conversation:            _____%
Conversation → Audit:              _____%
Audit → Proposal:                  _____%
Proposal → Close:                  _____%

═══════════════════════════════════════════════════════
```

---

*Built for TR3 Media Solutions. Keep it simple. Work the rooms. Follow up same night. Close with clarity.*
