# Coinability Policy

Use this reference for candidate analysis. It is a semantic policy; numeric scoring and final publication eligibility belong to deterministic backend code using `config/coinability.v1.json`.

## First question

Do not ask only whether the item is popular or important. Ask whether people can rapidly recognize, name, repeat, remix, and gather around a safe, compact identity derived from the item.

## Hard reject before scoring

Return `HARD_REJECT`, a matching reason, `launch_hook: null`, no RWA matches, and `no_safe_recommendation: true` for:

- war or armed conflict;
- death or serious injury;
- disaster, emergency, or active public-safety alert;
- crime victimization, serious illness, or private grief;
- exploitation of minors;
- explicit or hateful content;
- promotion of an existing token or a contract address.

Do not rescue a hard-rejected item because it has high reach, a famous author, a high provider AI rating, or an apparent RWA match.

## Human-review-only content

Political/election content, public-figure or brand rights risks, impersonation risks, copyrighted-media risks, and unverified material claims never qualify for automatic publication. Apply the appropriate risk flag and request review.

Use the `NONE` risk flag only when no other risk flag applies; never combine it with another flag.

## Eligible content classes

- `FAMOUS_PERSON_MOMENT`: an unexpected, quotable, visual, or participatory moment involving a recognized person. Routine statements do not qualify.
- `MEME_MOMENT`: an organic joke, reaction, image, clip, or format that others are independently repeating or modifying.
- `CATCHPHRASE`: a short phrase that is already being repeated, quoted, or adapted.
- `CHARACTER_OR_ANIMAL`: a visually clear subject with a recognizable identity and derivative potential.
- `SPORTS_MOMENT`: a safe, iconic celebration, performance, phrase, rivalry, or fan moment rather than injury or tragedy.
- `PRODUCT_CULTURE_MOMENT`: an object or launch that has escaped routine marketing and generated independent cultural participation.
- `COMMUNITY_CHALLENGE`: a repeatable action, format, game, or challenge with organic adoption.

`RWA_CATALYST`, `ROUTINE_PROMOTION`, `HARD_NEWS`, and `OTHER` are not automatically eligible for the Coinable Radar.

## Promotion test

Classify a release announcement, teaser, pre-save link, ticket sale, scheduled event, album/photo drop, brand campaign, or ordinary product announcement as `ROUTINE_PROMOTION` unless evidence shows an independent derivative narrative. Large fandom engagement alone is insufficient; compare with the account's normal baseline and look for independent quotes, remixes, nicknames, parodies, or cross-community adoption.

## Factor ratings

Rate each factor `NONE`, `WEAK`, `MEDIUM`, or `STRONG`:

- `narrative_compression`: can a new viewer understand the moment in one short sentence?
- `iconic_anchor`: is there one clear person, character, animal, object, action, image, or phrase?
- `remixability`: can people adapt it into jokes, captions, clips, images, or variations?
- `community_participation`: can people repeat it, take a side, imitate it, or form an identity around it?
- `emotional_charge`: is it funny, surprising, absurd, wholesome, exciting, or otherwise emotionally memorable without relying on human suffering?
- `cross_community_portability`: can it travel beyond one fandom, language, or promotional audience?
- `name_symbol_clarity`: can a short, legible name and 2–10 character symbol be derived without misrepresentation?
- `novelty`: is the narrative genuinely new rather than recycled media or a renamed duplicate?

Provide the enum labels only. Do not total the score.

## Launch hook

For `COINABLE` or `EARLY_GEM`, provide:

- one-sentence concept;
- a concrete visual anchor grounded in evidence;
- why people would remix or participate;
- at most three candidate names and uppercase symbols.

Names and symbols are creative suggestions, not ownership claims. Add rights-risk flags when a person, brand, copyrighted character, or protected media is involved. Use `launch_hook: null` for other recommendations.

## Two independent lanes

- `COINABLE_RADAR`: safe cultural moments eligible for the launch-oriented feed after deterministic thresholds and review.
- `RWA_CATALYST`: material company, issuer, market, or economic events. Preserve them for intelligence and RWA analysis, but do not place them in the Coinable Radar merely because they are important.

## RWA matching

Run RWA matching only after the semantic decision. A famous person's indirect association with a company is not enough. Every recommendation requires an enabled runtime asset, an evidence-supported `DIRECT_ENTITY` or `VERIFIED_ECONOMIC_EXPOSURE` relation, and a relevance score meeting policy. Otherwise return `NO_SAFE_RECOMMENDATION`.
