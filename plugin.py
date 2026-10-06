from __future__ import annotations

from LSP.plugin import AbstractPlugin
from LSP.plugin import register_plugin
from LSP.plugin import Request
from LSP.plugin import unregister_plugin
from typing import Callable
import sublime
import urllib.parse


class Deno(AbstractPlugin):

    @classmethod
    def name(cls) -> str:
        return cls.__name__

    def on_open_uri_async(self, uri: str, callback: Callable[[str, str, str], None]) -> bool:
        if uri.startswith("deno:"):
            if (session := self.weaksession()):
                params = {"textDocument": {"uri": uri}}
                request = Request("deno/virtualTextDocument", params, progress=True)
                # find_syntax_for_file will return "plain text" for unknown files
                if syntax := sublime.find_syntax_for_file(urllib.parse.urlparse(uri).path):
                    session.send_request_async(
                        request,
                        lambda response: callback(uri, response, syntax.path),
                        lambda err: callback("ERROR", str(err), 'Packages/Text/Plain text.tmLanguage')
                    )
                    return True
        return False


def plugin_loaded() -> None:
    register_plugin(Deno)


def plugin_unloaded() -> None:
    unregister_plugin(Deno)
