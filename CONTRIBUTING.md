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

## Building an AI tool node

A node can be a self-contained tool an Ask AI node calls - no `ai.tool` + sub-flow + Tool Reply
wiring. Give it a **`Tool` output** (that's the handle you wire into Ask AI's `tools`), make its **data
inputs the tool's arguments**, and put the **result on a data output**. When the model calls the tool,
ircuitry binds the model's arguments to your inputs by name, runs the node, and feeds the first data
output back to the model.

```json
{
  "typeId": "web.search",
  "title": "Web Search",
  "icon": "🔎",
  "category": "Ai",
  "description": "What the tool does - the model reads this to decide when to call it.",
  "inputs": [ { "name": "query", "kind": "Text" } ],
  "outputs": [ { "name": "tool", "kind": "Tool" }, { "name": "results", "kind": "Text" } ],
  "language": "python",
  "timeout": 15,
  "code": "import os; print('results for ' + (os.environ.get('QUERY') or ''))"
}
```

To use it: drop the node, wire its `tool` output into an **Ask AI** node's `tools` input, and the model
can call it. The tool's name shown to the model is the `typeId` (dots become underscores, so
`web.search` → `web_search`); its description and input names guide the model. The full
[`web.search`](nodes/web.search.ircnode) node in this repo is a working example (DuckDuckGo, no key).

Notes:
- A `Tool` output is only a handle - it carries no data; your result goes on a separate data output.
- Inputs left unwired are filled from the model's arguments; a wired input still takes the wire.
- The trigger context (`NICK`, `CHANNEL`, …) is available to tool code too.
- For keyed APIs (e.g. Google Custom Search), read the key from a param or `{{secret.NAME}}` - never
  bake it in.

## Test it locally

```bash
python3 tools/build_index.py        # validate all nodes + rebuild index.json
```

Or load the file in ircuitry: drag the `.ircnode` onto the canvas, or use Install from clipboard.

## Ground rules

- One node per file; safe, useful, no obfuscated or malicious code.
- No secrets baked in. Read keys from the environment or the app's secrets (`{{secret.name}}`).
- By submitting, you license your contribution under this repo's [MIT license](LICENSE).
