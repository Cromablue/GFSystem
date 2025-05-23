#!/bin/bash
SCRIPT_DIR="$(dirname "$0")"
echo "Qual o tipo deste nó?"
echo "1) Master"
echo "2) Slave 1"
echo "3) Slave 2"
read -p "Digite 1, 2 ou 3: " NODE_CHOICE

case $NODE_CHOICE in
  1) "$SCRIPT_DIR/deploy_master.sh" ;;
  2) "$SCRIPT_DIR/deploy_slave.sh" 192.168.1.101 slave1 ;;
  3) "$SCRIPT_DIR/deploy_slave.sh" 192.168.1.102 slave2 ;;
  *) echo "Opção inválida"; exit 1 ;;
esac
