import hashlib
import hmac
import json
import os
import urllib.request
from datetime import datetime, timezone


def main():
    run_id = os.environ.get("GITHUB_RUN_ID", "")
    
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.") + \
                f"{datetime.now(timezone.utc).microsecond // 1000:03d}Z"

    payload = {
        "action_run_link": f"https://github.com/Bella63-glitch/b12-application/actions/runs/{run_id}",
        "email": "christabellahmuricho@gmail.com",
        "name": "Christabelah Nekesa Muricho",
        "repository_link": "https://github.com/Bella63-glitch/b12-application",
        "resume_link": "https://bella63-glitch.github.io/My-portfolio-/",
        "timestamp": timestamp,
    }

    body = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")

    secret = b"hello-there-from-b12"
    hex_digest = hmac.new(secret, body, hashlib.sha256).hexdigest()
    signature = f"sha256={hex_digest}"

    req = urllib.request.Request(
        url="https://b12.io/apply/submission",
        data=body,
        headers={
            "Content-Type": "application/json",
            "X-Signature-256": signature,
        },
        method="POST",
    )

    with urllib.request.urlopen(req) as response:
        result = response.read().decode("utf-8")
        data = json.loads(result)
        if data.get("success"):
            print(f"Receipt: {data.get('receipt')}")


if __name__ == "__main__":
    main()