class Transferencia:

    def __init__(self, remetente, destinatario, valor, senha):
        self.remetente = remetente
        self.destinatario = destinatario
        self.valor = valor
        self.senha = senha
        self.status = "Pendente"
        self.mensagem = ""

    def validar_transferencia(self):
        if not self.remetente.validar_senha(self.senha):
            self.status = "Rejeitada"
            self.mensagem = "Senha incorreta."
            return False

        if not self.remetente.saldo.debitar(self.valor):
            self.status = "Rejeitada"
            self.mensagem = "Saldo insuficiente para realizar a transferência."
            return False

        return True

    def executar(self):
        if self.validar_transferencia():
           
            self.destinatario.saldo.creditar(self.valor)
            self.status = "Aprovada"
            self.mensagem = "Transferência realizada com sucesso."
            self.remetente.saldo._registrar_historico("Transferência enviada", -self.valor)
            self.destinatario.saldo._registrar_historico("Transferência recebida", self.valor)
            return True

        return False

    def detalhes_transferencia(self):
        return {
            "remetente": self.remetente.nome,
            "destinatario": self.destinatario.nome,
            "valor": self.valor,
            "status": self.status,
            "mensagem": self.mensagem
        }
