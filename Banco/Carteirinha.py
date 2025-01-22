class Carteirinha:
    PRECO_PADRAO = 5.6
    PRECOS_FUMP = {
        "I": 0.0,
        "II": 1.0,
        "III": 1.0,
        "IV": 2.0
    }
    PRECO_PROFESSOR = 13.0

    def __init__(self, tipo_usuario, nivel_fump=None):
        self._saldo_carteirinha = 0.0
        self._historico = []
        self._tipo_usuario = tipo_usuario
        self._nivel_fump = nivel_fump
        self._custo_refeicao = self.definir_custo_refeicao()

    @property
    def saldo_carteirinha(self):
        return self._saldo_carteirinha

    @saldo_carteirinha.setter
    def saldo_carteirinha(self, valor):
        if not isinstance(valor, (int, float)) or valor < 0:
            raise ValueError("O saldo deve ser um número positivo.")
        self._saldo_carteirinha = valor

    @property
    def custo_refeicao(self):
        return self._custo_refeicao

    def definir_custo_refeicao(self):
        if self._tipo_usuario == "Professor":
            return self.PRECO_PROFESSOR
        elif self._tipo_usuario == "Aluno":
            return self.PRECOS_FUMP.get(self._nivel_fump, self.PRECO_PADRAO)
        return 20.0 
    def adicionar_saldo(self, valor):
        if not isinstance(valor, (int, float)) or valor <= 0:
            raise ValueError("O valor para recarga deve ser um número positivo.")
        self.saldo_carteirinha += valor
        print(f"Saldo da carteirinha atualizado: R$ {self.saldo_carteirinha:.2f}")

    def liberar_catraca(self, categoria_acesso):
        if categoria_acesso in self.PRECOS_FUMP:
            valor = self.PRECOS_FUMP[categoria_acesso]
        else:
            valor = self.PRECO_PROFESSOR

        if self.saldo_carteirinha < valor:
            return f"Saldo insuficiente na carteirinha. Valor necessário: R$ {valor:.2f}"

        self.saldo_carteirinha -= valor
        self._registrar_historico("Débito: Acesso ao RU", valor)
        return f"Catraca liberada. R$ {valor:.2f} deduzidos da carteirinha."

    def exibir_saldo(self):
        return self.saldo_carteirinha

    def _registrar_historico(self, descricao, valor):
        self._historico.append({"descricao": descricao, "valor": valor})

    def exibir_historico(self):
        historico = [
            f"{'Crédito' if mov['valor'] > 0 else 'Débito'}: {mov['descricao']} - R$ {abs(mov['valor']):.2f}"
            for mov in self._historico
        ]
        return "\n".join(["=== Histórico da Carteirinha ==="] + historico + ["=============================="])
