# Free Media Rights Policy

## Purpose

Prevent a provider name from being treated as proof of commercial reuse rights.

## Rule

Every externally sourced asset must retain its item-level rights record before it is eligible for a production render.

Required fields:

- provider
- provider asset ID
- original source URL
- creator / rights holder when available
- license identifier
- license URL or rights statement URL
- commercial-use status
- attribution requirement
- attribution text when required
- retrieval timestamp
- SHA-256 of the downloaded asset

## Provider classes

### Generally uniform provider licenses

Pexels, Pixabay and Unsplash provide broad provider-level licenses, but API-specific attribution and linking obligations must still be respected.

### Mixed-rights collections

Openverse, Wikimedia Commons, NASA, Library of Congress, Smithsonian, Mixkit and Videvo can contain assets with materially different rights. Validate the individual asset record. Smithsonian Open Access assets explicitly marked CC0 are a particularly clean source; do not infer CC0 for non-Open-Access Smithsonian material.

## Production gate

An asset is rejected before rendering when:

1. commercial-use status is unknown;
2. the license or rights statement cannot be retained;
3. required attribution cannot be generated;
4. the downloaded file does not match the recorded checksum;
5. an editorial-only or otherwise incompatible restriction conflicts with the intended use.

## Storage boundary

The media artifact may live in Drive, local storage, object storage or another approved store. The rights record must remain independently queryable and survive replacement of the final composition.
