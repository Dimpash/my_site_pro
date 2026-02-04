"""
mail_provider_detector.py

Manual CLI tool to detect email hosting provider
(Google Workspace vs Microsoft 365) by DNS records.

Usage:
    python mail_provider_detector.py
"""

import dns.resolver
import dns.exception


GOOGLE_MX_KEYWORDS = (
    "aspmx.l.google.com",
    "google.com",
)

OUTLOOK_MX_KEYWORDS = (
    "outlook.com",
    "mail.protection.outlook.com",
)

GOOGLE_SPF = "include:_spf.google.com"
OUTLOOK_SPF = "include:spf.protection.outlook.com"


def extract_domain(value: str) -> str:
    value = value.strip().lower()
    if "@" in value:
        return value.split("@", 1)[1]
    return value


def get_mx_records(domain: str) -> list[str]:
    try:
        answers = dns.resolver.resolve(domain, "MX", lifetime=3)
        return sorted(
            [str(r.exchange).rstrip(".").lower() for r in answers]
        )
    except dns.exception.DNSException:
        return []


def get_spf_record(domain: str) -> str | None:
    try:
        answers = dns.resolver.resolve(domain, "TXT", lifetime=3)
        for r in answers:
            txt = "".join(part.decode() for part in r.strings).lower()
            if txt.startswith("v=spf1"):
                return txt
    except dns.exception.DNSException:
        pass
    return None


def detect_provider(domain: str) -> dict:
    mx_records = get_mx_records(domain)

    for mx in mx_records:
        if any(key in mx for key in GOOGLE_MX_KEYWORDS):
            return {
                "provider": "Google Workspace",
                "signal": "MX",
                "mx_records": mx_records,
            }

        if any(key in mx for key in OUTLOOK_MX_KEYWORDS):
            return {
                "provider": "Microsoft 365 (Outlook)",
                "signal": "MX",
                "mx_records": mx_records,
            }

    spf = get_spf_record(domain)
    if spf:
        if GOOGLE_SPF in spf:
            return {
                "provider": "Google Workspace",
                "signal": "SPF",
                "mx_records": mx_records,
            }
        if OUTLOOK_SPF in spf:
            return {
                "provider": "Microsoft 365 (Outlook)",
                "signal": "SPF",
                "mx_records": mx_records,
            }

    return {
        "provider": "Unknown / Custom mail provider",
        "signal": "None",
        "mx_records": mx_records,
    }


def main():
    print("Email Provider Detector")
    print("-----------------------")
    print("Enter email address or domain (Ctrl+C to exit)\n")

    while True:
        try:
            user_input = input("Email / Domain: ").strip()
            if not user_input:
                continue

            domain = extract_domain(user_input)
            result = detect_provider(domain)

            print("\nResult")
            print("------")
            print(f"Domain   : {domain}")
            print(f"Provider : {result['provider']}")
            print(f"Signal   : {result['signal']}")

            if result["mx_records"]:
                print("MX records:")
                for mx in result["mx_records"]:
                    print(f"  - {mx}")
            else:
                print("MX records: none found")

            print()

        except KeyboardInterrupt:
            print("\nExiting.")
            break


if __name__ == "__main__":
    main()
