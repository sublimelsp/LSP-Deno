from __future__ import annotations

from LSP.plugin import Error
from LSP.plugin import LspPlugin
from LSP.plugin import Promise
from LSP.plugin import Request
from LSP.plugin import uri_handler
from LSP.protocol import DocumentUri
from LSP.protocol import TextDocumentIdentifier
from typing import TypedDict
import sublime
import urllib.parse


class VirtualTextDocumentParams(TypedDict):
    textDocument: TextDocumentIdentifier


class LspDenoPlugin(LspPlugin):

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
