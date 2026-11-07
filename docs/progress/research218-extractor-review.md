# Research218 extractor review

**Disposition: accepted for qualified static extraction, 2026-11-07.** Retrieve
conquest source at `1544d666c45004f1eda362cb84a4701e0e4143d2`, tool version
**1.0.1**, SHA256
`5d266a075ce1cc75ccb359f2b4a64aa5bbf82e2dca031965c729e6abd53a97f5`.
The path-disclosure correction below is resolved. Consumer/native/packaging
acceptance remains separate. [Scalar review receipt](../data/research218-extractor-review-v1.json).

Independent research review of conquest PR346, implementation first delivered at
`282777136e355ff94f8e21aac01ae7a6818d4cba`. The initial source SHA256 was
`558bdb331e451c47b209c8c85ff77cb5a03d874a3e3b826e846e75f2a42f407c`.
The later `1094f72c` changes receipts/notes only, not that implementation.
No research changes were made in conquest. Source corrections belong to its session.

## Completed independent checks

- Read all 767 tool lines and 448 test lines, the integration guide, scalar v3
  and validation receipts, and compared them with Research219's contract.
- Copied exact pinned tool/tests outside conquest; all 35 tests pass. The source
  hash matches the author's receipt. The copied tool has no conquest imports.
- Recovered the ten supplied WAV contents unambiguously from the verified private
  backup. Source object hashes checked privately; format/provenance remains
  "supplied file", not "shipped original". No private paths/hashes are published.
- Ran an isolated copied-tool CLI into a new private directory. The metadata is
  exactly equal to the author's v3 report: 73 PE leaves, 29 forms, 11 lists/128
  images, 63 glyph sheets/79 frames, ten resource bitmaps and ten valid WAVs.
- Verified all 362 freshly exported files against their private manifest hashes;
  independent ImageMagick accepted 345 PNGs, six CURs and one ICO. Separately
  checked PNG CRCs, decompressed lengths, filter bytes and geometry with stdlib.
  Native container decode is not native cursor/rendering/compositing acceptance.
- Repeated an export against the existing private output directory with a new
  metadata path: exit 2, no new receipt, all 362 existing payloads unchanged.
- Independently checked all 89 candidate consumer keys against the 100 keys at
  remake `55bd7fce`; no invalid keys. The eleven absent keys are five generic
  `unit.*.icon` choices and six seamless `terrain.*.surface` keys. Candidate
  component correspondence, river/owner variants and screen use remain distinct.
- Decoded all ten supplied PCM files independently with Python's `wave` module;
  channels, depth, sample rate, frame counts and decoded payload lengths agree.

## Review correction requested

`wav_inventory` stored `reason=str(e)` for an OSError. A synthetic PermissionError
with an absolute WAV filename reproduces that private input path in JSON.
Requested a stable error class/errno without exception filenames, a regression
and a new immutable source/receipt identity. This is an error-path metadata
contract defect; the successful v3 receipt itself contains no such failure.
No pixel/parser mismatch was found in the tested qualified profile.

**Resolved at `1544d666`:** reviewed the complete implementation/test/guide diff.
The code change is limited to version 1.0.1 and structured OSError diagnostics
(`wav-file-io-error`, exception class, errno). It does not serialize exception
filenames or arbitrary exception text into JSON. A new test covers PermissionError
and FileNotFoundError; the full isolated suite now passes **36/36**.

A new isolated copied-tool CLI run against the pinned original and recovered
supplied WAVs exactly reproduces the author's immutable
`extractor-private-export-v5.json`. Compared with the reviewed v3 metadata, only
`extractor_version`, `extractor_sha256` and `cache_identity` change. All **362**
newly written files match the corrected private manifest and are byte-identical
to the initial files independently decoded above. The 352-image external decoder
run and existing-directory refusal were performed on 1.0.0; their output/unchanged
publication-code coverage is carried forward, not claimed as new 1.0.1 runs.
No other blocker was found within this qualified static scope. Later source
changes require a new source identity and assessment of affected checks.

## Boundaries

Static inventory/conversion only; no game, Wine or native Windows run. All media,
audio and per-output hashes remain outside Git. Main must retrieve the final
reviewed source pin and source hash, explicitly supply Python 3.10+ or port the
tested contract to .NET, and validate real consumer loading/compositing/fallback.
No runtime packaging or shipped adapter is claimed by this review.
