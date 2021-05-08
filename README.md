# LSP-Deno

A convenience package to take advantage of the bundled language server present in the Deno runtime.

To use this package, you must have:

- Sublime Text 4.
- The [LSP](https://packagecontrol.io/packages/LSP) package. (requires https://github.com/sublimelsp/LSP/pull/1620)
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

You may edit the default settings by running _Preferences: LSP-Deno Settings_ from the _Command Palette_.
