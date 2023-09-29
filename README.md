# LSP-Deno

A convenience package to take advantage of the bundled language server present in the Deno runtime.

To use this package, you must have:

- The [LSP](https://packagecontrol.io/packages/LSP) package.
- A [Deno runtime](https://deno.land).

# Applicable Selectors

The Deno language server operates on the following base scopes:

- `source.ts.react`
- `source.tsx`
- `source.ts`
- `source.js.react`
- `source.jsx`
- `source.js`

# Configuration

The server **does not automatically start** for the scopes listed above - it's expected that you enable it for a given project by running `LSP: Enable Language Server in Project` from the _Command Palette_.

It is recommended to disable LSP-typescript when working with LSP-deno.
Run `LSP: Disable Language Server in Project` from the _Command Palette_, then select LSP-typescript.

You may edit the default settings by running `Preferences: LSP-Deno Settings` from the _Command Palette_.

