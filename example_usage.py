"""Example usage for Redact Unredact Session Vault."""
from client import RedactUnredactSessionVault
import json

vault = RedactUnredactSessionVault()

secrets = ["sk-proj-998877AABB", "postgres://admin:pass123@db.prod.internal:5432/core"]
prompt = "Connect to database postgres://admin:pass123@db.prod.internal:5432/core using key sk-proj-998877AABB"

masked_info = vault.register_and_mask(prompt, secrets)
print("Masked for LLM:", json.dumps(masked_info, indent=2))

llm_reply = f"Successfully verified connection to {masked_info['surrogate_tokens'][0]}"
unmasked_reply = vault.unmask(llm_reply)
print("Unmasked Reply:", unmasked_reply)
