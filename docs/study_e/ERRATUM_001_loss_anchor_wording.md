# Erratum 001 (2026-11-19): loss-anchor wording in the frozen Study E pre-registration
Affects wording only. No grid value, hypothesis, code or result changes. The frozen files (tag study-e-prereg-v1) are not edited; this erratum is filed beside them.

## What was checked
CosmicDancePro (Basak, Pal, Bhattacherjee; arXiv:2604.22685v1) and WetLinks (Table II) were re-read against the PDFs on 2026-11-19.
- WetLinks Table II: Osnabruck 22.7% of samples with loss, min 0.4%, max 84.4%, mean 1.0%, sd 3.3%; Enschede 24.6%, 0.4%, 81.2%, 1.0%, 2.9%; 250 pings at 0.1 s interval every 3 minutes. Matches what the pre-registration and paper draft used.
- CosmicDancePro: a baseline loss of up to 2% is observed at all four LENS vantage points. This matches the pre-registration.

## What was incomplete or overstated
1. The pre-registration cites only the 2% baseline from CosmicDancePro. The same paper reports uplink loss rising during solar storms: increases of up to 4-10% across four vantage points in May 2024, and, in October 2024, up to 60% uplink loss "for a while" at Seattle (abstract: 10-60% uplink packet loss; abstract also states the uplink is more sensitive than the downlink). These are consumer broadband (Starlink) measurements, not TT&C.
2. The wording approved in the working session for p = 0.3 and 0.5 ("stress points, not observed conditions", on the claim that nothing measured supports sustained 30-50% loss) is too strong. Broadband uplink loss of that order has been reported during an extreme space-weather event, at one site, for limited periods.

## Corrected wording for the paper
p = 0.3 and 0.5 are stress points beyond the clear-sky broadband baseline (about 1-2% mean loss in WetLinks, up to 2% in LENS data) and beyond the burst-level Starlink ping data (2.16%). The upper values are comparable to the worst broadband uplink loss reported during the May and October 2024 solar storms [CosmicDancePro], at limited sites and for limited periods. They are not measured TT&C loss and no TT&C link is claimed to experience them.

## Consequence
None for results. The wording in the paper replaces "not observed conditions". The pre-registration text itself stays frozen; this erratum is the record.
