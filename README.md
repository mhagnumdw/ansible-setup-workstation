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
- [Máquina Virtual qemu/kvm (libvirt)](#máquina-virtual-qemukvm-libvirt)
  - [Conectar na Máquina Virtual criada](#conectar-na-máquina-virtual-criada)
- [Comandos variados](#comandos-variados)
- [Links](#links)

## Executar o playbook

```bash
# instalar o ansible
sudo dnf install ansible

# executar o playbook
ansible-playbook playbook.yml

# se precisar de root por conta do become=true
ansible-playbook playbook.yml --ask-become-pass
# ou
ansible-playbook playbook.yml -e "ansible_become_password=${PASS}"
```

## Testes automatizados

Os testes do playbook do Ansible são feitos com o [Molecule](https://molecule.readthedocs.io/en/latest/). Primeiro vamos configurar o ambiente e em seguida rodar os testes.

### Versões que foram usadas

- Python 3.10.4
- Docker Community 20.10.15

### Instalar o Ansible

```bash
sudo dnf install ansible

# dependências extras (para usar vm do kvm)
sudo dnf install libvirt-client guestfs-tools
# guestfs-tools, traz o comando: virt-resize
```

### Configurar o virtualenv do Python

// TODO: com o [asdf](https://github.com/asdf-vm/asdf) não daria pra gerenciar de modo mais simples? Se sim, colocar aqui uma seção com o `asdf`.

```bash
pip install virtualenv
```

> 📝 Se aparecer o warnning
>
> ```log
> WARNING: The script virtualenv is installed in '$HOME/.local/bin' which is not on PATH.
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
# Para funcionar com docker:
pip install "molecule[docker]" ansible-core

# Para funcionar com o libvirt (máquina virtual):
# pip install molecule ansible-core molecule-libvirt libvirt-python
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
molecule converge
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
- No terminal: `sudo dnf install python3-ansible-lint`

## Máquina Virtual qemu/kvm (libvirt)

```bash
# listar as vms
virsh list --all

# listar as interfaces de rede
virsh net-list --all

# obter informações de rede de uma vm
# no lugar de system pode ser session
# também existe o parâmetro --source com os valores: arp, agent e arp
virsh --connect qemu:///system domifaddr instance-name

# visualizar o xml de configuração de uma vm
virsh dumpxml instance-name
```

### Conectar na Máquina Virtual criada

Basta abrir o console do virt manager e logar na vm com o usuário `molecule` e senha `123`.

Via ssh com senha:

```bash
sshpass -p 123 \
  ssh -o "StrictHostKeyChecking no" \
  molecule@$( virsh --connect qemu:///system domifaddr instance | grep 52:54:00:ab:cd: | awk '{ print $4 }' | sed 's/\/.*//' )
```

Via ssh com chave:

```bash
# descobrir o IP
VM_IP=$(virsh --connect qemu:///system domifaddr instance | grep 52:54:00:ab:cd:)
# logar com a chave ssh que foi gerada na task "Generate OpenSSH key pair"
ssh -i $HOME/.cache/molecule/ansible-setup-workstation/default/id_ssh_rsa molecule@$VM_IP

# ou em uma única linha
ssh -i $HOME/.cache/molecule/ansible-setup-workstation/default/id_ssh_rsa \
  molecule@$( virsh --connect qemu:///system domifaddr instance | grep 52:54:00:ab:cd: | awk '{ print $4 }' | sed 's/\/.*//' )
```

## Comandos variados

```bash
# alterar a senha do usuário "molecule"
sudo passwd molecule

# conectar na vm com senha
sshpass -p 123 \
  ssh -o "StrictHostKeyChecking no" \
  molecule@$( virsh --connect qemu:///system domifaddr instance | grep 52:54:00:ab:cd: | awk '{ print $4 }' | sed 's/\/.*//' )

# conectar na vm com chave ssh
ssh -i $HOME/.cache/molecule/ansible-setup-workstation/default/id_ssh_rsa \
  molecule@$( virsh --connect qemu:///system domifaddr instance | grep 52:54:00:ab:cd: | awk '{ print $4 }' | sed 's/\/.*//' )

# destruir todo o ambiente
molecule test --destroy=never 2>&1 | gnomon --medium=3 --high=5

# destruir e rodar o teste (bom pra testar mudanças consecutivas)
molecule destroy 2>&1 | gnomon ; reset ; clear ; molecule converge 2>&1 | gnomon --medium=3 --high=5
```

## Links

- <https://fedoramagazine.org/using-ansible-setup-workstation/>
- <https://github.com/caiodelgadonew/tools>
- <https://www.youtube.com/watch?v=GfOj2wgxyF4>
- <https://www.youtube.com/watch?v=bG2kX7W_s0c>
- Playbook vs Roles: <https://stackoverflow.com/questions/32101001/ansible-playbooks-vs-roles#32101316>
- <https://docs.ansible.com/ansible/2.9/modules/list_of_all_modules.html>
- <https://stackoverflow.com/questions/45473463/pip-install-libvirt-python-fails-in-virtualenv#46366293>
