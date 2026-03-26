import time
from locust import HttpUser, task, between

class ColaboradorUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):

        res_login = self.client.post("/api/auth/login", json={
            "email": "teste-carga@floricultura.com",
            "senha": "teste-carga"
        })

        if res_login.status_code == 200:
            self.token = res_login.json().get("token")
            self.headers = {"Authorization": f"Bearer {self.token}"}

            sufixo_cargo = str(int(time.time() * 1000))[-5:]
            payload_cargo = {
                "nomeCargo": f"Cargo Teste {sufixo_cargo}",
                "descricao": "Cargo gerado para suporte ao teste de colaboradores"
            }

            res_cargo = self.client.post("/api/cargos", json=payload_cargo, headers=self.headers)

            if res_cargo.status_code in [200, 201]:
                self.cargo_id = res_cargo.json().get("id") or res_cargo.json().get("idCargo")
            else:
                self.cargo_id = None
                print(f"ERRO AO CRIAR CARGO DE APOIO: {res_cargo.status_code}")
        else:
            self.token = None
            print(f"FALHA NO LOGIN: {res_login.status_code}")

    @task
    def fluxo_colaborador(self):
        if not self.token or not self.cargo_id:
            return

        semente_unica = str(int(time.time() * 1000000))

        matricula = semente_unica[-6:]
        cpf_unico = semente_unica[-11:]

        payload_colaborador = {
            "matricula": matricula,
            "nome": f"Colaborador {matricula}",
            "cpf": cpf_unico,
            "salario": 3500.00,
            "cargo": { "id": self.cargo_id }
        }

        with self.client.post("/api/colaboradores", json=payload_colaborador, headers=self.headers, catch_response=True) as response:
            if response.status_code in [200, 201]:
                try:
                    colab_id = response.json().get("id") or response.json().get("idColaborador")

                    if colab_id:
                        res_get = self.client.get(
                            f"/api/colaboradores/{colab_id}",
                            headers=self.headers,
                            name="/api/colaboradores/[id]"
                        )
                        if res_get.status_code != 200:
                            response.failure(f"GET falhou: Status {res_get.status_code}")
                    else:
                        response.failure("ID do colaborador não retornado no POST")
                except Exception as e:
                    response.failure(f"Erro ao processar JSON: {e}")
            else:
                response.failure(f"POST falhou: {response.status_code} - {response.text}")
