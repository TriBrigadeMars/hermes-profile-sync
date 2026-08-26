# Ballotpedia deterministic style-lint report

- Source: `examples/sample_input.txt`
- Context: `news`
- Candidate findings: **11**

> This is a lexical/mechanical preflight, not a neutrality certification. Hermes must review context, structure, attribution, due weight, and sources.

| Line | Severity | Match | Rule | Recommendation |
|---:|---|---|---|---|
| 1 | MUST FIX | `far-right` | Ballotpedia Style Guide: Right-wing, rightist, far-right | Ballotpedia says not to use these labels to describe a person's political ideology; describe affiliation, voting history, and issue stances instead. Replace the label with specific, sourced political affiliation or issue-position information. |
| 1 | MUST FIX | `bi-partisan` | Ballotpedia Style Guide: Bipartisan | Ballotpedia uses 'bipartisan', not 'bi-partisan'. bipartisan |
| 1 | MUST FIX | `67 percent` | Ballotpedia Style Guide: Percent | Use the % sign with a numeral, with no space. Replace 'N percent' with 'N%'. |
| 3 | MUST FIX | `Many experts say` | Ballotpedia bias taxonomy: Weasel words | This is vague attribution. Identify the experts/source and provide evidence. Name the source(s) and attribute the claim specifically. |
| 3 | MUST FIX | `is comprised of` | Ballotpedia Style Guide: Comprised of, composed of | Ballotpedia recommends 'composed of', 'made up of', or a correct 'comprises' construction rather than 'comprised of'. Use 'composed of', 'made up of', or '[whole] comprises [parts]'. |
| 1 | SHOULD FIX | `Yesterday` | Ballotpedia Style Guide: Today, tomorrow, tonight; BP News best practices | Ballotpedia prefers specific dates to relative time markers because content may be read later. Replace the relative time marker with the specific date when known. |
| 1 | SHOULD FIX | `12` | Ballotpedia Style Guide: Numerals | Spell out a number at the beginning of a sentence. (Years are a separate exception.) Spell out the number or revise the sentence so it does not begin with the numeral. |
| 1 | NEEDS CONTEXT | `noted` | Ballotpedia Style Guide: Factive verbs; Ballotpedia bias taxonomy: Factive verbs | This verb can presuppose the truth of the attributed claim. It is acceptable for verifiable facts but may bias disputed opinions or narratives. If the claim is disputed/opinion, consider 'said', 'stated', or 'wrote'. |
| 1 | NEEDS CONTEXT | `clearly` | Ballotpedia bias taxonomy: Editorializing / Loaded language / Inappropriate descriptors | This adverb may insert the writer's judgment rather than letting the sourced facts establish the point. Remove it or replace it with the specific evidence that makes the conclusion supportable. |
| 1 | NEEDS CONTEXT | `gun rights` | Ballotpedia Style Guide: Firearms, guns | The guide identifies these firearms-policy phrases as speech-tribe or disfavored shorthand, subject to quotation/legal-term context. Describe the specific firearm policy or legal requirement; quote legal/source terminology when necessary. |
| 3 | NEEDS CONTEXT | `adviser` | Ballotpedia Style Guide: Adviser, advisor | Ballotpedia prefers 'advisor', but an official title may retain its official spelling. Use 'advisor' unless reproducing an official title. |
