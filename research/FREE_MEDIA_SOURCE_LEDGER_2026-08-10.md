# Free Media Source Ledger — verified 2026-08-10

Purpose: operational source/rights/quota record. Provider-level license terms never override item-level third-party rights.

| Source | Free request/download limit | Reset | Commercial-use position | Attribution | API | Primary sources |
|---|---:|---|---|---|---|---|
| Pexels | 200 requests/hour + 20,000/month per default API key | Hourly + monthly quota windows; inspect response headers | Pexels photos/videos are free for personal and commercial use under the Pexels License, subject to restrictions | Website license: not required. API integrations must follow Pexels API linking/attribution terms | Yes | https://help.pexels.com/hc/en-us/articles/47677890260761-Is-the-Pexels-API-free-to-use ; https://www.pexels.com/api/documentation/ ; https://www.pexels.com/license/ |
| Pixabay | 100 requests per 60 seconds by default; responses must be cached for 24h; systematic mass downloads prohibited | `X-RateLimit-Reset` gives seconds remaining | Pixabay Content License permits commercial use subject to prohibited uses and third-party rights | License: not required; API asks applications to show users where results come from | Yes | https://pixabay.com/api/docs/ ; https://pixabay.com/service/license-summary/ ; https://pixabay.com/service/terms/ |
| Unsplash | Demo: 50 JSON API requests/hour. Approved production: 1,000/hour | Hourly | Unsplash License permits free commercial and non-commercial use; standalone resale/competing-library restrictions apply | General license: not required. API: photographer + Unsplash attribution/linking required | Yes | https://unsplash.com/documentation ; https://unsplash.com/license ; https://help.unsplash.com/en/articles/2511315-guideline-attribution |
| Openverse | **No stable numeric quota verified in current consumer docs retrieved.** Anonymous and authenticated clients are throttled; authenticated apps can receive standard/enhanced tiers. Read rate-limit response headers and back off | Response-header / throttle-tier controlled | Search index contains CC-licensed and public-domain works; license varies per result. Openverse explicitly says it does not verify each work’s license status | Per underlying license; independently verify attribution | Yes | https://docs.openverse.org/packages/js/api_client/index.html ; https://docs.openverse.org/api/reference/index.html ; https://openverse.org/about |
| Wikimedia Commons | 2026 global API rate limits: unidentified client 10 requests/minute; compliant User-Agent-only unauthenticated bot 200/minute. Browser unauthenticated 200/minute. Higher authenticated classes exist | Per minute; respect `Retry-After` on 429/503 | Mixed free licenses/public domain; verify each file’s license and non-copyright rights | Item-specific | Yes, Wikimedia APIs | https://www.mediawiki.org/wiki/Wikimedia_APIs/Rate_limits ; https://www.mediawiki.org/wiki/Wikimedia_APIs/Access_policy ; https://commons.wikimedia.org/wiki/Commons:Reusing_content_outside_Wikimedia |
| NASA | Registered default API key: 1,000 requests/hour. `DEMO_KEY`: 30/hour and 50/day | Registered key uses rolling hourly counter; DEMO_KEY also has daily cap | Much NASA-created material is not subject to U.S. copyright, but logos/insignia, identifiable people and third-party content can carry restrictions | Follow NASA media/credit guidance and item context | Yes | https://api.nasa.gov/assets/html/authentication.html ; https://www.nasa.gov/nasa-brand-center/images-and-media/ |
| Library of Congress | 20 requests/minute; no key required | Per minute; can tighten under heavy load; handle 429/CAPTCHA | Rights vary by collection/item. Prefer `Free to Use and Reuse` collections, then retain the item rights statement | Item-specific | Yes | https://www.loc.gov/apis/json-and-yaml/working-within-limits/ ; https://www.loc.gov/apis/ ; https://www.loc.gov/free-to-use/ |
| Smithsonian Open Access | Public API runs through api.data.gov. Default registered api.data.gov quota is 1,000 requests/hour unless a service-specific override applies. `DEMO_KEY`: 30/hour + 50/day | Rolling hourly; DEMO_KEY also daily | Assets **designated CC0** may be used commercially without Smithsonian permission/fee. Non-CC0 assets do not receive that grant | CC0: not required; credit encouraged. Third-party trademark/privacy/publicity rights can still apply | Yes | https://www.si.edu/openaccess/faq ; https://api.data.gov/docs/developer-manual/ ; https://edan.si.edu/openaccess/apidocs/ |
| Coverr | Free Demo API: 50 requests/hour. 2,000/hour Production requires paid Pro/Ultimate | Hourly | **CONTRADICTION requiring conservative handling:** Coverr license says free downloads can be used commercially; API developer intro says free API access must not be used to resell or “use the videos for commercial use,” while current developer FAQ says API content is commercially licensed. Do not automate commercial Coverr ingestion until Coverr clarifies which API term controls | Free download license page currently says free downloads require creator/Coverr attribution; API requires Coverr logo/link | Yes | https://api.coverr.co/docs/start/ ; https://api.coverr.co/docs ; https://coverr.co/developers ; https://coverr.co/license/ |
| Mixkit | No production public API/quota verified; treat as manual/download source, not an API dependency | N/A | License varies by item type and can be Free License or Restricted License. Commercial eligibility must be read from the relevant license | Depends on item/license | No production public API verified | https://mixkit.co/license/ |
| Videvo | No stable free public API quota verified | N/A | Free content may use Videvo Attribution, CC BY 3.0, legacy/royalty-free licenses; Editorial Use Only content is not commercial-use eligible | Depends on asset/license; Attribution and CC BY require credit | No stable public API dependency verified | https://www.videvo.net/blog/terms-conditions/ ; https://www.videvo.net/blog/how-we-license-our-footage-on-videvo-net/ |

## Production policy

A source adapter must emit these fields for every asset before the asset is eligible for a render:

```text
provider
provider_asset_id
source_url
creator
license_code
license_url
commercial_use_status
attribution_required
attribution_text
rights_checked_at
retrieved_at
sha256
```

Reject an asset when commercial-use status is unknown, attribution cannot be satisfied, the rights statement cannot be retained, or third-party restrictions conflict with the intended use.

## Operational implications

- Pexels, Pixabay and Unsplash are the cleanest API-first stock candidates, but each has API-specific behavioral requirements beyond the general content license.
- Smithsonian CC0 is the cleanest cultural-heritage commercial source when the item is explicitly CC0.
- Wikimedia and Openverse are high-value discovery sources but require item-level license/attribution verification.
- Coverr is quarantined for automated commercial ingestion until its current API/commercial-use wording is reconciled.
- Mixkit and Videvo remain manual/item-licensed sources unless a current stable API contract is independently verified.
