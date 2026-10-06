from __future__ import annotations

from LSP.plugin import command_handler
from LSP.plugin import Error
from LSP.plugin import LspPlugin
from LSP.plugin import parse_uri
from LSP.plugin import Promise
from LSP.plugin import Request
from LSP.plugin import uri_handler
from LSP.protocol import DocumentUri
from LSP.protocol import ExecuteCommandParams
from LSP.protocol import TextDocumentIdentifier
from pathlib import Path
from typing import Any
from typing import TypedDict
import re
import sublime
import urllib.parse


class VirtualTextDocumentParams(TypedDict):
    textDocument: TextDocumentIdentifier


# A failing test is reported as `name => ./main_test.ts:16:6` and stack frames as `at file:///path/main_test.ts:17:3`.
TEST_FILE_REGEX = r'(?:=> |at (?:.*\()?file://)(\S+?):(\d+):(\d+)'


class LspDenoPlugin(LspPlugin):

    @command_handler('deno.client.test')
    def on_client_test(self, arguments: list[Any] | None) -> Promise[None]:
        """Runs a single test. Sent by the "Run Test" and "Debug" code lenses with `[specifier, name, {inspect}]`."""
        session = self.weaksession()
        if not session or not arguments or len(arguments) < 2:
            return Promise.resolve(None)
        specifier, name = arguments[0], arguments[1]
        options = arguments[2] if len(arguments) > 2 and isinstance(arguments[2], dict) else {}
        scheme, file_path = parse_uri(specifier)
        if scheme != 'file':
            session.window.status_message(f'LSP-Deno: Cannot run tests from {specifier}')
            return Promise.resolve(None)
        settings = session.config.settings
        test_args: list[str] = list(settings.get('deno.codeLens.testArgs') or [])
        unstable = settings.get('deno.unstable')
        if isinstance(unstable, list):
            for feature in unstable:
                if (flag := f'--unstable-{feature}') not in test_args:
                    test_args.append(flag)
        if options.get('inspect'):
            test_args.append('--inspect-wait')
        if '--import-map' not in test_args and (import_map := (settings.get('deno.importMap') or '').strip()):
            test_args.extend(['--import-map', import_map])
        # Escape the same characters as JavaScript's RegExp syntax since Deno builds a RegExp from the filter.
        name_pattern = re.sub(r'[.*+?^${}()|[\]\\]', r'\\\g<0>', name)
        cmd = [session.config.command[0], 'test', *test_args, '--filter', f'/^{name_pattern}$/', file_path]
        working_dir = next(
            (folder.path for folder in session.get_workspace_folders() if Path(folder.path) in Path(file_path).parents),
            str(Path(file_path).parent))
        sublime.set_timeout(lambda: session.window.run_command('exec', {
            'cmd': cmd,
            'working_dir': working_dir,
            'file_regex': TEST_FILE_REGEX,
            'env': {'NO_COLOR': '1'},
            'kill_previous': True,
        }))
        return Promise.resolve(None)

    @command_handler('deno.client.showReferences')
    def on_client_show_references(self, arguments: list[Any] | None) -> Promise[None]:
        """
        Shows locations. Sent by the "references" and "implementations" code lenses with `[uri, position, locations]`.
        These are the same arguments as `editor.action.showReferences`, which LSP supports natively.
        """
        if not (session := self.weaksession()) or not arguments:
            return Promise.resolve(None)
        command: ExecuteCommandParams = {'command': 'editor.action.showReferences', 'arguments': arguments}
        return session.execute_command(command, view=session.window.active_view()).then(lambda _: None)

    @uri_handler('deno')
    def on_open_deno_uri(self, uri: DocumentUri, flags: sublime.NewFileFlags) -> Promise[sublime.Sheet | None]:
        session = self.weaksession()
        if not session:
            return Promise.resolve(None)
        # find_syntax_for_file will return "plain text" for unknown files
        syntax = sublime.find_syntax_for_file(urllib.parse.urlparse(uri).path)
        syntax_path = syntax.path if syntax else 'Packages/Text/Plain text.tmLanguage'
        params: VirtualTextDocumentParams = {'textDocument': {'uri': uri}}
        request: Request[VirtualTextDocumentParams, str] = Request('deno/virtualTextDocument', params, progress=True)

        def on_response(response: str | Error) -> Promise[sublime.Sheet | None]:
            if isinstance(response, Error):
                session.window.status_message(f'LSP-Deno: Failed to open {uri}: {response}')
                return Promise.resolve(None)
            return session.open_scratch_buffer(uri, response, syntax_path, flags).then(lambda view: view.sheet())

        return session.send_request_task(request).then(on_response)


def plugin_loaded() -> None:
    LspDenoPlugin.register()


def plugin_unloaded() -> None:
    LspDenoPlugin.unregister()
