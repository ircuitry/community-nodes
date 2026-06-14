# Contributing a node

A node is one JSON file, `nodes/<typeId>.ircnode`. Name the file after the `typeId` (for example
`web.weather.ircnode` for typeId `web.weather`). Open a PR; CI runs `tools/build_index.py` and rejects
an invalid manifest before it can merge.

## Manifest format

```json
{
  "typeId": "web.example",
  "title": "Example",
  "subtitle": "community",
  "icon": "🧩",
  "category": "Action",
  "description": "One clear sentence about what it does and what it outputs.",
  "author": "your-github-handle",
  "tags": ["web", "fun"],
  "inputs": [
    { "name": "", "kind": "Exec" },
    { "name": "query", "kind": "Text" }
  ],
  "outputs": [
    { "name": "then", "kind": "Exec" },
    { "name": "result", "kind": "Text" }
  ],
  "params": [],
  "language": "python",
  "timeout": 12,
  "code": "import os\nq=(os.environ.get('QUERY') or os.environ.get('ARGS') or '').strip()\nprint('you said: ' + q)\n"
}
```

### Fields

- `typeId` (required) - unique id, dotted, lowercase, for example `web.weather`.
- `title` - shown on the node card. `subtitle` - small label, usually `community`.
- `icon` - one emoji. Or set `iconImage` to a base64 PNG (data only, no `data:` prefix) for a logo.
- `category` - one of `Event`, `Filter`, `Logic`, `Action`, `Data`, `Ai`, `Storage`.
- `description` - one helpful sentence.
- `author`, `tags` - optional; `author` is your credit on the website.
- `inputs` / `outputs` - pins. `kind` is one of `Exec`, `Text`, `User`, `Channel`, `Number`, `Bool`, `Tool`.
  The first `Exec` input is the trigger; the first `Exec` output fires when the node finishes.
- `code` + `language` (`python` or `js`), OR `subgraph` for a reusable flow.

### How a scripted node runs

Inputs and params arrive as UPPERCASE environment variables (a `query` input is `QUERY`), plus the
trigger context: `NICK`, `CHANNEL`, `MESSAGE`, `ARGS`, `COMMAND`, `BOTNICK`, and the first data input
as `INPUT`. Whatever you print to stdout becomes the output. Print a JSON object to fill named outputs;
print plain text to fill the first data output.

Keep scripts to the standard library where you can (no install step for users). Python uses `python3`,
JavaScript uses `node`.

## Test it locally

```bash
python3 tools/build_index.py        # validate all nodes + rebuild index.json
```

Or load the file in ircuitry: drag the `.ircnode` onto the canvas, or use Install from clipboard.

## Ground rules

- One node per file; safe, useful, no obfuscated or malicious code.
- No secrets baked in. Read keys from the environment or the app's secrets (`{{secret.name}}`).
- By submitting, you license your contribution under this repo's [MIT license](LICENSE).
