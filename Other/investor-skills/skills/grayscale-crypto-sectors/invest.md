---
version: alpha
name: Grayscale Crypto Sectors
slug: grayscale-crypto-sectors
aliases:
  - Grayscale
  - Grayscale Research
  - Crypto Sectors
  - FTSE Grayscale
  - ZCSH
description: Sector taxonomy, FTSE/Grayscale index eligibility, fee/usage fundamentals, sector-share valuation, and institutional wrappers for digital assets
investor: Grayscale Research / Grayscale Investments
style: crypto+research+index+institutional
timeHorizon: months-years
decisionCadence: quarterly
assetClasses:
  - crypto
  - crypto ETPs
circleOfCompetence:
  - crypto sector classification
  - index eligibility and investability
  - blockchain fee/usage fundamentals
  - sector-share valuation
  - ETP/trust market structure
  - privacy as a monetary property
universe:
  geographies:
    - global crypto markets
    - US-listed crypto products
  sectors:
    - Currencies
    - Smart Contract Platforms
    - Financials
    - Consumer and Culture
    - Utilities and Services
    - Artificial Intelligence
  instruments:
    - spot tokens
    - sector indexes
    - single-asset trusts
    - spot ETPs
  marketCap: index floors from $50M-$200M by sector and status
  liquidity: required
  dataRequirements:
    - sector market cap and circulating supply
    - active addresses, transactions, fees
    - exchange listings and ADTV
    - product NAV and premium/discount when a wrapper is involved
marketRegime:
  preferred: institutionalization, regulatory clarity, theme rotation inside a classified sector
  avoid: unclassifiable memes, no-custody/no-listing names, narrative-only privacy with collapsing shielded usage
  posture: evidence-first, sector-relative, wrapper-aware
signals:
  classification:
    primaryUseCase:
      weight: high
      frequency: quarterly
      source: project docs, on-chain activity, Grayscale/FTSE sector assignment
      description: One primary Crypto Sector. Mutual exclusivity matters more than a clever multi-label.
  fundamentals:
    feeRevenue:
      weight: high
      frequency: quarterly
      source: on-chain fees
      description: Hardest-to-manipulate analog to revenue. Exception: Bitcoin, judged as monetary commodity more than fee business.
    usersAndTransactions:
      weight: high
      frequency: quarterly
      source: active addresses and transaction counts
      description: Imperfect user proxy. Judge trend vs speculative wash, not one-week spikes.
    adoptionQuality:
      weight: high
      frequency: monthly
      source: use-case-specific activity
      description: For privacy coins, shielded supply and shielded transaction share. For apps, retention and fee quality.
  valuation:
    sectorShare:
      weight: high
      frequency: weekly
      source: token market cap / Crypto Sector market cap
      description: Ask what a modest, plausible share of the assigned sector would imply. Do not require replacing Bitcoin.
    supplyInflation:
      weight: medium
      frequency: monthly
      source: issuance, unlocks, halving schedules
      description: High inflation or heavy unlocks can cancel an otherwise clean use-case story.
  catalysts:
    institutionalAccess:
      weight: high
      frequency: event-driven
      source: ETP filings, custody, listings, legislation
      description: Trust-to-ETF conversion, generic listing standards, market-structure bills, and qualified custody.
    themeCatalyst:
      weight: medium
      frequency: quarterly
      source: Grayscale outlook and sector quarterlies
      description: Privacy, tokenization, stablecoins, staking, sustainable fees, AI rails.
  product:
    wrapperGap:
      weight: high
      frequency: daily
      source: NAV vs market price
      description: Closed trusts can trade at large premiums or discounts. ETF-style AP arbitrage is supposed to collapse that gap.
filters:
  classifiableUseCase: required
  indexOrAccessEligible: required
  evidenceNotNarrativeOnly: required
  riskDefined: required
  memeWithNoSectorJob: disqualifier
  custodyOrListingImpossible: disqualifier
  wrapperConfusedWithThesis: disqualifier
sizing:
  maxPosition: satellite / theme overlay, volatility-adjusted
  maxPortfolio: do not let one alt-sector name dominate a monetary sleeve
  convictionThreshold: high
  scalingRule: add only if usage and sector-share math both improve; do not pyramid on filing headlines alone
risk:
  stopLoss: thesis-based
  maxDrawdown: model-aware; privacy and app-layer names are higher-vol than BTC
  correlationLimit: avoid stacking several tokens that are the same sector beta
  leverage: none unless the user already defined a risk budget
  positionCutRule: exit if primary use case, eligibility, or usage evidence breaks
metrics:
  sectorShare:
    frequency: weekly
    alert: share thesis no longer has a plausible path, or price already discounts the bull share
  feeAndUsageTrend:
    frequency: monthly
    alert: users, transactions, or fees roll over with no structural explanation
  wrapperGap:
    frequency: daily
    alert: premium/discount widens instead of converging after an uplist
  regulatoryAccess:
    frequency: event-driven
    alert: exchange delistings, enforcement, or failed ETP path
playbooks:
  decisionMemo:
    verdictOptions: "Overweight Sector / Single-Name Research / Watch / Wrapper Trade / Pass / Too Hard"
    requiredSections: sector,eligibility,fundamentals,sector-share,wrapper,risk,invalidation
sources:
  - "Zcash: Financial Privacy in the Age of AI (Grayscale, updated 2026-03-27): https://research.grayscale.com/reports/zcash-financial-privacy-in-the-age-of-ai"
  - "2026 Digital Asset Outlook: Dawn of the Institutional Era: https://research.grayscale.com/reports/2026-digital-asset-outlook-dawn-of-the-institutional-era"
  - "Zcash has something Bitcoin does not (The Stack): https://www.grayscale.com/the-stack/zcash-has-something-bitcoin-does-not"
  - "FTSE Grayscale Crypto Sector Index Series Ground Rules (June 2026): https://www.lseg.com/content/dam/ftse-russell/en_us/documents/ground-rules/ftse-grayscale-crypto-sector-index-series-ground-rules.pdf"
  - "Grayscale Zcash Trust product page: https://www.grayscale.com/crypto-products/grayscale-zcash-trust"
  - docs/reading-list.md
  - docs/podcast-list.md
  - docs/youtube-list.md
---

# Grayscale Crypto Sectors

Grayscale does not pick crypto like a stock-picker hunting tenbagger stories. It first puts every token in a use-case sector, then asks whether that token is investable enough for an index or product, whether usage/fees confirm the use case, and whether the market is still treating a real monetary or application property as a rounding error.

Zcash is the worked example. The published thesis is not "ZEC replaces BTC." It is: Bitcoin made digital scarcity credible, not digital privacy; privacy is a normal property of money; ZEC is still a tiny share of the Currencies Crypto Sector relative to that optionality.

## Philosophy

1. **Classify before you value.** A currency, a smart-contract platform, and an application token are different jobs. Scoring ZEC like a fee-max L1, or SOL like a store of value, is a process error.
2. **Investability is a filter, not a vibe.** Listings, liquidity, custody, and legal classification decide whether institutions can own it. Grayscale's own products exist because most allocators will not self-custody.
3. **Fees are the cleanest fundamental.** Users and transactions matter, but fees are harder to fake and more comparable across chains. Bitcoin is the main exception: treat it as a scarce monetary commodity.
4. **Value against sector share.** If a name is 0.3% of its sector and a 5% share is even plausible, the upside is in the share-capture math, not in a 100x narrative.
5. **The wrapper is not the asset.** A trust premium, an S-3 amendment, or an affiliate contribution can change access and near-term flows. It does not replace usage evidence.

## Universe & Regime

- **Asset classes**: spot crypto and US-style crypto products (trusts, ETPs).
- **Sectors** (FTSE/Grayscale, six as of 2026):
  - **Currencies**: store of value, medium of exchange, unit of account. Includes standard monetary protocols and privacy-preserving money. ZEC lives here.
  - **Smart Contract Platforms**: general-purpose programmable base layers.
  - **Financials**: on-chain financial services, payments, exchange tokens.
  - **Consumer and Culture**: NFTs, games, social, consumption apps.
  - **Utilities and Services**: oracles, interoperability, compute/storage, wallets, ads infra.
  - **Artificial Intelligence**: protocols whose primary use case is AI.
- **Index cadence**: quarterly reviews in March, June, September, December. Data cut-off is month-end before the review month; implementation after the third Friday of the review month. No intra-quarter additions.
- **Preferred regime**: regulatory clarity, ETP plumbing, and theme rotation where usage is rising inside a classified sector.
- **Avoid**: unclassifiable memes, names that fail custody/listing/legal screens, or privacy theses whose shielded usage is falling.
- **Posture**: quarterly research, satellite sizing, wrapper-aware.

## Signals

### 1. Sector classification

- **primaryUseCase** (high): What job does this asset actually do? Grayscale plus FTSE/DAR assign one primary sector and keep sectors mutually exclusive when possible. If the primary use is unclear, the name is Too Hard.

### 2. Index eligibility

Use the public FTSE Grayscale Ground Rules as the investability checklist, then say whether the name is Broad-index eligible, Investible-index eligible, or product-only.

- **Universe**: FTSE DAR vetted pricing universe, then Grayscale sector lists.
- **Exclusion list**: wrong primary use, not representative of the sector, better fit elsewhere, or insufficient data.
- **Access list** (investible products): trading/access, qualified custody, and legal/regulatory viability. All three must pass.
- **Market-value floors for new non-benchmark names**: Currencies and Smart Contract Platforms $200M; AI, Consumer & Culture, Financials, Utilities & Services $100M. Benchmark-asset floor is lower ($50M new / $40M existing).
- **Liquidity**: existing-universe names need roughly $250K ADTV to enter and $200K to stay; new universe entrants need a higher $500K ADTV screen.
- **Weights**: Broad sector indexes use square-root market-cap weights to reduce BTC/ETH dominance. Some total-market and investible indexes use full market-cap weights; the Smart Contract Platforms Investible Index caps any name at 30%.

### 3. Fundamentals

Grayscale's public quarterlies treat blockchains as measurable economies, not businesses:

- **users**: active addresses as a noisy user proxy
- **transactions**: economic throughput, net of wash and spam
- **fees**: the preferred "revenue" analog

For privacy money, add shielded supply share and shielded transaction share. Narrative without those two is not enough.

### 4. Sector-share valuation

Worked Grayscale math from the March 2026 Zcash note, using their then-current snapshot:

- Currencies Crypto Sector ≈ $1.6T, ~15 assets
- Bitcoin ≈ 90% of that sector
- ZEC ≈ $4B, or about 0.3% of the sector
- If ZEC captured 5% of the same sector, the implied value was about 18x

Refresh the numbers live. Keep the method: `implied upside ≈ (plausible sector share / current sector share) - 1`, then haircut for inflation, dilution, and execution. Do not require a Bitcoin-replacement story.

### 5. Catalysts and wrapper

- **Research catalysts**: upgrades that make the use case usable (for ZEC: wallet/shielded UX, Tachyon, Crosslink, mining/institutional infrastructure).
- **Access catalysts**: generic listing standards, market-structure legislation, spot ETP filings, authorized-participant creation/redemption.
- **Wrapper gap**: Grayscale's Zcash Trust historically traded OTC as ZCSH with premiums up to 240% and discounts down to 55% (Oct 2021–Jun 2026). An NYSE Arca listing plus AP arbitrage is supposed to pin price to NAV. Until that mechanism is live, treat ZCSH as a closed-end wrapper, not as spot ZEC.

## Filters

- **classifiableUseCase** (required): one primary sector, stated in one sentence.
- **indexOrAccessEligible** (required): passes listings/liquidity/custody/legal, or there is a credible path. Otherwise Pass.
- **evidenceNotNarrativeOnly** (required): at least one usage series confirms the job (fees, active addresses, shielded share, TVL with fee quality, etc.).
- **memeWithNoSectorJob** (disqualifier): attention without a classified use case.
- **custodyOrListingImpossible** (disqualifier): institutions cannot hold or trade it.
- **wrapperConfusedWithThesis** (disqualifier): the only bull point is "ETF soon."

## Analysis

### 1. Assign the sector

- What is the primary job: money, platform, financial app, consumer app, infra, or AI?
- Who are the real sector peers? For ZEC: BTC and other monetary/privacy currencies, not every alt.

### 2. Run eligibility

- Is it in the FTSE DAR universe?
- Does it clear the sector market-cap floor and ADTV screen?
- Can it be listed, custodied, and legally held?
- If no, the research idea may still be interesting, but it is not a Grayscale-style product/index holding.

### 3. Read the fundamentals

- Users, transactions, fees: level, trend, and quality.
- For ZEC, prefer shielded supply % and shielded tx % over headline price.
- Ask whether the latest quarter is a usage regime or a speculative wash.

### 4. Do the sector-share math

- Current share of the assigned sector.
- A modest bull share that does not require becoming Bitcoin.
- What must be true for that share to be plausible (usage, access, regulation).
- What the market already prices.

### 5. Separate theme, name, and wrapper

- Theme: privacy needed as chains go mainstream; dollar-debasement demand for scarce digital money.
- Name: ZEC as optional-privacy base-layer money with viewing keys, not Monero-style default opacity and not a mixer bolt-on.
- Wrapper: ZCSH S-3 / NYSE Arca path, CoinDesk Zcash Price Index, Coinbase Custody, BNY Mellon admin, possible DCG-affiliate in-kind contribution. Nonbinding affiliate talk is a flow headline, not proof of thesis.

### 6. Write invalidation before size

If usage, eligibility, or the sector-share premise breaks, stand down even if the chart is up.

## Position Sizing

- **Core sleeve**: BTC/ETH-style monetary or platform beta. Grayscale treats these as the institutional default.
- **Satellite / theme**: ZEC-like names. Higher volatility, smaller weight, explicit invalidation.
- **Initial size**: only after sector, eligibility, and usage pass.
- **Add rule**: add when shielded/usage share and institutional access both improve, not when a filing prints.
- **Wrapper size**: if buying ZCSH instead of ZEC, size the NAV gap as a separate bet. A 50% discount can close on uplisting; a 200% premium can also close.
- **Cash/pass**: valid. Most tokens fail classification or eligibility.

## Risk Management

- **Primary risk**: treating a classified-sector option as a confirmed share-take, or treating a product filing as demand.
- **Regulatory risk**: privacy coins can lose listings even with viewing keys. Viewing keys reduce, they do not erase, VASP/Travel Rule/MiCA friction.
- **Protocol/execution risk**: ambitious upgrades (Tachyon, Crosslink, pool migrations) can slip or introduce new failure modes. The 2026 Orchard issue and Ironwood response belong in the file.
- **Legacy crypto risk**: older ZEC shielded pools still carry trusted-setup history; Orchard/Halo removed that for the new pool.
- **Quantum**: Grayscale's 2026 outlook calls this a near-term red herring for prices, and a long-horizon design issue for almost all chains.
- **Correlation**: do not stack ZEC + XMR + DASH + DCR as four independent ideas. That is one privacy-money bet.
- **Leverage**: default none.

## Execution

### Entry Rules

1. Primary sector is clear.
2. Eligibility or a dated access path is clear.
3. Usage confirms the job, or the discount to a modest sector share is extreme and usage is at least stable.
4. Wrapper gap is measured if the instrument is not spot.
5. Invalidation is written down.

### Exit Rules

1. The use case is no longer the primary job.
2. Eligibility breaks: delisting, custody loss, legal dead-end.
3. Usage evidence rolls over with no repair path.
4. Price already discounts the bull sector share and the remaining bid is only narrative.
5. A better same-sector expression appears with cleaner access.

## Monitoring

- **Cadence**: quarterly with the FTSE/Grayscale review; weekly for sector share and wrapper gap; event-driven for filings and protocol incidents.
- **Metrics**: sector share, fees, active addresses, shielded supply/tx share, ADTV, NAV gap, filing status.
- **Alerts**: delisting, exploit/inflation bug, failed upgrade, S-3 withdrawal, affiliate deal collapsing into zero, premium blowing out.

## Playbooks

### Decision Memo

Return one of: Overweight Sector / Single-Name Research / Watch / Wrapper Trade / Pass / Too Hard.

```md
# Decision Memo: [Asset]

## Verdict

## One-Line Thesis

## Sector And Peers

## Eligibility

## Usage / Fees

## Sector-Share Math

## Wrapper / Access

## Risks / Invalidation

## What To Monitor

## Missing Data
```

### Zcash file, as of the latest public Grayscale materials

Use this as the canonical application, then refresh live numbers.

**Thesis.** Privacy is part of what makes money work. AI plus public-chain transparency plus institutional rails should raise demand for confidential settlement. ZEC is Bitcoin-like money (21M cap, PoW) with optional shielded transfers that hide sender, receiver, and amount, plus viewing keys for selective disclosure. The market still prices that as a rounding error inside Currencies.

**What Grayscale emphasized (March 2026 note).**

- Third privacy wave: digitized banking, then internet/Patriot Act, now stablecoins + AI surveillance.
- Privacy category historically lost distribution because it created exchange/wallet friction. That is a commercial problem, not proof the demand is fake.
- ZEC is an optionally private base layer, not a mixer on a transparent chain and not default-private Monero.
- Usability path: Sapling (2018) -> Orchard/Halo 2 and no trusted setup for the new pool (2022) -> unified addresses / Zodl (Zashi) shielded-first wallet, NEAR Intents swaps, CrossPay.
- Watch list: Tachyon (shielded scaling), Crosslink (PoW plus finality), shielded assets beyond native ZEC, Foundry institutional mining.
- As of 2026-03-16: shielded transactions ~86.5% of count; shielded supply ~5.16M ZEC, ~31.1% of circulating supply.
- Valuation snapshot then: $4B, 0.3% of a $1.6T Currencies sector; 5% share implied ~18x. Not a replace-Bitcoin bet.

**2026 outlook placement.** Theme #1 (dollar debasement: BTC, ETH, ZEC) and Theme #5 (privacy as chains go mainstream: ZEC, Aztec, Railgun, plus ETH/SOL confidential-transfer rails).

**Q4 2025 sector quarterly.** Privacy was the winning theme while all six sectors printed negative returns. ZEC led; XMR, DASH, DCR, BAT, BDX also showed up. Grayscale explicitly warned that mindshare and usage both rose — do not confuse the two.

**Product layer (Aug 2026).** Grayscale filed S-3 Amendment No. 4 to list ZCSH on NYSE Arca, tracking the CoinDesk Zcash Price Index, with 10,000-share baskets and an AP arbitrage path. DCG International Investments was in nonbinding talks to contribute about 200,000 ZEC after effectiveness. The filing also disclosed the Orchard vulnerability and the Ironwood upgrade (activated 2026-07-28) that added a tracked shielded pool and tighter Orchard-exit controls. Treat the affiliate ticket as nonbinding until it settles.

**Risks Grayscale itself listed.** Regulatory/listing friction despite viewing keys; residual trusted-setup pools; quantum as long-horizon; upgrade/coordination risk; and the usual higher-vol small-cap currency risk.

## Canonical Cases

- **Zcash sector-share, 2025-2026**: privacy usage and mindshare rose; Grayscale valued ZEC as under-recognized Currencies optionality, not as a BTC killer.
- **ZCSH wrapper path, 2026**: closed-end trust with huge historical NAV gaps seeking an ETF-style listing. Lesson: measure the wrapper separately from spot ZEC.
- **Privacy vs AI/tokenization rotation, Q1 2026**: same framework, different leadership. Sector leadership changes; the process does not.
- **Square-root sector indexes**: used to keep BTC/ETH from turning every sector product into the same two names.

## Do's and Don'ts

- Do assign one sector before talking upside.
- Do refresh sector share, fees, and shielded/usage data before giving a live verdict.
- Do distinguish research Top 20 (forward factors) from performance Top 20 (backward volatility-adjusted returns).
- Do read the product prospectus when the vehicle is ZCSH or another trust/ETP.
- Don't treat "Grayscale filed an ETF" as proof the token is cheap.
- Don't stack four privacy coins and call it diversification.
- Don't use this skill for memecoin tape-reading.

## Podcasts

- Unchained: https://podcasts.apple.com/us/podcast/id1123922160
- Bankless: https://podcasts.apple.com/us/podcast/id1499409058
- Shared podcast list: ../../docs/podcast-list.md

## YouTube

- Grayscale Investments: https://www.youtube.com/@GrayscaleInvestments
- Shared YouTube list: ../../docs/youtube-list.md

## Reading List

- Zcash: Financial Privacy in the Age of AI: https://research.grayscale.com/reports/zcash-financial-privacy-in-the-age-of-ai
- 2026 Digital Asset Outlook: https://research.grayscale.com/reports/2026-digital-asset-outlook-dawn-of-the-institutional-era
- The Stack, Zcash vs Bitcoin: https://www.grayscale.com/the-stack/zcash-has-something-bitcoin-does-not
- FTSE Grayscale Ground Rules: https://www.lseg.com/content/dam/ftse-russell/en_us/documents/ground-rules/ftse-grayscale-crypto-sector-index-series-ground-rules.pdf
- Shared reading list: ../../docs/reading-list.md

## Source Notes

Distilled from public Grayscale Research notes, FTSE Grayscale index ground rules, and Grayscale product/SEC materials. This is a judgment framework, not Grayscale advice and not a recommendation to buy ZEC or ZCSH. When quoting a multiple or share figure, cite the date of the snapshot and recompute with live data.
