from __future__ import annotations

class Codeblock:
    """
    Represents a discord codeblock

    Takes params ``code`` and ``lang``, which is optional.
    """
    def __init__(self, code: str, *, lang: str = None) -> None:
        self.code = code
        self.lang = lang
    
    def __str__(self) -> str:
        return f"```{self.lang}\n{self.code}```" if self.lang else f"```\n{self.code}```"