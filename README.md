# Clínica Espaço Autoestima - Sistema de agendamento

Aplicação desenvolvida especificamente para uma clínica de estética chamada "Espaço Autoestima" que visa o cadastro e agendamento de clientes com suas respectivas sessões, horário e os(as) profissionais que irão tratá-los. Assim como, cadastro de produtos que serão utilizados nas sessões, controle de estoque, entre outros. Esse projeto se refere à disciplina de "Software Product: Analysis and Specification" do 4° semestre do curso de Análise e Desenvolvimento de Sistemas da Faculdade Impacta.

## Integrantes
- Anderson Tengan Amador;
- David Castanheira de Souza;
- Letícia Nunes de Lima;

## Tecnologias 
A linguagem back-end responsável pelas regras de negócio e lógica da aplicação em questão é o **[Python](https://docs.python.org/pt-br/3/tutorial/)**:
* O framework web utilizado é **[Flask](https://flask.palletsprojects.com/en/3.0.x/)** que permite que a construção de aplicações Web de maneira simples e objetiva com a capacidade de escalar para aplicações complexas;
* Neste projeto, utilizamos esse framework para criar páginas web dinâmicas através de rotas, pois facilita a criação de endpoints e a integração com bancos de dados, tornando o desenvolvimento do backend eficiente e organizado;
* Para a prototipação e design das telas do projeto, está sendo utilizado o **[Figma](https://www.figma.com/design/VEhO4SsuqNKRqIPCCrhl0K/Espaço-Autoestima-Prototipos?node-id=0-1&node-type=canvas&t=mEEwngDu1dxQ5xk9-0)**.

## Execução da aplicação
Para executá-la localmente, é necessário se certificar de que o **[Docker](https://www.docker.com/products/docker-desktop/)** está instalado na sua máquina. Para isso (caso esteja utilizando Windows), foi-se necessária a instalação do [Windows Subsystem Linux]([https://learn.microsoft.com/pt-br/windows/wsl/install]):

Feito isso, execute o comando abaixo:
```
docker compose up -d
```
Em caso de uma eventual alteração ou restabelecimento respectivamente:
```
docker compose stop
docker compose down 
```

## Contribuição
Contribuições são sempre bem-vindas! Se você tiver ideias para melhorar este projeto, sinta-se à vontade para abrir uma issue ou enviar um pull request.