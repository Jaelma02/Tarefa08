import requests
from typing import List, Dict

# === CONFIGURAÇÃO ===
INFURA_URL = 'https://mainnet.infura.io/v3/e94cc1c9db1447b29ee88e7abf15b93e'
HEADERS = {'Content-Type': 'application/json'}

# === FUNÇÃO PARA OBTER TRANSAÇÕES DE UM BLOCO ===
def obter_transacoes_bloco(numero_bloco: int) -> List[Dict]:
    tag_hex = hex(numero_bloco)

    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getBlockByNumber",
        "params": [tag_hex, True],
        "id": 1
    }

    response = requests.post(INFURA_URL, json=payload, headers=HEADERS)
    data = response.json()

    if 'result' not in data or data['result'] is None:
        print(f"[ERRO] Não foi possível obter dados do bloco {numero_bloco}.")
        return []

    transacoes = [{
        'hash': tx['hash'],
        'from': tx['from'],
        'to': tx['to']
    } for tx in data['result']['transactions']]

    print(f"[INFO] Bloco {numero_bloco}: {len(transacoes)} transações obtidas.")

    return transacoes

# === FUNÇÃO PARA DETECTAR ATAQUE SANDUÍCHE ===
def is_sandwich(tx1: Dict, tx2: Dict, tx3: Dict) -> bool:
    if not tx1['to'] or not tx2['to'] or not tx3['to']:
        return False  # evita erros se to for None

    same_sender = tx1['from'].lower() == tx3['from'].lower()
    diff_victim = tx2['from'].lower() != tx1['from'].lower()
    same_to = tx1['to'].lower() == tx2['to'].lower() == tx3['to'].lower()
    return same_sender and diff_victim and same_to

# === FUNÇÃO PARA DETECTAR ATAQUES EM BLOCOS ===
def detectar_ataques_sanduiche(blocos: Dict[int, List[Dict]]) -> List[Dict]:
    ataques = []

    for bloco, transacoes in blocos.items():
        for i in range(len(transacoes) - 2):
            tx1 = transacoes[i]
            tx2 = transacoes[i + 1]
            tx3 = transacoes[i + 2]

            if is_sandwich(tx1, tx2, tx3):
                ataque = {
                    'bloco': bloco,
                    'TA1': tx1['hash'],
                    'TV': tx2['hash'],
                    'TA2': tx3['hash']
                }
                ataques.append(ataque)

    return ataques

# === FUNÇÃO PRINCIPAL ===
def main():
    # Blocos com ataques identificados (informados na descrição)
    ataques_identificados = [
        {
            'bloco': 16308191,
            'TA1': '0x155fd4919a33a9b41480ceed4a3a68eaa43b6608eb6c9657a63a97fecac396e7',
            'TV':  '0xbe2ac237061b744bd788485a10618c019c72c1ccb17356e8a1c52459499a8162',
            'TA2': '0xc2a441f1cc431b25b6acac08a5112e3545afdfb969a5f118a890f9e852f51a02'
        },
        {
            'bloco': 16308192,
            'TA1': '0x352c7857be785bb79599a552462349852928f7fc083b78eef856ef86c67b2000',
            'TV':  '0x025cd39223ed9f62194822bb6b8f6ac63a36a174fac048ebf759adde61f22c42',
            'TA2': '0xf71e4568e9cbb8f56aa91cf5ebc4372d6efa2ca8731543cb5fa82d26455f40f9'
        },
        {
            'bloco': 16308193,
            'TA1': '0xaaefe792a84e83093941693991674b6c3ded185ac911aebec674c9f719487274',
            'TV':  '0x5a229017bd804c94dcc0d2ae6a7e75486d170d41b3a42bae6760c05b62b33f45',
            'TA2': '0x7cfbcafbc597d06c88aaa46172de9e2e61ee4518c5bd286c95434f1df94e3e6d'
        },
        {
            'bloco': 16308204,
            'TA1': '0x396756239e7e8973dce9e25076d5eb218d233a3a2dd7272cb526914c978af975',
            'TV':  '0xd9b45ba96b29de922a2261c0ea435ed318d0b7a454c4a609de2bae2f16cca07c',
            'TA2': '0x70658cfc080eda48fff1f43466c3f35d2a3453f19d5c7ffd51b6d28fda64c5fa'
        },
        {
            'bloco': 16308205,
            'TA1': '0x2b87c2570a232b2b96d3e446a5d56abf1011067b57b2b9af4a03bb30baae613a',
            'TV':  '0x7a9985374cf3ec254f4b41a07bf2d81eaf859837a1577d38f21ccc046e53b71d',
            'TA2': '0xc934b62081aa17ef2ee7b35b6d1b58ac0b7d8958cc2bba43c44c1ee3c9378c07'
        },
        {
            'bloco': 16308207,
            'TA1': '0xd06b4769aed972bba99e6ca5b05c66e241a440f85c6636b5df157a07ec6033db',
            'TV':  '0xb5b85e94af0d37bf2b4bd2d3d5cbbb1fbe7b2d33492852a555c95651710f9a62',
            'TA2': '0xbada06a4aeeb30c2aea1b6b5273945ed4eff412677c73bf20d8f2ee4315a71ee'
        }
    ]

    with open("resultado.txt", "w") as f:
        f.write("=== Blocos com ataques identificados ===\n")
        for ataque in ataques_identificados:
            f.write(f"Bloco: {ataque['bloco']}\n")
            f.write(f"  TA1: {ataque['TA1']}\n")
            f.write(f"  TV : {ataque['TV']}\n")
            f.write(f"  TA2: {ataque['TA2']}\n")
            f.write('-' * 40 + '\n')

    # Blocos para análise de possíveis ataques
    bloco_inicio = 16530251
    bloco_fim = 16530263
    blocos_para_analisar = list(range(bloco_inicio, bloco_fim + 1))

    blocos_transacoes = {}

    for bloco in blocos_para_analisar:
        transacoes = obter_transacoes_bloco(bloco)
        if transacoes:
            blocos_transacoes[bloco] = transacoes

    ataques_detectados = detectar_ataques_sanduiche(blocos_transacoes)

    with open("resultado.txt", "a") as f:
        f.write("\n=== Resultados da análise automática ===\n")
        if not ataques_detectados:
            f.write("Nenhum ataque detectado nos blocos analisados.\n")
            print("[INFO] Nenhum ataque detectado nos blocos analisados.")
        else:
            for ataque in ataques_detectados:
                f.write(f"Bloco: {ataque['bloco']}\n")
                f.write(f"  TA1: {ataque['TA1']}\n")
                f.write(f"  TV : {ataque['TV']}\n")
                f.write(f"  TA2: {ataque['TA2']}\n")
                f.write('-' * 40 + '\n')
                print(f"[DETECÇÃO] Ataque detectado no bloco {ataque['bloco']}")

    print("[FINALIZADO] Resultado salvo em resultado.txt.")

if __name__ == "__main__":
    main()
