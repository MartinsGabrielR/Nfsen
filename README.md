Monitoramento com Netflow
Este repositório reúne uma coleção de **scripts em Python** para automatizar tarefas relacionadas ao **NetFlow**, **Nfdump** e **NfSen**.  
O objetivo é facilitar o monitoramento, a geração de relatórios e a manutenção da infraestrutura de rede.

# Scripts Disponíveis

1. `nfsen_telegram.py`
*Relatórios para o Telegram*  
- Gera relatórios a partir dos arquivos `nfcapd` mais recentes.  
- Converte o relatório em **imagem legível** e envia para um grupo/canal no Telegram.  
- Executa em segundo plano com verificação periódica (a cada 10 minutos).  
- Utiliza variáveis de ambiente para maior segurança.

2. `backupnfsen.py`
*Backup dos dados*  
- Percorre os diretórios do NfSen.  
- Compacta os arquivos de dias anteriores em `.tar.gz`.  
- Move para o diretório de backup definido em `backup_dir`.  
- Remove os arquivos originais após o backup para liberar espaço.  
- Executa automaticamente uma vez por dia.

3. `auto_nfsen.py`
*Forçar start*  
- Reinicia o serviço do NfSen em intervalos configuráveis (padrão: 1 hora).  
- Mantém o sistema ativo e evita travamentos.  
- Ideal para ambientes de produção em que o NfSen precisa estar sempre disponível.
