import random
import string
import uuid
def generate_qr_data(order_id: int, amount: float) -> str:
    """
    Gera uma string mockada para o QRCode, simulando a integração com Mercado Pago.
    """
    transaction_uuid = str(uuid.uuid4()).replace('-', '')
    order_id_str = f"{order_id:06d}"       # Ex.: 000123
    amount_str = f"{int(amount):03d}"       # Ex.: 030 (valor inteiro apenas para exemplo)
    client_name = ''.join(random.choices(string.ascii_uppercase, k=25))
    client_str = client_name.upper().ljust(25)[:25]  # Nome do cliente com 25 caracteres
    city = ''.join(random.choices(string.ascii_uppercase, k=7))
    city_str = city.upper().ljust(7)[:7]     # Cidade com 7 caracteres

    qr_data = (
        "000201010212"                      # Cabeçalho fixo
        "43650016COM.MERCADOLIBRE"            # Identificação do estabelecimento (exemplo)
        "020130" + transaction_uuid[:30] +    # Identificador único
        "040000" + order_id_str +             # ID do pedido
        "5303" + amount_str +                 # Valor do pedido
        "5802BR" +                          # País (BR)
        "5925" + client_str +                # Nome do cliente
        "6007" + city_str +                  # Cidade
        "6207" + "0503***" +                 # Dados adicionais fixos
        "6304" + "0B6D"                      # Checksum fixo para mock
    )
    return qr_data