from __future__ import annotations

from enum import Enum
from typing import Dict


class TargetType(str, Enum):
    DOMAIN = "domain"
    EMAIL = "email"
    IP = "ip"
    USERNAME = "username"


CATEGORY_PACKAGES: Dict[TargetType, str] = {
    TargetType.DOMAIN: "domain",
    TargetType.EMAIL: "emails",
    TargetType.IP: "ip",
    TargetType.USERNAME: "username",
}

PREFIX_BY_CATEGORY: Dict[TargetType, str] = {
    TargetType.DOMAIN: "domain_",
    TargetType.EMAIL: "email_",
    TargetType.IP: "ip_",
    TargetType.USERNAME: "username_",
}
