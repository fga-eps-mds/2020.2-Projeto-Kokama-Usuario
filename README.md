[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_2020.2-Projeto-Kokama-Usuario&metric=alert_status)](https://sonarcloud.io/dashboard?id=fga-eps-mds_2020.2-Projeto-Kokama-Usuario)

# 2020.2-Projeto-Kokama-Usuario

### Configurar as variáveis de ambiente
* Criar um arquivo .env da api do projeto;
- SECRET_KEY=
- DEBUG=
- ALLOWED_HOSTS=
- ...

* Criar um arquivo .env do projeto;
 - POSTGRES_DB=
 - POSTGRES_USER=
- ...
* Tem que conter os seguintes links:
 - LEARN_MICROSERVICE_URL=http://seu_ip:8001/
 - TRANSLATE_MICROSERVICE_URL=http://seu_ip:8000/

## Execução

* Para executar a aplicação basta usar a chamada `make`
* Para entrar no container em execução, use `make enter`
