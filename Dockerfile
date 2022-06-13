#
# Ambiente utilizado apenas para testar o playbook do Ansible
#

FROM fedora:36

# docker build -t myfedora .

RUN dnf update -y && \
    dnf install -y \
        ansible \
        git \
        procps-ng
