# Hella Cool Features for the AURA Lab

*A brainstorm of features that very few research-lab sites have — picked
because each one signals something real about AURA's identity (efficiency,
interpretability, honest evaluation, mentorship).*

Each block has a one-line **why it's on-brand for AURA**.

---

## I. Live, in-browser proof (the lab as a working artifact)

1. **Run-Our-Model-In-Your-Browser**
   A WebGPU/ONNX widget lets visitors paste a code snippet and run the lab's
   latest distilled code-summarization model **on their own device**, with a
   real-time meter showing parameters, memory, latency, and energy used.
   *Why AURA:* the entire point of the efficiency thread is "small enough to
   deploy at developer scale" — prove it by running on the visitor's laptop.

2. **Reproduce-In-Browser**
   Each paper has a "▶ reproduce key results" button that loads a WASM-Python
   notebook in the browser and reruns the headline figure live.
   *Why AURA:* reproducibility as a first-class affordance, not a footnote.

3. **Interpretability Sandbox**
   Type code → see the lab's interpretability tool highlight which tokens the
   model "attended to" while producing its output. Swap models, change inputs.
   *Why AURA:* makes the *U* of A·U·R·A inspectable, not just claimed.

4. **LLM-as-a-Judge Calibration Game**
   Visitors rate 5 pairs of model outputs. The page reveals how their ratings
   compare to (a) the lab's gold labels, (b) GPT-4-as-Judge, (c) Claude. A
   running scoreboard shows where humans and judges disagree.
   *Why AURA:* turns the lab's TSE paper into a participatory experience.

---

## II. Receipts & provenance (anti-hype credibility)

5. **Hyperlinked Claims**
   Every factual sentence in the homepage carries a tiny footnote glyph; clicking
   opens the paper + figure + page where the claim is supported. A counter in the
   footer reads "47 claims · 47 with receipts."
   *Why AURA:* makes "honest evaluation" a property of the homepage itself.

6. **Version-Tracked Site (git-backed)**
   Hover any sentence → see the commit hash, author, and date it was last
   touched. A slider at the bottom lets visitors scrub through past versions.
   *Why AURA:* the site practices the openness it preaches.

7. **The Retractions & Errata Log**
   A small public log of "what we said that turned out to be wrong, and how
   we corrected it." Linked from the footer of every paper card.
   *Why AURA:* almost no lab does this. Doing it is a stronger signal than any
   award.

8. **The "What We Don't Yet Know" Wall**
   A continuously updated list of open questions the lab is actively chasing
   but hasn't answered. Updated when papers ship.
   *Why AURA:* honesty as identity.

---

## III. Mentorship made visible (the real differentiator for new PhDs)

9. **The PhD Onboarding Open-Source Kit**
   The lab's actual onboarding doc: week-by-week reading list, recommended
   tools, the "first paper" walkthrough. Released as a public repo with MIT
   license.
   *Why AURA:* mentorship as method, made tangible. Recruits self-select.

10. **Student-Led Long-Form Posts**
    Every PhD student publishes one signed long-form post per semester
    (research diary, paper retrospective, "I tried X and it didn't work"). The
    homepage features the most recent.
    *Why AURA:* puts students at the center, not in a roster.

11. **Mentor Tree / Academic Genealogy**
    A clickable family tree showing Antonio's advisors, his collaborators, and
    his students. Each node opens a mini-bio + their best 3 papers.
    *Why AURA:* makes the intellectual lineage navigable.

12. **Open Office-Hours Bot**
    A small Q&A widget trained on the lab's public material answers
    prospective-student questions ("what background do I need?", "what
    machines do you have?", "what's a typical first paper?").
    *Why AURA:* uses the lab's own technology to serve its applicants.

---

## IV. Operations transparency (rare and powerful)

13. **Compute / Energy Dashboard**
    Live(ish) tracker of GPU-hours and kWh spent this quarter, plotted
    against the lab's self-imposed budget. "We will keep paper-X under 5 kWh."
    *Why AURA:* puts the efficiency thread on a public scoreboard.

14. **Open Peer-Review Archive**
    When papers get accepted, the lab anonymizes and publishes the reviews
    plus the rebuttal, alongside the camera-ready.
    *Why AURA:* teaches the field how peer review actually works, and shows
    the lab's responses are good-faith.

15. **Funding Ledger**
    Every grant, every dollar, mapped to outputs (papers, talks, students).
    *Why AURA:* radically transparent — and short to write because the lab
    has one NSF CRII and is just starting out.

16. **Submission Tracker (Kanban)**
    Public board: drafting → submitted → under review → revisions → accepted.
    No paper titles until accepted, but counts and venues visible.
    *Why AURA:* demystifies the publication pipeline.

---

## V. Community & teaching (positioning the lab as a steward)

17. **AURA Reading Group · public feed**
    Weekly paper-of-the-week with a 200-word lab commentary. Public RSS feed.
    *Why AURA:* claims a stewardship position in the SE+AI community.

18. **Code-Summarization Public Leaderboard**
    Host a leaderboard for code summarization using the lab's evaluation
    methodology. Other groups can submit; the lab keeps the rules honest.
    *Why AURA:* the LLM-as-a-Judge research becomes a community good.

19. **Searchable Lecture Archive**
    Every keynote, guest lecture, IEEE column, and reading-group recording —
    embedded, with full transcripts. Click any line of the transcript to play
    that moment of video.
    *Why AURA:* makes the panorama actually navigable, not a list.

20. **Annotate-Our-Papers Club**
    Hypothes.is layer over every lab PDF. Readers leave inline comments;
    Antonio replies to the thoughtful ones, monthly.
    *Why AURA:* invites the field to argue with the lab in public.

---

## VI. Recruitment pipeline (the recruiting page that recruits)

21. **"Working Trial" Application Path**
    Applicants do a 2-week, scoped, paid mini-project (graded against a public
    rubric) before formal interview. Lowers mismatched admits dramatically.
    *Why AURA:* matches lab values — rigor, evidence, honest evaluation.

22. **Public Application Kit**
    Sample statement, CV template, the actual interview question bank, a
    rubric. Removes guesswork; widens the applicant pool.
    *Why AURA:* signals fair treatment of all applicants.

23. **Undergrad Pipeline Map**
    Clear stepwise path: take CSCI 426 → submit a 1-pager → join reading group
    → first co-author paper. Each step has a deadline and an example.
    *Why AURA:* turns undergraduate mentorship into a visible asset.

---

## VII. Signaling-rich and whimsical (1–2 of these go a long way)

24. **Per-Paper Vital Signs**
    Each paper card has a tiny dashboard: citations/month pulse, mentions
    EKG, downloads heartbeat. The papers look *alive*.

25. **Weekly Whiteboard Photo**
    A literal photo of the lab's whiteboard from the past week, uploaded each
    Friday. Captioned in two sentences by whichever student wrote on it.

26. **Reverse-Q&A · "questions we ask ourselves"**
    Instead of an FAQ, a section titled *Questions we ask ourselves and don't
    have answers to.* Updated when the lab figures something out (then it
    moves to the publications list).

27. **Knowledge-Graph Side-Quest**
    A subtle, link-able sidebar that visualizes every page's neighbours in
    the lab's idea graph (papers, threads, methods). Visitors can wander
    without using the nav.

---

## Recommended starter set (low effort, high signal)

If you want to ship something this semester:

- **9 — PhD Onboarding Kit** (one weekend of writing; massive recruiting impact)
- **5 — Hyperlinked Claims** (footnote-style citations on the homepage)
- **17 — Reading Group public feed** (one Markdown post per week)
- **2 — Reproduce-In-Browser** (one paper, one button — proves the pattern)
- **8 — "What We Don't Yet Know" wall** (a single page; revisited quarterly)

These five together give you a homepage that **demonstrably** lives the values
the lab claims, before you write a single new paper.

---

*Brainstorm by — Cowork, May 2026. Pick the three that feel most yours; I'll
turn them into HTML mockups.*
