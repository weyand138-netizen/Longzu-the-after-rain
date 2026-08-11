# ADR-0007: SYS-BUILD Contract Closure and Release Identity

## Status

Accepted

## Date

2026-08-09

Amended 2026-08-09: identity-affecting versus run-only build configuration
split; BUILD-Q6–Q9 reclassified as downstream implementation/release gates.

## Engine Compatibility

| Field | Value |
|---|---|
| **Engine** | Ren'Py 8.5.3 / Python 3.12-compatible scripts |
| **Domain** | Core / Build / Test / Release |
| **Knowledge Risk** | HIGH — pinned engine is newer than the May 2025 baseline |
| **References Consulted** | `docs/engine-reference/renpy/VERSION.md`, `docs/engine-reference/renpy/BUILD.md`, `docs/engine-reference/renpy/capability-manifest-v1.json`, `docs/engine-reference/renpy/evidence/2026-08-09-build-q1-spike/` |
| **Post-Cutoff APIs Used** | Ren'Py `launcher distribute` and `testcase`/`testsuite` are used only through the verified capability boundary; no unverified API is admitted by this ADR |
| **Verification Required** | Re-run the pinned runner capability probe, lint, complete RELEASE evidence, staging/archive exclusion scans, offline launch, and final hash/provenance validation before public release |

The local reference library has no dedicated Ren'Py module references,
`breaking-changes.md`, or `deprecated-apis.md`. The verified capability manifest
and build spike are therefore normative for the runner contract, while all
engine-specific implementation details remain subject to the verification gate
above.

## ADR Dependencies

| Field | Value |
|---|---|
| **Depends On** | ADR-0001 through ADR-0006; approved owner GDD manifests; `design/registry/entities.yaml` |
| **Enables** | SYS-BUILD implementation stories, SYS-TEST RELEASE implementation, release-pipeline spike, archive closure and public-build readiness |
| **Blocks** | No implementation may mark a release `READY` until this ADR's candidate, evidence, legal, isolation, and identity contracts are implemented |
| **Ordering Note** | SYS-BUILD creates the candidate identity and staging manifest first; SYS-TEST returns staging evidence before package execution, then archive evidence after package execution. Any identity or hash change starts a new build run. |

## Context

### Problem Statement

SYS-BUILD and SYS-TEST already require deterministic manifests, provenance,
test-only isolation, and archive closure, but their exact schemas and sequencing
were left provisional. In particular, the project had no frozen answer for the
runner capability contract, `candidate_manifest:v1`, artifact directory layout,
canonical encoding, legal/provenance closure, archive hashing, the two-way
SYS-TEST evidence handshake, or the identity hierarchy that prevents an archive
hash from hashing itself.

### Constraints

- The shipped artifact is an offline Windows 10/11 x86-64 Ren'Py 8.5.3 package.
- Python logic and build helpers use the standard library only.
- Builds are offline, deterministic, and independent of file enumeration order,
  local time, locale, timezone, and random values.
- Source owners retain authority over content, IDs, formulas, thresholds, and
  legal declarations; SYS-BUILD validates and seals but does not repair them.
- Test observers, spies, fault injectors, synthetic saves/roots, benchmark
  harnesses, debug IDs, runtime scanners, and evidence forgers are test-only.
- Release provenance must be inspectable without exposing semantic state,
  counterevidence tokens, resolver predicates, or hidden progress.

### Requirements

- Freeze a versioned runner capability contract with executable and environment
  identity, command, exit-code, output, timeout, and cleanup semantics.
- Freeze `candidate_manifest:v1` and a stable, non-overlapping staging/release
  directory layout.
- Use one canonical encoding for all identity and manifest hashes.
- Make provenance, legal closure, archive closure, and SHA-256 hashes exact and
  reproducible.
- Require SYS-TEST evidence in both directions: before package execution for
  staging and after package execution for the final archive.
- Keep production-to-test-only dependency count at zero and prove it twice.
- Define source, candidate, evidence, archive, and release identity layers with
  no archive-hash self-reference.

## Decision

### 1. Frozen runner capability contract

`engine-capability-manifest:v1` is the only authority for the package runner.
The current accepted instance is
`docs/engine-reference/renpy/capability-manifest-v1.json`.

The manifest must include:

- engine name, pinned and observed versions, Python compatibility, target OS and
  architecture;
- runner relative path and SHA-256;
- working directory, command entrypoint, package selection, format, destination
  and no-update options;
- verified success, lint, build, interruption, timeout, and native failure
  exit-code semantics;
- stdout/stderr/log/distribution-log capture rules;
- output format, package markers, archive root, and expected output cardinality;
- supervisor timeout/termination behavior, process-tree cleanup, and retained
  diagnostic paths;
- verification date and evidence-root references.

The runner must be invoked with the pinned SDK and a new isolated output
directory. A successful package command is not sufficient by itself: exit code,
raw output, output cardinality, runtime markers, and process cleanup must all
match the capability contract.

### 2. Candidate manifest and artifact directory contract

Each build run has a unique `build_run_id`, but `candidate_identity` does not
include it or timestamps. Configuration is split into identity-affecting inputs
and run-only execution metadata. The frozen release root is:

```text
production/releases/<candidate_identity>/
  candidate_manifest.json
  source_inventory.json
  catalog_inventory.json
  asset_inventory.json
  legal_closure.json
  provenance_index.json
  evidence_index.json
  staging_exclusion_report.json
  archive_exclusion_report.json
  hashes.json
  archive/
    <package-name>.zip
```

Ephemeral and diagnostic material is kept outside the release root:

```text
production/build-runs/<build_run_id>/
  staging/
  runner/
  diagnostics/
```

`candidate_manifest:v1` is a canonical JSON object containing exactly these
top-level groups: `schema`, `candidate`, `inputs`, `engine_capability`,
`artifact_layout`, `evidence_contract`, `legal_closure`, `archive`, and
`provenance`. Required fields include `candidate_identity`,
`identity_generation`, `build_run_id`, `build_mode`, owner manifest IDs and
hashes, source/catalog/asset inventory IDs and hashes, engine capability ID and
hash, staging tree ID and hash, required RELEASE scope, evidence references,
legal closure reference, archive reference, and stable finding IDs. `build_run_id`
and timestamps are provenance fields only and never candidate identity inputs.

The manifest and all indexes are siblings of the package, not files inside the
package. This makes the package byte hash independent of the manifest that
records it.

### 3. Canonical encoding

`canonical_encoding:v1` is mandatory:

- structured manifests use JSON with UTF-8, no BOM, no trailing whitespace,
  LF line endings, `ensure_ascii=false`, no insignificant whitespace,
  lexicographically sorted object keys, and arrays in declared semantic order;
- strings are Unicode scalar values; paths use `/`, are relative to the declared
  root, and are normalized before sorting;
- identity input is restricted to `null`, booleans, exact integers, strings,
  arrays, and objects; floats, NaN, infinity, implicit defaults, and runtime
  timestamps are forbidden in identity records;
- hash inputs are the exact canonical bytes; files use exact bytes and
  structured records use canonical JSON bytes;
- record lists sort by `(kind, stable_id, relative_path, owner)` with UTF-8 byte
  comparison; duplicate keys, IDs, paths, or records fail closed.

No implementation may use language-native object serialization, platform path
ordering, locale collation, pretty-printing, or a serializer whose output is
not covered by this contract.

### 4. Identity hierarchy and archive-hash self-reference rule

The following hierarchy is normative:

```text
source_identity
  -> candidate_identity
       -> evidence_identity (SYS-TEST, per scope)
       -> archive_hash (raw package bytes)
       -> manifest_hash / provenance_hash / legal_closure_hash
            -> release_identity
```

- `source_identity` hashes the canonical source/catalog/asset/legal/engine and
  `identity_affecting_build_config` records.
- Identity-affecting build configuration includes build mode when it changes
  the delivered bytes, target platform, package format/package selection,
  archive/include policy, byte-producing build options, and any setting that
  changes shipped semantics or bytes.
- Run-only configuration includes workspace path, output location, log level,
  timeout, diagnostic retention count, `build_run_id`, timestamps, and other
  observability/placement controls. These belong only to `run_record` and never
  change `candidate_identity`.
- `candidate_identity` hashes the candidate identity core and excludes
  `build_run_id`, timestamps, final archive bytes, `archive_hash`,
  `manifest_hash`, `provenance_hash`, run-only configuration, and all derived
  finalization records.
- `evidence_identity` binds a test bundle to `candidate_identity`, its scope,
  input hashes, runner/environment identity, case mapping, and raw-output hashes.
- `archive_hash` is SHA-256 over the exact final package bytes only.
- `manifest_hash`, `provenance_hash`, `legal_closure_hash`, and exclusion-report
  hashes are computed after the archive exists and may contain `archive_hash`,
  but none is an input to `candidate_identity`.
- `release_identity` is the final audit identity over the ordered tuple of
  `candidate_identity`, `archive_hash`, manifest/provenance/legal/evidence and
  both exclusion-report hashes. It is not used to name the package before it is
  built.

The canonical manifest may record both configuration classes for auditability,
but only `identity_affecting_build_config` is included in the identity core.
Changing `diagnostic_retention_runs` or a valid workspace/output path therefore
creates a new `run_record`/`build_run_id` without making the candidate stale.

This two-phase construction prevents the archive hash from including a file
that contains the archive hash. A manifest stored inside the archive, a hash of
the release directory, or a candidate hash that includes any final hash is
forbidden.

### 5. Provenance, legal closure, and archive hashing

Every production source, catalog, generated bundle, asset, legal declaration,
runner, environment, evidence bundle, and package records its owner, stable ID,
relative path, generation, exact input hash, and canonical record hash.

`legal_closure:v1` requires each asset to resolve to a Legal Asset Register
entry containing source, permission/license, modification status, attribution,
allowlist status, and any non-commercial/fan-work notice. Missing, ambiguous,
forbidden, or unallowlisted assets fail the release; placeholder declarations do
not close the gate.

`archive_closure_valid` requires exact zero counts for test-only leakage,
production-to-test-only edges, network dependencies, telemetry entries,
unallowlisted assets, and undeclared assets, plus valid legal closure and exact
archive/provenance hashes. All hashes are SHA-256 lowercase 64-character hex.

### 6. SYS-TEST bidirectional evidence stages

The only release handshake is:

1. **`STAGING_EVIDENCE_BOUND`** — SYS-BUILD publishes the frozen candidate
   manifest, staging inventory, candidate identity, requested RELEASE manifest,
   runner capability identity, and staging exclusion input. SYS-TEST returns a
   non-empty current `test_evidence_bundle:v1` and staging exclusion report
   bound to the exact candidate identity and source/catalog/config/fixture/
   runner/environment hashes.
2. **Package execution** — SYS-BUILD may invoke the package runner only after
   stage 1 passes. It records raw runner output, exit code, package cardinality,
   and archive hash.
3. **`ARCHIVE_EVIDENCE_BOUND`** — SYS-BUILD publishes the archive inventory and
   archive hash. SYS-TEST performs the final test-only/dependency/closure scan
   and returns the archive exclusion report plus final RELEASE evidence binding.
4. **`READY`** — SYS-BUILD accepts the release only when both evidence stages,
   legal closure, package runner, archive closure, and all exact hashes pass.

SYS-TEST owns evidence schema, case execution, artifact state, and exclusion
reports. SYS-BUILD owns candidate/staging/archive manifests and package
execution. Neither system may edit the other's artifact or upgrade component
evidence into RELEASE evidence.

### 7. Test-only isolation

Test-only assets and code use an explicit test-only namespace and manifest. The
allowed dependency direction is `test-only -> production`; the reverse edge is
always a failure. Test-only content may observe or adapt production contracts
through approved adapters, but production source may not import, reference,
discover, or receive a runtime seam from test-only code.

The staging and final archive scans both cover observers, spies, fault
injectors, protocol bombs, synthetic saves/roots, benchmark harnesses, debug
IDs, evidence forgers, runtime scanners, test namespaces, and test-only save or
persistent payloads. Each category count must be zero.

## Architecture Diagram

```text
approved owner manifests + legal register + engine capability
                              |
                              v
                     SYS-BUILD / staging lock
                              |
                 candidate_manifest:v1 + candidate_identity
                              |
                              v
                  SYS-TEST: RELEASE evidence
                 + staging exclusion report
                              |
                              v
                 Ren'Py 8.5.3 package runner
                              |
                              v
                       archive + archive_hash
                              |
                              v
                  SYS-TEST: archive exclusion scan
                              |
                              v
            legal/provenance/hash closure -> release_identity -> READY
```

## Key Interfaces

```text
build_candidate_manifest_v1(inputs) -> CandidateManifestV1
candidate_identity(manifest_identity_core) -> sha256_hex
bind_staging_evidence(candidate_manifest, evidence_bundle, exclusion_report)
bind_archive_evidence(candidate_manifest, archive_inventory, archive_hash,
                      archive_exclusion_report, final_evidence)
```

The two bind operations require exact identity and hash equality and are
monotonic: a later bind cannot rewrite an earlier artifact. Any mismatch yields
`BLOCKED_INPUT`, `STALE`, or `FAILED` according to whether the input is missing,
old, or invalid.

## Alternatives Considered

### Alternative 1: Hash the complete release directory

- **Description**: Store the package, manifest, and hashes together and hash the
  whole directory as one release identity.
- **Pros**: Simple-looking audit command and one top-level digest.
- **Cons**: The manifest contains the archive hash and the directory hash would
  contain the manifest hash, creating self-reference or requiring mutable
  placeholders.
- **Rejection Reason**: It cannot provide a stable package hash and would make
  verification depend on write order.

### Alternative 2: Let SYS-TEST derive the candidate from executed artifacts

- **Description**: Run tests first, then let the test runner select the source,
  fixtures, and package inputs that become the candidate.
- **Pros**: Fewer explicit preflight files.
- **Cons**: Tests would become a second source authority, component evidence
  could be mistaken for release evidence, and production/test isolation would
  be checked too late.
- **Rejection Reason**: Violates owner authority and the existing SYS-TEST
  prohibition on defining production semantics.

### Alternative 3: Use ad hoc serializer and path conventions

- **Description**: Hash native Python/JSON output and rely on current directory
  enumeration for ordering.
- **Pros**: Minimal implementation effort.
- **Cons**: Output varies by platform, serializer, locale, and file order;
  stale evidence becomes difficult to detect.
- **Rejection Reason**: Fails deterministic offline reproducibility and audit
  requirements.

## Consequences

### Positive

- SYS-BUILD and SYS-TEST have a single, versioned, two-way release handshake.
- Candidate, evidence, archive, legal, and release identities are independently
  verifiable and cannot self-reference.
- The release directory is predictable and can be audited without opening the
  package to interpret its own hash.
- Test-only leakage is checked before and after package creation.

### Negative

- Every release requires two SYS-TEST exclusion scans and an additional final
  evidence binding step.
- Canonical encoding and exact hash equality make manual edits and serializer
  substitutions invalid.
- Legal and provenance records require ongoing owner maintenance.

### Risks

- **Runner drift**: the SDK or executable changes without a source change.
  Mitigation: runner path, observed version, and executable hash are required
  capability inputs and invalidate the candidate when changed.
- **Serializer drift**: different code emits different canonical bytes.
  Mitigation: canonical encoding is versioned and covered by golden vectors.
- **Late archive leakage**: packaging introduces test-only or undeclared files.
  Mitigation: final archive scan is independent of the staging scan and blocks
  `READY` on any non-zero count.
- **Legal record drift**: an asset changes while its declaration remains old.
  Mitigation: legal closure hashes and asset hashes are bound to the same
  candidate generation.

## GDD Requirements Addressed

| GDD System | Requirement | How This ADR Addresses It |
|---|---|---|
| `sys-build.md` | Offline Windows package, deterministic inventory, provenance, legal closure, archive hashing, and test-only isolation | Freezes runner, manifest, directory, encoding, closure, hash, and evidence contracts |
| `sys-test.md` | Non-empty current RELEASE evidence, exact identity binding, raw artifacts, and production/test separation | Defines staging and archive evidence stages and their ownership boundary |
| `systems-index.md` | SYS-BUILD/SYS-TEST dependencies must be bidirectional | Adds candidate-manifest input and final evidence output in both directions |

## Performance Implications

- **CPU**: Linear in the number of inventory records and archive bytes; hashing
  is performed once per locked input and once for the final package.
- **Memory**: Streaming file hashing is required; canonical records may be
  materialized only for the bounded manifest/index set.
- **Load Time**: No shipped runtime dependency; offline launch remains governed
  by the existing 5-second startup target.
- **Network**: None. Build and release validation are offline-only.

## Migration Plan

1. Add `docs/registry/architecture.yaml` and register the frozen interfaces and
   forbidden patterns.
2. Update SYS-BUILD, SYS-TEST, the master architecture, control manifest, and
   systems index to reference ADR-0007 and the exact schemas.
3. Implement manifest and canonical-encoding validators before the package
   runner integration.
4. Implement the staging evidence handshake, then the package runner, then the
   archive evidence handshake.
5. Generate fresh evidence and release artifacts; no existing provisional
   candidate or evidence may be upgraded in place.

## Validation Criteria

- Two independent runs with the same identity core produce identical
  `candidate_identity`, canonical bytes, inventories, and evidence bindings.
- A one-byte source, runner, legal, identity-affecting config, fixture, or
  environment change makes the old candidate stale; changing a valid workspace
  path, output location, log level, timeout, or diagnostic retention count does
  not.
- The package hash is reproducible from exact package bytes and is not affected
  by manifest/provenance writes beside it.
- Staging and archive exclusion reports each show zero test-only and
  production-to-test-only findings.
- Missing, stale, cross-generation, partial, or component-only evidence cannot
  reach `READY`.
- Final provenance and legal closure resolve every release artifact and asset
  with exact lowercase SHA-256 hashes.

## Related Decisions

- [ADR-0001](adr-0001-deterministic-ending-resolution.md)
- [ADR-0002](adr-0002-rollback-and-persistence-boundary.md)
- [ADR-0003](adr-0003-content-and-presentation-boundary.md)
- [ADR-0004](adr-0004-semantic-ending-snapshot-and-state-envelope.md)
- [ADR-0005](adr-0005-counterevidence-ledger-and-detectable-state-initialization.md)
- [ADR-0006](adr-0006-ending-completion-boundary.md)
- [SYS-BUILD](../../design/gdd/sys-build.md)
- [SYS-TEST](../../design/gdd/sys-test.md)
