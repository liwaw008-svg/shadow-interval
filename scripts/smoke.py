from pathlib import Path
import json, re, time
from genlayer_py import create_account, create_client
from genlayer_py.chains import studionet
import genlayer_py.contracts.actions as contract_actions

# StudioNet currently expects the legacy explicit `method` calldata key.
def compatible_calldata(method=None, args=None, kwargs=None):
    payload = {}
    if method is not None:
        payload["method"] = method
    if args:
        payload["args"] = args
    if kwargs:
        payload["kwargs"] = kwargs
    return payload

contract_actions.make_calldata_object = compatible_calldata

ROOT = Path(__file__).parents[1]
ENV = (ROOT.parents[3] / "accounts.env").read_text(encoding="utf-8")


def secret(number):
    return re.search(rf'^ACCOUNT_{number}_GENLAYER_PRIVATE_KEY\s*=\s*"?([^"\r\n]+)', ENV, re.M).group(1).strip()


owner = create_account(account_private_key=secret(4))
reviewer = create_account(account_private_key=secret(5))
owner_client = create_client(chain=studionet, account=owner)
reviewer_client = create_client(chain=studionet, account=reviewer)
deployment = json.loads((ROOT / "deployment.json").read_text(encoding="utf-8"))
address = deployment["contractAddress"]
record_id = "SUN-" + str(int(time.time()))
installation = {"kind": "temporary fabric canopy", "height_m": "2.4", "orientation": "south-east edge", "purpose": "afternoon reading table"}
protected = {"use": "seedling propagation benches", "protected_start": 540, "protected_end": 720, "sensitivity": "retain direct morning light"}
timing = {"start": 780, "end": 1080}
transactions = {}


def finalized(client, name, function, args):
    tx = client.write_contract(address=address, function_name=function, args=args)
    print(name + "_tx=" + str(tx), flush=True)
    receipt = client.wait_for_transaction_receipt(transaction_hash=tx, wait_until="finalized", retries=180, interval=5000, full_transaction=True)
    leaders = receipt.get("consensus_data", {}).get("leader_receipt") or []
    leaders = [leaders] if isinstance(leaders, dict) else leaders
    assert receipt.get("result_name") == "MAJORITY_AGREE", receipt
    assert any(row.get("execution_result") == "SUCCESS" for row in leaders), receipt
    transactions[name] = str(tx)


finalized(owner_client, "draft", "draft_interval", [record_id, reviewer.address, "Reading canopy beside propagation tables", json.dumps(installation), json.dumps(protected), json.dumps(timing)])
finalized(reviewer_client, "screen", "screen_interval", [record_id])
record = owner_client.read_contract(address=address, function_name="get_interval", args=[record_id])
if record.get("verdict") != "CONFLICT":
    finalized(owner_client, "adopt", "adopt_interval", [record_id])
    record = owner_client.read_contract(address=address, function_name="get_interval", args=[record_id])
output = {"recordType": "synthetic planning rehearsal; not a legal daylight determination", "recordId": record_id, "contractAddress": address, "transactions": transactions, "readback": record}
(ROOT / "evidence" / "live-run.json").write_text(json.dumps(output, indent=2, default=str) + "\n", encoding="utf-8")
print(json.dumps(output, indent=2, default=str), flush=True)
