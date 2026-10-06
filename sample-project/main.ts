// Sample project for manually testing LSP-Deno. Open `sample-project.sublime-project` in Sublime Text.
//
// - `deno:` URIs (`@uri_handler('deno')`): "Goto Definition" on `console` below opens
//   `deno:/asset/lib.deno.shared_globals.d.ts` in a read-only tab.
// - `deno.cache` command: until the `jsr:` import is cached it shows a `not-installed-jsr` diagnostic.
//   The "Install ... and its dependencies" quick fix should make it go away.
//   To reset, delete the package from the Deno cache: `deno clean`.

// deno-lint-ignore no-import-prefix
import { exists } from "jsr:@std/fs@1";

console.log(await exists("."));
