# ircuitry community nodes

A shared library of drop-in **`.ircnode`** nodes for [ircuitry](https://github.com/ircuitry/ircuitry),
the visual IRCv3 bot builder. Browse them on the website, copy one, and paste it straight into the app.

> Browse and copy: **https://ircuitry.github.io/nodes**

Each node is a single JSON manifest that declares its pins, params, an icon, and either a small
script (Python or JavaScript) or a reusable subgraph. The app runs the script in a child process, so
a node can hit an API, crunch text, do math, format output, and so on.

## Use a node

Three ways, easiest first:

1. **Paste it (in-app):** copy a node from the [website](https://ircuitry.github.io/nodes), then in
   ircuitry open the Node Library and choose **Install from clipboard**. It installs instantly.
2. **Drag a file:** download the `.ircnode` and drag it onto the ircuitry canvas.
3. **Drop in the folder:** save the `.ircnode` into `~/ircuitry/nodes/` and restart the app.

Installed nodes appear in the Node Library alongside the built-ins.

> Scripted nodes run code on your machine. Read a node before installing it, the same as any snippet
> off the internet.

## Contribute a node

1. Add one `<typeId>.ircnode` file under [`nodes/`](nodes/).
2. Open a pull request. CI validates the manifest automatically.
3. After merge, `index.json` is rebuilt and the node shows up on the website.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the manifest format and a copy-paste template.

## What is in here

- [`nodes/`](nodes/) - the node manifests (`*.ircnode`).
- [`index.json`](index.json) - generated catalog the website reads. Do not edit by hand.
- [`tools/build_index.py`](tools/build_index.py) - validates every node and rebuilds the index.

## License

[MIT](LICENSE). Individual node authors retain credit via the optional `author` field in each manifest.
