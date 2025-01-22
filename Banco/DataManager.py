import json
from Usuario import Aluno, Servidor
from Carteirinha import Carteirinha
from Saldo import Saldo

class DataManager:
    def __init__(self, arquivo_dados="dados_banco.json"):
        self._arquivo_dados = arquivo_dados

    def salvar_dados(self, usuarios):
        dados_para_salvar = [self._serializar_usuario(usuario) for usuario in usuarios]
        try:
            with open(self._arquivo_dados, "w", encoding="utf-8") as arquivo:
                json.dump(dados_para_salvar, arquivo, ensure_ascii=False, indent=4)
            print("Dados salvos com sucesso.")
        except IOError as e:
            print(f"Erro ao salvar os dados: {e}")

    def carregar_dados(self):
        try:
            with open(self._arquivo_dados, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
                return [self._desserializar_usuario(dado) for dado in dados]
        except FileNotFoundError:
            print("Nenhum arquivo de dados encontrado. Começando com dados vazios.")
            return []
        except IOError as e:
            print(f"Erro ao carregar os dados: {e}")
            return []

    def verificar_cpf_existente(self, cpf):
        usuarios = self.carregar_dados()
        return any(usuario.cpf == cpf for usuario in usuarios)

    @staticmethod
    def _serializar_usuario(usuario):
        """
        Serializa uma instância de `Aluno` ou `Servidor` para salvar em JSON.
        """
        base = {
            "tipo": usuario.tipo_usuario(),
            "nome": usuario.nome,
            "cpf": usuario.cpf,
            "data_nascimento": usuario.data_nascimento,
            "endereco": usuario.endereco,
            "senha": usuario._senha,
            "numero_conta_corrente": usuario.numero_conta_corrente,
            "numero_matricula": getattr(usuario, "numero_matricula", None),
            "saldo": usuario.saldo.saldo,
            "saldo_carteirinha": usuario.carteirinha.saldo_carteirinha,
            "extrato": usuario.saldo._extrato._transacoes
        }
        if isinstance(usuario, Aluno):
            base.update({
                "fumpista": usuario.fumpista,
                "nivel_fump": usuario.nivel_fump
            })
        elif isinstance(usuario, Servidor):
            base.update({"salario": getattr(usuario, "salario", None)})
        return base

    @staticmethod
    def _desserializar_usuario(dado):
        """
        Desserializa um dicionário JSON para uma instância de `Aluno` ou `Servidor`.
        """
        tipo = dado.get("tipo")
        if tipo == "Aluno":
            usuario = Aluno(
                nome=dado["nome"],
                cpf=dado["cpf"],
                data_nascimento=dado["data_nascimento"],
                endereco=dado["endereco"],
                senha=dado["senha"],
                numero_conta_corrente=dado["numero_conta_corrente"],
                numero_matricula=dado["numero_matricula"],
                fumpista=dado.get("fumpista", False),
                nivel_fump=dado.get("nivel_fump")
            )
        elif tipo == "Servidor":
            usuario = Servidor(
                nome=dado["nome"],
                cpf=dado["cpf"],
                data_nascimento=dado["data_nascimento"],
                endereco=dado["endereco"],
                senha=dado["senha"],
                numero_conta_corrente=dado["numero_conta_corrente"],
                salario=dado.get("salario", 0)
            )
        else:
            raise ValueError(f"Tipo de usuário desconhecido: {tipo}")

        usuario.saldo = Saldo(dado["numero_conta_corrente"])
        usuario.saldo._saldo = dado.get("saldo", 0)
        usuario.carteirinha = Carteirinha(usuario.tipo_usuario(), nivel_fump=dado.get("nivel_fump"))
        usuario.carteirinha._saldo_carteirinha = dado.get("saldo_carteirinha", 0.0)
        usuario.saldo._extrato._transacoes = dado.get("extrato", [])
        return usuario
