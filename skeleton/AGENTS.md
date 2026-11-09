# AGENTS.md — rule index

<!-- Generated block: managed by `vaibe-os generate` (rules from the core + this instance's
canon). Do not edit between the markers. -->
<!-- generated:rules:start -->
<!-- generated:rules:end -->

## Workspace rules

- The workspace is a git repository: everyone with access sees everything — private zones are
  separate workspaces.
- Incoming handoffs land in `inbox/`: process them like regular incoming material.
- Tasks live in `projects/*/tasks/`: `README.md` is for humans, `AGENTS.md` holds the machine
  state (frontmatter) and agent instructions.
