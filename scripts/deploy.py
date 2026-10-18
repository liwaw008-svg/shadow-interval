from pathlib import Path
import hashlib, json, re, subprocess
from genlayer_py import create_account, create_client
from genlayer_py.chains import studionet

ROOT = Path(__file__).parents[1]
ENV = (ROOT.parents[3] / "accounts.env").read_text(encoding="utf-8")
KEY = re.search(r'^ACCOUNT_4_GENLAYER_PRIVATE_KEY\s*=\s*"?([^"\r\n]+)', ENV, re.M).group(1).strip()
code = (ROOT / "contracts" / "contract.py").read_text(encoding="utf-8")
client = create_client(chain=studionet, account=create_account(account_private_key=KEY))
tx = client.deploy_contract(code=code, args=[])
print("deploy_tx=" + str(tx), flush=True)
receipt = client.wait_for_transaction_receipt(transaction_hash=tx, wait_until="finalized", retries=180, interval=5000, full_transaction=True)
leaders = receipt.get("consensus_data", {}).get("leader_receipt") or []
leaders = [leaders] if isinstance(leaders, dict) else leaders
address = receipt.get("data", {}).get("contract_address") or receipt.get("to_address")
assert receipt.get("result_name") == "MAJORITY_AGREE", receipt
assert any(row.get("execution_result") == "SUCCESS" for row in leaders), receipt
assert address, receipt
result = {
    "account": "liwaw008-svg",
    "network": "StudioNet",
    "contractAddress": address,
    "deploymentTransaction": str(tx),
    "deploymentConsensus": "MAJORITY_AGREE",
    "deploymentExecution": "SUCCESS",
    "sourceSha256": hashlib.sha256(code.encode()).hexdigest(),
    "sourceCommit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
    "repository": "https://github.com/liwaw008-svg/shadow-interval",
}
(ROOT / "deployment.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2), flush=True)
