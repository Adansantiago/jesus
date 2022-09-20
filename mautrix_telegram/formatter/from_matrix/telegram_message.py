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
from __future__ import annotations

from typing import Any, Type
from enum import Enum

from telethon.tl.types import (
    InputMessageEntityMentionName as InputMentionName,
    MessageEntityBlockquote as Blockquote,
    MessageEntityBold as Bold,
    MessageEntityBotCommand as Command,
    MessageEntityCode as Code,
    MessageEntityEmail as Email,
    MessageEntityItalic as Italic,
    MessageEntityMention as Mention,
    MessageEntityMentionName as MentionName,
    MessageEntityPre as Pre,
    MessageEntitySpoiler as Spoiler,
    MessageEntityStrike as Strike,
    MessageEntityTextUrl as TextURL,
    MessageEntityUnderline as Underline,
    MessageEntityUrl as URL,
    TypeMessageEntity,
)

from mautrix.util.formatter import EntityString, SemiAbstractEntity


class TelegramEntityType(Enum):
    """EntityType is a Matrix formatting entity type."""

    BOLD = Bold
    ITALIC = Italic
    STRIKETHROUGH = Strike
    UNDERLINE = Underline
    URL = URL
    INLINE_URL = TextURL
    EMAIL = Email
    PREFORMATTED = Pre
    INLINE_CODE = Code
    BLOCKQUOTE = Blockquote
    MENTION = Mention
    MENTION_NAME = InputMentionName
    COMMAND = Command
    SPOILER = Spoiler

    USER_MENTION = 1
    ROOM_MENTION = 2
    HEADER = 3


class TelegramEntity(SemiAbstractEntity):
    internal: TypeMessageEntity

    def __init__(
        self,
        type: TelegramEntityType | Type[TypeMessageEntity],
        offset: int,
        length: int,
        extra_info: dict[str, Any],
    ) -> None:
        if isinstance(type, TelegramEntityType):
            if isinstance(type.value, int):
                raise ValueError(f"Can't create Entity with non-Telegram EntityType {type}")
            type = type.value
        self.internal = type(offset=offset, length=length, **extra_info)

    def copy(self) -> TelegramEntity:
        extra_info = {}
        if isinstance(self.internal, Pre):
            extra_info["language"] = self.internal.language
        elif isinstance(self.internal, TextURL):
            extra_info["url"] = self.internal.url
        elif isinstance(self.internal, (MentionName, InputMentionName)):
            extra_info["user_id"] = self.internal.user_id
        return TelegramEntity(
            type(self.internal),
            offset=self.internal.offset,
            length=self.internal.length,
            extra_info=extra_info,
        )

    def __repr__(self) -> str:
        return str(self.internal)

    @property
    def offset(self) -> int:
        return self.internal.offset

    @offset.setter
    def offset(self, value: int) -> None:
        self.internal.offset = value

    @property
    def length(self) -> int:
        return self.internal.length

    @length.setter
    def length(self, value: int) -> None:
        self.internal.length = value


class TelegramMessage(EntityString[TelegramEntity, TelegramEntityType]):
    entity_class = TelegramEntity

    @property
    def telegram_entities(self) -> list[TypeMessageEntity]:
        return [entity.internal for entity in self.entities]
