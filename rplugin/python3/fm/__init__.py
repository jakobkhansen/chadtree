from pynvim import Nvim, autocmd, function, plugin

from .commands import (
    a_on_bufenter,
    a_on_filetype,
    c_clear,
    c_collapse,
    c_copy,
    c_copy_name,
    c_cut,
    c_delete,
    c_hidden,
    c_new,
    c_open,
    c_primary,
    c_refresh,
    c_rename,
    c_secondary,
    c_select,
)
from .consts import fm_filetype
from .keymap import keys
from .settings import initial as initial_settings
from .state import initial as initial_state


@plugin
class Main:
    def __init__(self, nvim: Nvim):
        user_settings = nvim.vars.get("fm_settings", None)
        user_icons = nvim.vars.get("fm_icons", None)
        settings = initial_settings(user_settings=user_settings, user_icons=user_icons)

        self.nvim = nvim
        self.state = initial_state(settings)
        self.settings = settings

        keys(self.nvim, self.settings)

    @function("FMopen")
    def fm_open(self, *_) -> None:
        """
        Folders -> toggle
        File -> open
        """

        c_open(self.nvim, state=self.state, settings=self.settings)

    @function("FMprimary")
    def primary(self, *_) -> None:
        """
        Folders -> toggle
        File -> open
        """

        self.state = c_primary(self.nvim, state=self.state, settings=self.settings)

    @function("FMsecondary")
    def secondary(self, *_) -> None:
        """
        Folders -> toggle
        File -> preview
        """

        self.state = c_secondary(self.nvim, state=self.state, settings=self.settings)

    @function("FMrefresh")
    def refresh(self, *_) -> None:
        """
        Redraw buffers
        """

        self.state = c_refresh(self.nvim, state=self.state, settings=self.settings)

    @function("FMcollapse")
    def collapse(self, *_) -> None:
        """
        Collapse folder
        """

        self.state = c_collapse(self.nvim, state=self.state, settings=self.settings)

    @function("FMhidden")
    def hidden(self, *_) -> None:
        """
        Toggle hidden
        """

        self.state = c_hidden(self.nvim, state=self.state, settings=self.settings)

    @function("FMcopyname")
    def copy_name(self, *_) -> None:
        """
        Copy dirname / filename
        """

        c_copy_name(self.nvim, state=self.state, settings=self.settings)

    @function("FMnew")
    def new(self, *_) -> None:
        """
        new file / folder
        """

        self.state = c_new(self.nvim, state=self.state, settings=self.settings)

    @function("FMrename")
    def rename(self, *_) -> None:
        """
        rename file / folder
        """

        self.state = c_rename(self.nvim, state=self.state, settings=self.settings)

    @function("FMclear")
    def clear(self, *_) -> None:
        """
        Clear selected
        """

        self.state = c_clear(self.nvim, state=self.state, settings=self.settings)

    @function("FMselect")
    def select(self, visual: int, *_) -> None:
        """
        Folder / File -> select
        """
        is_visual = visual == 1

        self.state = c_select(
            self.nvim, state=self.state, settings=self.settings, is_visual=is_visual
        )

    @function("FMdelete")
    def delete(self, visual: int, *_) -> None:
        """
        Delete selected
        """
        is_visual = visual == 1

        self.state = c_delete(
            self.nvim, state=self.state, settings=self.settings, is_visual=is_visual
        )

    @function("FMcut")
    def cut(self, visual: int, *_) -> None:
        """
        Cut selected
        """
        is_visual = visual == 1

        self.state = c_cut(
            self.nvim, state=self.state, settings=self.settings, is_visual=is_visual
        )

    @function("FMcopy")
    def copy(self, visual: int, *_) -> None:
        """
        Copy selected
        """
        is_visual = visual == 1

        self.state = c_copy(
            self.nvim, state=self.state, settings=self.settings, is_visual=is_visual
        )

    @autocmd("FileType", pattern=fm_filetype, eval="expand('<abuf>')")
    def on_filetype(self, buf: str) -> None:
        """
        Setup keybind
        """

        a_on_filetype(self.nvim, state=self.state, settings=self.settings, buf=int(buf))

    @autocmd("BufEnter", eval="expand('<abuf>')")
    def on_bufenter(self, buf: str) -> None:
        """
        Update background tasks
        """

        self.state = a_on_bufenter(
            self.nvim, state=self.state, settings=self.settings, buf=int(buf)
        )
