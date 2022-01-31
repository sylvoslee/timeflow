from idom.server.sanic import PerClientStateServer
from sanic import Sanic, response
from pathlib import Path

from main import page as main_page
from sidebar import page as sidebar_page

app = Sanic(__name__)
HERE = Path(__file__).parent
app.static("/static", str(HERE / "tailwind/build"))
PerClientStateServer(
    sidebar_page,
    {
        "redirect_root_to_index": False,
    },
    app,
)


def run():
    app.run(
        host="0.0.0.0",
        port=8001,
        workers=1,
        debug=True,
    )


run()
