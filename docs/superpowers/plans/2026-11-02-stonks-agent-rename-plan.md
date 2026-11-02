# Implementation Plan: Rename Plugin to `stonks-agent` and Skills to Generic Names

**Spec:** [`docs/superpowers/specs/2026-11-02-stonks-agent-rename-design.md`](file:///c:/Users/aruna/development/stonks-agent/docs/superpowers/specs/2026-11-02-stonks-agent-rename-design.md)

## Proposed Changes

### 1. Rename Skill Directories & Files
- Rename `skills/indian-fundamental-valuation` to `skills/fundamental-valuation`
- Update frontmatter in `skills/fundamental-valuation/SKILL.md` (`name: fundamental-valuation`)
- Rename `skills/indian-portfolio-sentinel` to `skills/portfolio-sentinel`
- Update frontmatter in `skills/portfolio-sentinel/SKILL.md` (`name: portfolio-sentinel`)

### 2. Rename Plugin Identifiers in Manifests & Harnesses
- `plugin.json`: `"name": "stonks-agent"`
- `plugin.yaml`: `name: stonks-agent`
- `harnesses/openclaw_config.json`: Update `"name"` and `"id"` to `"stonks-agent"`, update skill paths and references from `indian-fundamental-valuation` and `indian-portfolio-sentinel` to `fundamental-valuation` and `portfolio-sentinel`.
- `harnesses/hermes_config.yaml`: Update skill paths if referenced.

### 3. Update Agents & Skills References
- `agents/fundamental_analyst.md`: Update `indian-fundamental-valuation` to `fundamental-valuation`.
- `agents/portfolio_sentinel.md`: Update `indian-portfolio-sentinel` to `portfolio-sentinel`.
- `agents/portfolio_manager.md`: Update `indian-portfolio-sentinel` to `portfolio-sentinel`.
- `skills/portfolio-sentinel/SKILL.md`: Update any internal self-referential name/links.
- `skills/fundamental-valuation/SKILL.md`: Update any internal self-referential name/links.

### 4. Rename Spec and Plan Docs
- Rename `docs/superpowers/specs/2026-11-01-indian-market-trading-plugin-design.md` -> `docs/superpowers/specs/2026-11-01-stonks-agent-design.md`
- Rename `docs/superpowers/plans/2026-11-01-indian-market-trading-plugin-plan.md` -> `docs/superpowers/plans/2026-11-01-stonks-agent-plan.md`
- Update links in the spec and plan files.

### 5. Update Documentation & Tests
- `README.md`: Update symlink examples (`~/.hermes/plugins/stonks-agent`), table of skills, and references.
- `tests/test_plugin_verification.py`:
  - Update expected skills list (`fundamental-valuation`, `portfolio-sentinel`).
  - Update path check for sentinel skill (`skills/portfolio-sentinel/SKILL.md`).
- `tests/test_hermes_plugin.py`:
  - Update assertion for plugin name: `self.assertEqual(parsed.get("name"), "stonks-agent")`.

### 6. Verification
- Run `.venv\Scripts\python -m unittest discover tests` and verify 100% pass rate.

## Plan Steps
- [ ] Task 1: Rename skill directories and update their SKILL.md frontmatter.
- [ ] Task 2: Update manifests (`plugin.json`, `plugin.yaml`) and harness configs (`openclaw_config.json`, `hermes_config.yaml`).
- [ ] Task 3: Update agent markdown files (`fundamental_analyst.md`, `portfolio_sentinel.md`, `portfolio_manager.md`).
- [ ] Task 4: Rename spec and plan files in `docs/superpowers/`.
- [ ] Task 5: Update `README.md` and tests (`test_plugin_verification.py`, `test_hermes_plugin.py`).
- [ ] Task 6: Run tests and confirm all pass.
