import time
from locust import HttpUser, task, between

class ProdutoUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        """
        Executado uma vez por usuário virtual.
        Faz login e cria o fornecedor de apoio necessário para os produtos.
        """
        res_login = self.client.post("/api/auth/login", json={
            "email": "teste-carga@floricultura.com",
            "senha": "teste-carga"
        })
       
        if res_login.status_code == 200:
            self.token = res_login.json().get("token")
            self.headers = {"Authorization": f"Bearer {self.token}"}
           
            cnpj_apoio = "88" + str(int(time.time() * 1000000))[-12:]
            payload_fornecedor = {
                "nome": "Fornecedor de Apoio para Produtos",
                "cnpj": cnpj_apoio,
                "endereco": "Rua de Apoio, 100",
                "cep": "86000000",
                "telefone": "43900000000"
            }
           
            res_forn = self.client.post("/api/fornecedores", json=payload_fornecedor, headers=self.headers)
           
            if res_forn.status_code in [200, 201]:
                
                self.fornecedor_id = res_forn.json().get("id") or res_forn.json().get("idFornecedor")
            else:
                self.fornecedor_id = None
                print(f"ERRO AO CRIAR FORNECEDOR DE APOIO: {res_forn.status_code}")
        else:
            self.token = None
            print(f"FALHA NO LOGIN: {res_login.status_code}")

    @task
    def fluxo_produto(self):
        if not self.token or not self.fornecedor_id:
            return

        sufixo_unico = str(int(time.time() * 1000000))[-6:]

        payload_produto = {
            "descricao": f"Produto Teste {sufixo_unico}",
            "valorVenda": 45.90,
            "quantidadeEstoque": 200,
            "validade": "2026-12-31",
            "fornecedor": { "id": self.fornecedor_id }
        }

        with self.client.post("/api/produtos", json=payload_produto, headers=self.headers, catch_response=True) as response:
            if response.status_code in [200, 201]:
                try:
                    produto_id = response.json().get("id") or response.json().get("idProduto")
                   
                    if produto_id:
                
                        res_get = self.client.get(
                            f"/api/produtos/{produto_id}",
                            headers=self.headers,
                            name="/api/produtos/[id]"
                        )
                        if res_get.status_code != 200:
                            response.failure(f"GET falhou: {res_get.status_code}")
                    else:
                        response.failure("ID do produto não retornado no POST")
                except Exception as e:
                    response.failure(f"Erro ao processar JSON: {e}")
            else:
                response.failure(f"POST falhou: {response.status_code} - {response.text}")
