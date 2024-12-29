## Iniciar os terminais dos hosts
   quando iniciar ir para o dentro da pasta cifar10-real-world e dar o comando
   export PYTHONPATH=${PWD}/..
   fazer isso em todos os terminais

## Iniciar o server e clients do Flare
## Abrir outra janela de terminal do server
   rodar o arquivo .sh submit_job dentro da pasta do cifar10-real-world
   rodar ./submit_job.sh cifar10_fedavg_stream_tb 1.0
   o project.yml ainda precisa ser ajustado pra funcionar com HE
   quando for adicionar mais clientes copiar o job do cifar10 no workspace do project.yml