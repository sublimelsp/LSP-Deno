from LSP.plugin import AbstractPlugin
from LSP.plugin import register_plugin
from LSP.plugin import Request
from LSP.plugin import unregister_plugin
from LSP.plugin.core.typing import Callable


class Deno(AbstractPlugin):

    @classmethod
    def name(cls) -> str:
        return cls.__name__

    def on_open_uri_async(self, uri: str, callback: Callable[[str, str, str], None]) -> bool:
        if uri.startswith("deno:"):
            session = self.weaksession()
            if session:
                params = {"textDocument": {"uri": uri}}
                request = Request("deno/virtualTextDocument", params, progress=True)
                session.send_request_async(
                    request,
                    lambda response: callback(uri, response, 'Packages/JavaScript/TSX.sublime-syntax'),
                    lambda err: callback("ERROR", str(err), 'Packages/Text/Plain text.tmLanguage')
                )
                return True
        return False


def plugin_loaded() -> None:
    register_plugin(Deno)


def plugin_unloaded() -> None:
    unregister_plugin(Deno)
