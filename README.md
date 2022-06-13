# ansible-setup-workstation <!-- omit in toc -->

Automatiza a configurção inicial da minha estação de trabalho.

_Automate setup of my workstation._

```raw
- // TODO: documentar como o projeto foi criado
- // TODO: documentar como os testes foram configurado com o molecule
```

- [Executar o playbook](#executar-o-playbook)
- [Testes automatizados](#testes-automatizados)
  - [Versões que foram usadas](#versões-que-foram-usadas)
  - [Instalar o Ansible](#instalar-o-ansible)
  - [Configurar o virtualenv do Python](#configurar-o-virtualenv-do-python)
  - [Instalar o Molecule](#instalar-o-molecule)
  - [Executar os testes](#executar-os-testes)
- [Ansible](#ansible)
- [Plugins do Ansible para o vscode](#plugins-do-ansible-para-o-vscode)
- [Links](#links)

## Executar o playbook

```bash
# instalar o ansible
sudo dnf install ansible

# executar o playbook
ansible-playbook playbook.yml
```

## Testes automatizados

Os testes do playbook do Ansible são feitos com o [Molecule](https://molecule.readthedocs.io/en/latest/). Primeira vamos configurar o ambiente e em seguida rodar os testes.

### Versões que foram usadas

- Python 3.10.4
- Docker Community 20.10.15

### Instalar o Ansible

```bash
sudo dnf install ansible
```

### Configurar o virtualenv do Python

```bash
pip install virtualenv
```

> 📝 Se aparecer o warnning
>
> ```log
> WARNING: The script virtualenv is installed in '/home/mhagnumdw/.local/bin' which is not on PATH.
> Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
> ```
>
> É preciso adicionar a pasta acima no `PATH`. No arquivo `~/.zshrc` (ou `/.bashrc`) adicionar
>
> ```bash
> export PATH=$HOME/.local/bin:$PATH
> ```
>
> E recarregar com o comando `source ~/.zshrc`.

Entrar na pasta do projeto e criar o ambiente virtual

```bash
virtualenv .venv

# ou, para especificar a versão do python
virtualenv -p <PATH_DO_EXECUTAVEL_DO_PYTHON>\python .venv
```

> 📝 `pip list` nesse momento vai exibir todas as dependências instaladas globalmente.

Agora vamos ativar o ambiente virtual do python

```zsh
source .venv/bin/activate
# o PS1 (prompt) deve mudar após esse comando
```

> 📝 Agora o `pip list` nesse momento vai exibir apenas as dependências do ambiente virtual.

Para sair do ambiente virtual, basta executar

```bash
deactivate
# novamente o PS1 (prompt) deve mudar após esse comando
```

### Instalar o Molecule

```zsh
pip install "molecule[docker]" ansible-core
```

### Executar os testes

```bash
# rodar o teste automatizado
molecule test
# o molecule vai subir um container docker especificado
# no arquivo molecule.yml, rodar o playbook e checar
# se tudo ocorreu bem

# rodar o teste sem destruir o container ao final do teste
# (bom pra explorar algo dentro do container)
molecule test --destroy=never

# rodar apenas o teste em si e sem destruir o container (mais rápido)
# (bom pra explorar algo dentro do container)
molecule coverage
```

## Ansible

Alguns arquivos relevantes

- /etc/ansible/hosts
- /etc/ansible/ansible.cfg

Lista de módulos do Ansible

- na web: <https://docs.ansible.com/ansible/2.9/modules/list_of_all_modules.html>
- consultando localmente: `ansible-doc -l`

## Plugins do Ansible para o vscode

- [Ansible, by RedHat](https://marketplace.visualstudio.com/items?itemName=redhat.ansible)
- [VSCode snippets for Ansible](https://marketplace.visualstudio.com/items?itemName=MattiasBaake.vscode-snippets-for-ansible)

## Links

- <https://fedoramagazine.org/using-ansible-setup-workstation/>
- <https://github.com/caiodelgadonew/tools>
- <https://www.youtube.com/watch?v=GfOj2wgxyF4>
- <https://www.youtube.com/watch?v=bG2kX7W_s0c>
- Playbook vs Roles: <https://stackoverflow.com/questions/32101001/ansible-playbooks-vs-roles#32101316>
