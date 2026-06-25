# Naming convention for vAIbe ecosystem products

> Source: `/evolve` 2026-03-28 — naming standardization based on observed inconsistencies

## Rule

All ecosystem products are named in the format:

```
vAIbe-{product}
```

Where:
- `vAIbe` — always in this exact case (lowercase `v`, uppercase `AI`, lowercase `be`)
- `-` — hyphen separator
- `{product}` — product name in **lowercase**

Exception: if the product part contains a well-established acronym, it keeps its standard casing.

## Examples

| Correct | Incorrect |
|-----------|-------------|
| `vAIbe-OS` | `Vaibe-OS`, `VAIBE-OS`, `vAIbe OS`, `vaibe-os` |
| `vAIbe-digest` | `vAIbe Digest`, `vAIbe-Digest`, `Vaibe-Digest` |
| `vAIbe-bots` | `vAIbe Bots`, `vAIbe-Bots` |
| `vAIbe-studio` | `vAIbe Studio`, `vAIbe-Studio` |
| `vAIbe-listener` | `vAIbe Listener` |
| `vAIbe-vpn` | `vAIbe VPN` |

## Why `-OS` is uppercase

`OS` is a well-established acronym (Operating System). Likewise: if a product were named `vAIbe-API`, the acronym API would be uppercase.

## Where it applies

- File and directory names
- README and documentation
- Code (repository names, configuration variables)
- User interface and marketing materials
- Internal documents (tasks, plans, knowledge base)

## Special cases

- At the start of a sentence the case of `vAIbe` **does not change** — write `vAIbe-digest is...`, not `VAIbe-digest is...`
- In URLs and repository names lowercase is allowed: `vaibe-digest` (platform limitation)
- In vault directory names: `vAIbe-bots`, `vAIbe-OS` — per the standard
