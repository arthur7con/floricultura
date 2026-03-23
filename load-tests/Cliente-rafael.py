from locust import HttpUser, task, between

class ClienteUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        res = self.client.post("/api/auth/login", json={
            "email": "teste-carga@floricultura.com",
            "senha": "teste-carga"
        })
        if res.status_code == 200:
            self.token = res.json().get("token")
        else:
            self.token = None
            print(f"FALHA NO LOGIN: {res.status_code} - {res.text}")

    @task
    def fluxo_registro_leitura(self):
        if not self.token:
            return

        headers = {"Authorization": f"Bearer {self.token}"}
        cpf_unico = str(int(time.time() * 1000000))[-11:]

        cliente = {
            "nome": "Cliente Teste",
            "email": f"teste_{cpf_unico}@floricultura.com",  # email único também!
            "dataNascimento": "1990-01-01",
            "endereco": "Rua Teste, 10",
            "cep": "86010100",
            "telefone": "4399999999",
            "cpf": cpf_unico
        }

        with self.client.post("/api/clientes", json=cliente, headers=headers, catch_response=True) as response:
            if response.status_code in [200, 201]:
                try:
                    data = response.json()
                    print(f"[DEBUG] POST response: {data}")  # <-- vê o JSON real aqui
                   
                    cliente_id = data.get("id") or data.get("codigo") or data.get("_id")

                    if cliente_id:
                        res_get = self.client.get(
                            f"/api/clientes/{cliente_id}",
headers=headers,
                            name="/api/clientes/[id]",
                            catch_response=True  # captura pra ver o erro
                        )
                        with res_get:
                            print(f"[DEBUG] GET status: {res_get.status_code}, body: {res_get.text[:200]}")
                            if res_get.status_code == 200:
                                res_get.success()
                                response.success()
                            else:
                                res_get.failure(f"GET falhou: {res_get.status_code}")
                                response.failure(f"GET falhou: {res_get.status_code}")
                    else:
                        response.failure(f"ID não encontrado. JSON: {data}")
                except Exception as e:
                    response.failure(f"Erro ao processar JSON: {str(e)}")
            else:
                response.failure(f"POST falhou: {response.status_code} - {response.text}")
