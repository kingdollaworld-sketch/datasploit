from __future__ import annotations

import ipaddress
from typing import Optional

import tldextract
import validators
from email_validator import EmailNotValidError, validate_email

from .types import TargetType


def classify_target(target: str) -> TargetType:
    """Classify the user supplied target into one of the supported types."""
    target = target.strip()

    ip_obj = parse_ip(target)
    if ip_obj and not ip_obj.is_loopback:
        return TargetType.IP

    target_type = _classify_email(target)
    if target_type:
        return target_type

    target_type = _classify_domain(target)
    if target_type:
        return target_type

    return TargetType.USERNAME


def parse_ip(target: str) -> Optional[ipaddress._BaseAddress]:  # type: ignore[name-defined]
    try:
        return ipaddress.ip_address(target)
    except ValueError:
        return None


def is_private_ip(target: str) -> bool:
    ip = parse_ip(target)
    if not ip:
        return False
    return ip.is_loopback or ip.is_private


def _classify_email(target: str) -> Optional[TargetType]:
    try:
        validate_email(target)
        return TargetType.EMAIL
    except EmailNotValidError:
        return None


def _classify_domain(target: str) -> Optional[TargetType]:
    if validators.domain(target):
        return TargetType.DOMAIN

    extracted = tldextract.extract(target)
    if extracted.domain and extracted.suffix:
        return TargetType.DOMAIN
    return None
