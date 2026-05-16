# Agently-Skills Legacy V1

This directory preserves the previous 12-skill Agently-Skills catalog for
explicit rollback and historical projects.

- Status: frozen
- Last supported Agently framework version: `4.1.1`
- Skills path: `legacy/v1/skills/`
- Bundle manifest: `legacy/v1/bundles/manifest.json`

New projects should use the compact default catalog in the repository root
`skills/` directory. The Agently framework compatibility registry only tracks
the current default catalog generation; this V1 archive does not receive new
framework-surface updates.

Do not use `--full-depth` for default installs. That option can discover legacy
skills under this archive and should be reserved for explicit rollback work.
