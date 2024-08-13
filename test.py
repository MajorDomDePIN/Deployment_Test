import subprocess
import time

# Schlüssel und deren Herkunft
keys_with_source = [
    {"key": "0x7726827caac94a7f9e1b160f7ea819f172f7b6f9d2a97f992c38edeab82d4110", "source": "documentation"},
    {"key": "0xac1e735be8536c6534bb4f17f06f6afc73b2b5ba84ac2cfb12f7461b20c0bbe3", "source": "documentation"},
    {"key": "0xd293c684d884d56f8d6abd64fc76757d3664904e309a0645baf8522ab6366d9e", "source": "documentation"},
    {"key": "0x850683b40d4a740aa6e745f889a6fdc8327be76e122f5aba645a5b02d0248db8", "source": "documentation"},
    {"key": "0xf12e28c0eb1ef4ff90478f6805b68d63737b7f33abfa091601140805da450d93", "source": "documentation"},
    {"key": "0xe667e57a9b8aaa6709e51ff7d093f1c5b73b63f9987e4ab4aa9a5c699e024ee8", "source": "documentation"},
    {"key": "0x28a574ab2de8a00364d5dd4b07c4f2f574ef7fcc2a86a197f65abaec836d1959", "source": "documentation"},
    {"key": "0x74d8b3a188f7260f67698eb44da07397a298df5427df681ef68c45b34b61f998", "source": "documentation"},
    {"key": "0xbe79721778b48bcc679b78edac0ce48306a8578186ffcb9f2ee455ae6efeace1", "source": "documentation"},
    {"key": "0x3eb15da85647edd9a1159a4a13b9e7c56877c4eb33f614546d4db06a51868b1c", "source": "documentation"},
    {"key": "0x3d3cbc973389cb26f657686445bcc75662b415b656078503592ac8c1abb8810e", "source": "node"},
    {"key": "0x509ca2e9e6acf0ba086477910950125e698d4ea70fa6f63e000c5a22bda9361c", "source": "node"},
    {"key": "0x71781d3a358e7a65150e894264ccc594993fbc0ea12d69508a340bc1d4f5bfbc", "source": "node"},
    {"key": "0x379d31d4a7031ead87397f332aab69ef5cd843ba3898249ca1046633c0c7eefe", "source": "node"},
    {"key": "0x105de4e75fe465d075e1daae5647a02e3aad54b8d23cf1f70ba382b9f9bee839", "source": "node"},
    {"key": "0x7becc4a46e0c3b512d380ca73a4c868f790d1055a7698f38fb3ca2b2ac97efbb", "source": "node"},
    {"key": "0xe0415469c10f3b1142ce0262497fe5c7a0795f0cbfd466a6bfa31968d0f70841", "source": "node"},
    {"key": "0x4d91647d0a8429ac4433c83254fb9625332693c848e578062fe96362f32bfe91", "source": "node"},
    {"key": "0x41c9f9518aa07b50cb1c0cc160d45547f57638dd824a8d85b5eb3bf99ed2bdeb", "source": "node"},
    {"key": "0xb0680d66303a0163a19294f1ef8c95cd69a9d7902a4aca99c05f3e134e68a11a", "source": "node"}
]

# Konfiguration
rpc_url = "http://127.0.0.1:8011"
contract_path = "src/SimpleStorage.sol:SimpleStorage"
max_attempts = 5
max_retries_per_key = 3
delay_between_attempts = 2  # Zeit in Sekunden zwischen den Versuchen

def deploy_contract(private_key):
    command = [
        "forge", "create", contract_path,
        "--private-key", private_key,
        "--rpc-url", rpc_url,
        "--legacy", "--zksync"
    ]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        if "Error:" in result.stderr:
            return False, result.stderr.strip()
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return False, e.stderr.strip()

def main():
    successful_keys = set()
    successful_outputs = {}

    for attempt in range(max_attempts):
        print(f"\nAttempt {attempt + 1}")
        for key_info in keys_with_source:
            key = key_info["key"]
            source = key_info["source"]
            
            if key in successful_keys:
                continue  # Überspringen, wenn der Schlüssel bereits erfolgreich getestet wurde
            
            print(f"Testing key {key} from {source}")
            success = False
            for retry in range(max_retries_per_key):
                print(f"  Retry {retry + 1}")
                success, output = deploy_contract(key)
                if success:
                    successful_keys.add(key)
                    successful_outputs[key] = (source, output)
                    break
                #time.sleep(5)  # Warte 5 Sekunden, bevor der nächste Retry gestartet wird
            if not success:
                print(f"  Failed to deploy contract with key {key} after {max_retries_per_key} retries.")
        # Warte zwischen den Versuchen
        if attempt < max_attempts - 1:  # Kein Delay nach dem letzten Versuch
            print(f"Waiting for {delay_between_attempts} seconds before the next attempt...")
            time.sleep(delay_between_attempts)
    
    # Zusammenfassung
    print("\nDeployment Ergebnisse:")
    if successful_keys:
        print("Erfolgreich:")
        for key in successful_keys:
            source, output = successful_outputs[key]
            print(f"Key: {key} (Source: {source})")
            print(f"Output: {output}")
    else:
        print("Keine erfolgreichen Deployments gefunden.")

if __name__ == "__main__":
    main()
