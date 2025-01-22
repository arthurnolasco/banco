from abc import ABC, abstractmethod


class EmprestimoBase(ABC):
    def __init__(self, valor_emprestimo, numero_parcelas):
        self._valor_emprestimo = valor_emprestimo
        self._numero_parcelas = numero_parcelas
        self._taxa_juros = 0.05
        self._valor_parcela = self.calcular_valor_parcela()

    @property
    def valor_emprestimo(self):
        return self._valor_emprestimo

    @property
    def numero_parcelas(self):
        return self._numero_parcelas

    @property
    def taxa_juros(self):
        return self._taxa_juros

    @property
    def valor_parcela(self):
        return self._valor_parcela

    @abstractmethod
    def calcular_valor_parcela(self):
        pass

    @abstractmethod
    def validar_emprestimo(self, saldo):
        pass

    def registrar_emprestimo(self, saldo):
        saldo.creditar(self._valor_emprestimo)
        saldo._registrar_historico("Empréstimo recebido", self._valor_emprestimo)
        print(f"Empréstimo registrado: R$ {self._valor_emprestimo:.2f}")


class EmprestimoEstudantil(EmprestimoBase):
    def __init__(self, valor_emprestimo, numero_parcelas):
        super().__init__(valor_emprestimo, numero_parcelas)
        self._taxa_juros = 0.02

    def calcular_valor_parcela(self):
        valor_total = self._valor_emprestimo * (1 + self._taxa_juros * self._numero_parcelas)
        return valor_total / self._numero_parcelas

    def validar_emprestimo(self, saldo):
        if saldo.saldo < 0:
            print("Empréstimo negado: saldo negativo.")
            return False

        limite_parcela = saldo.saldo * 0.3 
        if self._valor_parcela > limite_parcela:
            print("Empréstimo negado: parcela excede 30% do saldo disponível.")
            return False

        return True


class EmprestimoPessoal(EmprestimoBase):
    def calcular_valor_parcela(self):
        valor_total = self._valor_emprestimo * (1 + self._taxa_juros * self._numero_parcelas)
        return valor_total / self._numero_parcelas

    def validar_emprestimo(self, saldo):
        if saldo.saldo < 0:
            print("Empréstimo negado: saldo negativo.")
            return False

        limite_parcela = saldo.saldo * 0.5
        if self._valor_parcela > limite_parcela:
            print("Empréstimo negado: parcela excede 50% do saldo disponível.")
            return False

       
