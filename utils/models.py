from __future__ import annotations
from typing import Optional

class Codeblock:
    """
    Represents a discord codeblock

    Takes params ``code`` and ``lang``, which is optional.
    """
    def __init__(self, code: str, *, lang: Optional[str] = None) -> None:
        self.code = code
        self.lang = lang
    
    def __str__(self) -> str:
        return f"```{self.lang}\n{self.code}```" if self.lang else f"```\n{self.code}```"