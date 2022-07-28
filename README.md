
# Service BNDES API

API para distribuição e controle de dados da aplicação [Service BNDES API](https://github.com/hexgis/service_bndes_api).

Utiliza o formato Rest para comunicação e entrega de dados.

## Construindo o ambiente de desenvolvimento

### Docker

Neste seguimento é descrito como construir o ambiente de desenvolvimento do Service BNDES API utilizando docker contêiner com docker-compose, portanto, verifique se o seu computador possui o **docker** e o **docker-compose** instalados.

---
> **NOTA**: Para verificar se o **docker** e o **docker-compose** estão instalados, utilize os comandos a seguir no terminal do Ubuntu: `$ docker -v` para o **docker** e `$ docker-compose -v` para o **docker-compose**.
>
---
**Alterando informações de environment [docker-compose.yml](docker-compose.yml)**

Para algumas funcionalidades do Service BNDES API é necessário a integração com outros serviços, portanto, o arquivo de configuração das variáveis de ambiente (docker-compose.yml) deverá ser modificado com as informações necessárias para a conexão.

Como as variáveis são dinâmicas, cada desenvolvedor deverá preenchê-las com as informações do ambiente de desenvolvimento em que está trabalhando.

Abaixo segue a lista de serviços e suas respectivas variáveis a serem alteradas na sessão de desenvolvimento (**dev**) do arquivo **docker-compose.yml**.

---

> **NOTA**:  As informações abaixo, serão utilizadas para alterar o arquivo [docker-compose.yml](docker-compose.yml):
>
> - **NOME-DO-CONTÊINER** -> Nome gerado automaticamente pelo docker ao construir um contêiner. Para encontrá-lo digite o comando abaixo:
> `$ docker ps -a`
>
> >O nome do contêiner está descrito na coluna *NAMES*.
>
> - **IP-LOCAL** -> É o número de IP local do computador em que o serviço será construído. No Ubuntu, utilize o comando `$ ip addr` para encontrar esta informação.
>
> > Caso sinta dificuldade em encontrar o valor correto, contate o seu administrador de redes.
>
> - **PORTA-DO-SERVIÇO** -> É o número da porta em que o serviço destino está usando. Para encontrá-la, verifique o arquivo **docker-compose.yml do serviço a ser integrado** conforme exemplo abaixo:
>  
> ```yaml
> Arquivo docker-compose.yml do serviço a ser integrado
> dev:
>  ...
>     ports:
>         - "8888:9999"
> ```
>
> > Neste caso a **PORTA-DO-SERVIÇO** terá o valor 8888.
>
> - **TOKEN-GERADO-PELO-SERVIÇO** -> Chave de autenticação gerada pelo Django REST Framework. Para gerar esta chave, digite o comando abaixo quando o serviço a ser integrado estiver sendo executado:
> `$ docker exec -it NOME-DO-CONTÊINER python manage.py drf_create_token root`
>

---
### Executando contêiner

```bash
docker-compose up --build dev
```

> **NOTA**: Se apresentar o erro:
>
> ```bash
> django.db.utils.OperationalError: could not connect to server: Connection refused
>     Is the server running on host "db" (IP-LOCAL) and accepting
>     TCP/IP connections on port 5432?
> ```
>
> Execute o comando `docker-compose up --build dev` novamente.

---

### Carga de dados

Executa a carga inicial de dados na aplicação.

---

> **NOTA**: Deve ser executada em outro terminal.

---

Execute os comandos abaixo no terminal para fazer a carga de dados completa:

```bash
docker exec NOME-DO-CONTÊINER python manage.py loaddata */fixtures/*.yaml
docker exec NOME-DO-CONTÊINER python manage.py loaddata fixtures/*.yaml
```

---

**Executando contêiner para debug de sistema**:

```bash
docker-compose run --service-ports dev
```

---
