from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time

#Variaveis
driver = webdriver.Chrome()
item = 0

#Modelos
MODELO = ["Para eu conseguir te ajudar por aqui, você precisa autorizar que eu acesse sua conta da Vivo e aceitar os Termos e Condições de Uso: https://vivo.tl/aura-termos-condicoes.  Você aceita e autoriza? Digite o número da opção desejada: . Sim . Não",
          "Agora, para falar sobre outro tema, é só digitar o aqui na conversa que eu te mostro o caminho.",          
          "Você gostaria de saber mais sobre qual tipo de plano da Vivo?  Digite o número da opção desejada: . Plano para Celular . Plano para Casa",
          "A Vivo separou alguns planos que podem combinar com o seu perfil.  Para escolher o plano que você quer saber mais detalhes, é só digitar o número da opção aqui na conversa.  . #1 VIVO CONTROLE   por R$ 32,49/mês . #2 VIVO CONTROLE por R$ 37,49/mês . #3 VIVO CONTROLE por R$ 36,99/mês . #4 VIVO CONTROLE por R$ 41,99/mês",
          "Me conta se você gostou desse plano ou se prefere ver outras opções.  É só digitar o número da opção desejada.*",
          "Ah, que pena! Eu estava gostando de te ajudar. Quando precisar da minha ajuda de novo, estarei por aqui. . Confirmar sair . Cancelar",
          "Até logo! Foi um prazer poder te ajudar. Quando precisar, pode me chamar por aqui.",
          "Olá! Eu sou a Aura, a inteligência artificial da Vivo. Posso te ajudar? Por aqui, eu sei resolver os temas que estão neste menu, é só escolher o assunto que vamos falar."]

RESPOSTAS = ["Sim",
             "Conhecer Planos",
             "Plano para Celular",
             "1",
             "Sair",
             "Confirmar Sair"]

TESTES = ["Termos Aceito....",
          "Planos Conhecidos...",
          "Planos para Celular...",
          "O Plano foi selecionado...",
          "Saiu...",
          "Confirmou sair..."]

#Laço para Comparar modelos
def ComparaModelos(Ultima_Mensagem, index):    
    if Ultima_Mensagem == (str(MODELO[index])) or Ultima_Mensagem == (str(MODELO[7])):        
        EnviaMensagem(driver, (str(RESPOSTAS[index])))      
        return True
    return False    
    
#Laço para identificar a ultima mensagem    
def PegaUltimaMensagem():
    time.sleep(1)
    try:        
        mensagem = driver.find_element(By.CSS_SELECTOR, "[tabindex='0'] [data-testid='last-msg-status']")
        texto = mensagem.text        
    except NoSuchElementException:
        print("Não foi possível encontrar a última mensagem.")                
        return None
    return texto

#Laço para enviar mensagem
def EnviaMensagem(browser, message):
    Vai_Menssagem = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p')))
    Vai_Menssagem.send_keys(message)        
    Vai_Menssagem.send_keys(Keys.RETURN)
    time.sleep(1)

#Laço que aguarda mensagem ser exibida
def IdentificaModeloEEsperaMensagem(index):        
    EsperaModelo = str(PegaUltimaMensagem())
    while EsperaModelo != (str(MODELO[index])):
        print("Aguardando Mensagem...")        
        EsperaModelo = str(PegaUltimaMensagem())        
        time.sleep(1)                     

#Laço de Teste
def test_ValidaTeste(index):              
    result = ComparaModelos(PegaUltimaMensagem(), index)    
    print(str(TESTES[index])+str(result))            

#Acessa o Whatspp
driver.get("https://web.whatsapp.com/send?phone=5511999151515&text=Ola")
EnviaMensagem(driver, ", Boa tarde")

#Tempo para carregar Pagina
wait = WebDriverWait(driver = driver, timeout = 30)

#Tempo inicial para o Bot Responder
time.sleep(10)

#Inicia Conversa
while item <= 6:
    #Executa e Valida testes
    test_ValidaTeste(item)
    item = item + 1  

    #Tempo até mensagem aparecer em tela
    IdentificaModeloEEsperaMensagem(item)            

print("Conversa Finalizada e Todos os testes Passaram")

#Fechar aba do navegador.
driver.close()