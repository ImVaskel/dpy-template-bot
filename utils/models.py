from __future__ import annotationsOptional

__all__ = ("Codeblock",)

class Codeblock:
    """
    Represents a discord codeblock

    Takes params ``code`` and ``lang``, which is optional.
    """
    def __init__(self, code: str, *, lang: str = "") -> None:
        self.code = code
        self.lang = lang
    
    def __str__(self) -> str:
        return f"```{self.lang}\n{self.code}```"