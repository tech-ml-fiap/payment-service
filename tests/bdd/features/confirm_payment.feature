Feature: Confirmar pagamento

  Scenario: Pedido pago muda status para PAID
    Given existe um pagamento pendente para o pedido 20
    When o provedor envia um webhook de pagamento PAID para o pedido 20
    Then o status do pagamento do pedido 20 é PAID
