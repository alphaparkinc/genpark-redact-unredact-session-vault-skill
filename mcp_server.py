"""MCP Server for Redact Unredact Session Vault.
100% Python Standard Library JSON-RPC.
"""
import sys
import json
from client import RedactUnredactSessionVault

vault = RedactUnredactSessionVault()

def main():
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")

            if method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "tools": [
                            {
                                "name": "register_and_mask",
                                "description": "Mask sensitive secrets with vault surrogate tokens",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "text": {"type": "string"},
                                        "secrets": {"type": "array"}
                                    },
                                    "required": ["text", "secrets"]
                                }
                            },
                            {
                                "name": "unmask",
                                "description": "Restore surrogate tokens to plaintext secrets from vault",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "masked_text": {"type": "string"}
                                    },
                                    "required": ["masked_text"]
                                }
                            }
                        ]
                    }
                }
            elif method == "tools/call":
                call_name = req.get("params", {}).get("name")
                args = req.get("params", {}).get("arguments", {})
                if call_name == "register_and_mask":
                    res = vault.register_and_mask(args.get("text", ""), args.get("secrets", []))
                elif call_name == "unmask":
                    res = {"restored_text": vault.unmask(args.get("masked_text", ""))}
                else:
                    res = {"error": "Unknown tool"}
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
                }
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
