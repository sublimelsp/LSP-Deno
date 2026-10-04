from __future__ import annotations

from LSP.plugin import AbstractPlugin
from LSP.plugin import register_plugin
from LSP.plugin import Request
from LSP.plugin import text_document_identifier
from LSP.plugin import unregister_plugin
from typing import Any
from typing import Callable
from typing import Mapping
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

    def on_pre_server_command(self, command: Mapping[str, Any], done_callback: Callable[[], None]) -> bool:
        cmd = command["command"]
        if cmd == "deno.cache":
            session = self.weaksession()
            if session:
                view = session.window.active_view()
                if view:
                    referrer = session.config.map_client_path_to_server_uri(view.file_name() or "")
                    params = {"referrer": {"uri": referrer}, "uris": list(map(text_document_identifier, command["arguments"][0]))}
                    request = Request("deno/cache", params, view, progress=True)
                    session.send_request_task(request).then(lambda _: done_callback())
                    return True
        return False


def plugin_loaded() -> None:
    register_plugin(Deno)


def plugin_unloaded() -> None:
    unregister_plugin(Deno)
