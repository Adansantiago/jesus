# mautrix-telegram - A Matrix-Telegram puppeting bridge
# Copyright (C) 2022 Tulir Asokan
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
from mautrix.util.async_db import Connection

from . import upgrade_table


@upgrade_table.register(description="Track first event ID in portals for infinite backfilling")
async def upgrade_v8(conn: Connection) -> None:
    await conn.execute("ALTER TABLE portal ADD COLUMN first_event_id TEXT")
    await conn.execute("ALTER TABLE portal ADD COLUMN next_batch_id TEXT")
