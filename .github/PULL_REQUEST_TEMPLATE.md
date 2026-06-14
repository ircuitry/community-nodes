<!-- Thanks for sharing a node. Quick checklist: -->

## New / updated node

- **typeId:**
- **what it does:**

### Checklist

- [ ] One file `nodes/<typeId>.ircnode`, named after its `typeId`.
- [ ] `python3 tools/build_index.py` passes locally (or let CI check it).
- [ ] No secrets baked in; reads keys from env or `{{secret.name}}`.
- [ ] I read the code and it is safe and useful.
- [ ] I license this under the repo's MIT license.

<!-- index.json is rebuilt automatically after merge; you do not need to edit it. -->
