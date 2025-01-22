from DataManager import DataManager
from Usuario import Aluno, Servidor, Usuario
from Transferencia import Transferencia
from Extrato import Extrato
from Emprestimo import EmprestimoEstudantil, EmprestimoPessoal
from Saldo import Saldo
from Carteirinha import Carteirinha
import re
from datetime import datetime


class SistemaBancario:
    def __init__(self):
        self.data_manager = DataManager()
        self.usuarios = self.data_manager.carregar_dados()
        self.usuario_logado = None
    
    def validar_senha(self, senha):

        if len(senha) < 8:
            raise ValueError("A senha deve ter pelo menos 8 caracteres.")
        if not re.search(r"[A-Z]", senha):
            raise ValueError("A senha deve conter pelo menos uma letra maiúscula.")
        if not re.search(r"\d", senha):
            raise ValueError("A senha deve conter pelo menos um número.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", senha):
            raise ValueError("A senha deve conter pelo menos um caractere especial (!@#$%^&*(), etc.).")

        return True
    
    def autenticar_usuario(self, cpf, senha):

        for usuario in self.usuarios:
            if usuario.cpf == cpf and usuario.validar_senha(senha):
                return usuario
        return None

    def associar_recursos_ao_usuario(self, usuario):
        usuario.saldo = Saldo(usuario.numero_conta_corrente, callback_salvar=self._salvar_dados)
        usuario.carteirinha = Carteirinha(usuario.tipo_usuario(), nivel_fump=getattr(usuario, "nivel_fump", None))

        self.usuarios.append(usuario)
        self._salvar_dados()

    def _salvar_dados(self):
        self.data_manager.salvar_dados(self.usuarios)

    def fazer_login(self, cpf, senha):
        usuario = next((u for u in self.usuarios if u.cpf == cpf), None)
        if not usuario or not usuario.validar_senha(senha):
            raise ValueError("CPF ou senha inválidos.")
        self.usuario_logado = usuario
        return usuario

    def redefinir_senha(self, cpf, data_nascimento, nova_senha):
        if len(nova_senha) < 8:
            raise ValueError("A senha deve ter pelo menos 8 caracteres.")
        if not re.search(r"[A-Z]", nova_senha):
            raise ValueError("A senha deve conter pelo menos uma letra maiúscula.")
        if not re.search(r"\d", nova_senha):
            raise ValueError("A senha deve conter pelo menos um número.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", nova_senha):
            raise ValueError("A senha deve conter pelo menos um caractere especial (!@#$%^&*(), etc.).")
        usuario = next((u for u in self.usuarios if u.cpf == cpf), None)
        if not usuario:
            raise ValueError("CPF não encontrado.")
        if usuario.data_nascimento != data_nascimento:
            raise ValueError("Data de nascimento incorreta.")
        usuario._senha = nova_senha
        self._salvar_dados()

    def realizar_transferencia(self, cpf_destinatario, valor, senha):
        if not self.usuario_logado:
            raise ValueError("Nenhum usuário logado.")

        destinatario = next((u for u in self.usuarios if u.cpf == cpf_destinatario), None)
        if not destinatario:
            raise ValueError("Destinatário não encontrado.")

        transferencia = Transferencia(self.usuario_logado, destinatario, valor, senha)
        if not transferencia.executar():
            raise ValueError(transferencia.mensagem)

        self._salvar_dados()
        return transferencia

    def solicitar_emprestimo(self, tipo, valor, numero_parcelas):
        if not self.usuario_logado:
            raise ValueError("Nenhum usuário logado.")

        saldo = self.usuario_logado.saldo

        if tipo == "Estudantil":
            emprestimo = EmprestimoEstudantil(valor, numero_parcelas)
        elif tipo == "Pessoal":
            emprestimo = EmprestimoPessoal(valor, numero_parcelas)
        else:
            raise ValueError("Tipo de empréstimo inválido.")

        if emprestimo.validar_emprestimo(saldo):
            emprestimo.registrar_emprestimo(saldo)
            self._salvar_dados()
            return emprestimo
        else:
            raise ValueError("Empréstimo não aprovado. Verifique as condições.")

    def exibir_saldo(self):
        if not self.usuario_logado:
            raise ValueError("Nenhum usuário logado.")
        return self.usuario_logado.saldo.exibir_saldo()

    def exibir_extrato(self, filtro=None):
        if not self.usuario_logado:
            raise ValueError("Nenhum usuário logado.")
        extrato = self.usuario_logado.saldo.exibir_historico()
        return extrato

    def gerenciar_carteirinha(self, operacao, valor=None):
        if not self.usuario_logado:
            raise ValueError("Nenhum usuário logado.")
        carteirinha = self.usuario_logado.carteirinha

        if operacao == "adicionar_saldo" and valor is not None:
            carteirinha.adicionar_saldo(valor)
        elif operacao == "liberar_catraca":
            return carteirinha.liberar_catraca()
        else:
            raise ValueError("Operação inválida para a carteirinha.")
            
    def executar_transferencias_periodicas(self):
        data_atual = datetime.now()
        if data_atual.day != 5:
            return

        conta_origem = next(
            (u for u in self.usuarios if u.cpf == "12345678910"), None
        )
        if not conta_origem:
            print("Conta origem não encontrada para transferências periódicas.")
            return

        for usuario in self.usuarios:
            if isinstance(usuario, Aluno):
                if usuario.nivel_fump == "I":
                    valor = 700.0
                elif usuario.nivel_fump in ["II", "III"]:
                    valor = 500.0
                elif usuario.nivel_fump == "IV":
                    valor = 250.0
                else:
                    continue

                try:
                    self._realizar_transferencia_automatica(
                        conta_origem, usuario, valor, "Transferência mensal"
                    )
                except ValueError as e:
                    print(f"Erro ao transferir para {usuario.nome}: {e}")

        for usuario in self.usuarios:
            if isinstance(usuario, Servidor):
                valor = usuario.salario
                try:
                    self._realizar_transferencia_automatica(
                        conta_origem, usuario, valor, "Pagamento de salário"
                    )
                except ValueError as e:
                    print(f"Erro ao pagar salário para {usuario.nome}: {e}")

    def _realizar_transferencia_automatica(self, origem, destino, valor, descricao):
        if origem.saldo < valor:
            raise ValueError(f"Saldo insuficiente para transferir R$ {valor:.2f}")

        origem.saldo.debitar(valor)
        destino.saldo.creditar(valor)

        destino.saldo._registrar_historico(descricao, valor)
        print(
            f"Transferência de R$ {valor:.2f} realizada de {origem.nome} para {destino.nome}"
        )


        self._salvar_dados()
        

    def criar_conta(self, tipo_usuario, dados):
        dados = {k: v for k, v in dados.items() if k != "tipo"}
        novo_usuario = Usuario.criar_usuario(tipo_usuario, **dados)
        self.associar_recursos_ao_usuario(novo_usuario)
        self._salvar_dados()

