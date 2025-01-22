from datetime import datetime
import json

class Extrato:
    def __init__(self):
        self._transacoes = []

    def adicionar_transacao(self, descricao, valor):
        transacao = {
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "descricao": descricao,
            "valor": valor
        }
        self._transacoes.append(transacao)
        return f"Transação registrada: {descricao} - R$ {valor:.2f}"

    def exibir_extrato(self, saldo_atual=None, filtro=None):
        transacoes_filtradas = self._filtrar_transacoes(filtro)

        extrato_str = ["=== Extrato da Conta ==="]
        for transacao in transacoes_filtradas:
            tipo = "Crédito" if transacao["valor"] > 0 else "Débito"
            extrato_str.append(f"{transacao['data']} - {tipo}: {transacao['descricao']} - R$ {abs(transacao['valor']):.2f}")
        if saldo_atual is not None:
            extrato_str.append(f"Saldo Atual: R$ {saldo_atual:.2f}")
        extrato_str.append("=======================")

        return "\n".join(extrato_str)

    def exportar_extrato(self, caminho_arquivo, saldo_atual=None, filtro=None, formato="txt"):
        try:
            transacoes_filtradas = self._filtrar_transacoes(filtro)

            if formato == "txt":
                with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
                    arquivo.write(self.exibir_extrato(saldo_atual, filtro))
            elif formato == "json":
                with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
                    dados = {
                        "transacoes": transacoes_filtradas,
                        "saldo_atual": saldo_atual
                    }
                    json.dump(dados, arquivo, ensure_ascii=False, indent=4)
            return f"Extrato exportado para {caminho_arquivo}"
        except IOError as e:
            return f"Erro ao exportar o extrato: {e}"

    def _filtrar_transacoes(self, filtro):
        if filtro is None:
            return self._transacoes

        transacoes_filtradas = self._transacoes

        if "tipo" in filtro:
            tipo = filtro["tipo"]
            transacoes_filtradas = [
                t for t in transacoes_filtradas
                if (t["valor"] > 0 and tipo == "Crédito") or (t["valor"] < 0 and tipo == "Débito")
            ]

        if "data_inicio" in filtro and "data_fim" in filtro:
            data_inicio = datetime.strptime(filtro["data_inicio"], "%d/%m/%Y")
            data_fim = datetime.strptime(filtro["data_fim"], "%d/%m/%Y")
            transacoes_filtradas = [
                t for t in transacoes_filtradas
                if data_inicio <= datetime.strptime(t["data"], "%d/%m/%Y %H:%M:%S") <= data_fim
            ]

        return transacoes_filtradas
