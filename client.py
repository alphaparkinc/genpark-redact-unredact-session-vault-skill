"""Redact Unredact Session Vault.
100% Python Standard Library.
"""

class RedactUnredactSessionVault:
    """Bidirectional in-memory sensitive vault & surrogate token masker."""

    def __init__(self):
        self.vault = {}
        self.counter = 0

    def register_and_mask(self, text: str, secrets: list) -> dict:
        masked = text
        mapping = {}
        for secret in sorted(secrets, key=len, reverse=True):
            if secret in masked:
                self.counter += 1
                token = f"__VAULT_SECRET_{self.counter}__"
                self.vault[token] = secret
                mapping[token] = secret
                masked = masked.replace(secret, token)

        return {
            "masked_text": masked,
            "vault_tokens_count": len(mapping),
            "surrogate_tokens": list(mapping.keys())
        }

    def unmask(self, masked_text: str) -> str:
        restored = masked_text
        for token, original in self.vault.items():
            restored = restored.replace(token, original)
        return restored
