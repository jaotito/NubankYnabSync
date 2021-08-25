Programa que lança compras feitas no cartão de crédito NuBank automaticamente e rapidamente (cerca de 30 segundos) no software de orçamento YNAB (youneedabudget.com).

--MUITO Crédito para https://github.com/andreroggeri/, dev do https://github.com/andreroggeri/pynubank, que resolveu completamente a autenticação e comunicação com o Nubank. Também espiei o https://github.com/andreroggeri/nubank-sync-ynab, para descobrir como adicionar o certificado digital nas variáveis de ambiente do Heroku--

O programa lança a partir da última compra lançada no YNAB. Se não houver nenhuma compra lançada no YNAB, ele lança até o número de dias "Max_days" passados. Depois da primeira sincronização, a cada transação no cartão, o programa roda e é feito o lançamento no YNAB.

Como utilizar:

Parte A: Subir o Servidor no Heroku com o App

  1: Obter o certificado digital do NuBank utilizando o PyNubank:
  https://github.com/andreroggeri/pynubank/blob/master/examples/login-certificate.md , e  codificar o arquivo em uma string base64 no diretório onde salvou o certificado, rode o seguinte comando em python:

  file = open("cert.p12", "rb", ).read()
  encoded = base64.b64encode(file)
  print(encoded)

  Copie (sem o "b'" do início e o "'" do final)a string do resultado e guarde, será utilizado no passo 4


  2: Acessar aplicativo do Ynab, gerar e guardar um token para acesso à API do Ynab: https://app.youneedabudget.com/settings/developer.

  3: Acessar a API do Ynab e fazer um get dos budgets da sua conta:
  https://api.youneedabudget.com/v1#/Budgets/getBudgets o resultado vai conter o id do seu budget e o id da conta do ynab associada ao cartão de crédito.

  3: Clonar esse repositório, criar um app novo no heroku.com e fazer deploy do código.

  4: No Heroku, configurar as seguintes variáveis de ambiente do app:

    CERT_NU - Uma string do certificado digital gerado pelo PyNubank, codificado em base64 - Obtido no passo 1

    ACCOUNTID_YNAB - ID da conta do cartão nubank no seu budget no YNAB. - Obtido no passo 3

    BUDGETID_YNAB - ID do budget do YNAB onde está a conta do cartão nubank que você quer sincronizar - Obtido no passo 3

    Max_days - O número máximo de dias no passado que o programa irá sincronizar, recomendável até 30.

    SECRET_KEY_FLASK - qualquer valor, para melhorar a segurança, é recomendável algo acima de 10 dígitos.
    
    CPF_NU - O Cpf para login no aplicativo do nubank

    SENHA_NU - A senha do aplicativo do nubank (Não a senha do cartão)

    TOKEN_YNAB - O Token para acesso à API do Ynab - Obtido no passo 2

    USER_TIMEZONE - O nome do seu fuso horário de acordo com o padrão dessa lista: https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568 se você está em São Paulo utilize:

    America/Sao_Paulo

    Esse fuso horário deve ser o mesmo que você considera para lançar a data das suas transações no YNAB.


Parte B: Configurar aplicativo no seu celular, que vai ficar esperando uma notificação de compra do aplicativo do NuBank, e vai disparar o sinal para que o servidor faça a sincronização.

  1 - Ative notificações para compras no Nubank

  2 - Baixe o aplicativo IFTTT e crie uma conta gratuita.

  3 - No IFTT, crie um aplicativo utilizando o serviço "dispositivo android", e selecione como gatilho "receber uma notificação de um app específico", coloque o Nubank. Como ação seguinte, selecione o serviço "Webhook" e adicione a URL do seu app + o sufixo "webhook" (Ex: https://nomequevocedeuparaoseuapp.herokuapp.com/webhook), e selecione o método "GET".

PRONTO! Está funcionando! Se quiser usar mas estiver com problemas mande uma mensagem que eu posso ajudar!



-- Outras fontes que consultei/estudei para montar o programa estão no arquivo fontesconsultadas.
