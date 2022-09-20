# mautrix-telegram - A Matrix-Telegram puppeting bridge
# Copyright (C) 2021 Tulir Asokan
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from mautrix.util.logging.color import (
    MXID_COLOR,
    PREFIX,
    RESET,
    ColorFormatter as BaseColorFormatter,
)

TELETHON_COLOR = PREFIX + "35;1m"  # magenta
TELETHON_MODULE_COLOR = PREFIX + "35m"


class ColorFormatter(BaseColorFormatter):
    def _color_name(self, module: str) -> str:
        if module.startswith("telethon"):
            prefix, user_id, module = module.split(".", 2)
            return (
                f"{TELETHON_COLOR}{prefix}{RESET}."
                f"{MXID_COLOR}{user_id}{RESET}."
                f"{TELETHON_MODULE_COLOR}{module}{RESET}"
            )
        return super()._color_name(module)
