from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys
import tratamentoPlus
from tratamentoPlus import dividir_texto_em_partes, traduzir_parte

def obter_traducao(texto, nome_base):
    url_site = "https://dharmamitra.org/?input_encoding=dev&view=search&target_lang=english&model=default"
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ativa o modo headless
    chrome_options.add_argument("--disable-gpu")  # Evita problemas de renderização
    chrome_options.add_argument("--window-size=1920,1080")  # Define tamanho da janela
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url_site)

    # Verifica se o botão inicial está disponível e clica
    while True:
        try:
            botao_inicial = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".MuiButton-containedPrimary"))
            )
            botao_inicial.click()
            break
        except:
            print("Refresh da página, pois botão inicial não foi encontrado.")
            driver.refresh()

    # Divide o texto em duas partes
    partes = dividir_texto_em_partes(texto)
    texto_traduzido_total = ""
    indice = 1
    for parte in partes:
        texto_traduzido_total += traduzir_parte(driver, parte, indice)
        indice += 1

    # Traduzir a primeira parte
    # print("Traduzindo parte 1 de 2...")
    # texto_traduzido_total += traduzir_parte(driver, parte1, 1)
    # time.sleep(5)
    #
    # # Traduzir a segunda parte
    # print("Traduzindo parte 2 de 2...")
    # texto_traduzido_total += traduzir_parte(driver, parte2, 2)

    # Salvar o texto traduzido em um arquivo
    nome_arquivo = f"traducao_de_{nome_base}.txt"
    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(texto_traduzido_total)

    print(f"Texto traduzido salvo em '{nome_arquivo}'")
    driver.quit()






# Texto para teste
texto = """भारत एक अत्यधिक विविधतापूर्ण और समृद्ध सांस्कृतिक धरोहर वाला देश है। यह एशिया महाद्वीप में स्थित है और इसकी सीमा नेपाल, भूटान, बांगलादेश, पाकिस्तान, म्यांमार, श्रीलंका, मालदीव और चीन जैसे देशों से जुड़ी हुई है। भारत में लगभग 1.4 बिलियन लोग निवास करते हैं, और यहाँ की भाषा, धर्म, जाति और सांस्कृतिक विविधता उसे पूरी दुनिया में एक अद्वितीय स्थान देती है।

भारत का इतिहास प्राचीन और गौरवपूर्ण रहा है। यहाँ के धार्मिक स्थल, महल, किले और पुरातात्विक स्थल भारतीय सभ्यता के उत्थान की कहानी सुनाते हैं। वेद, उपनिषद, महाभारत, रामायण और भगवद गीता जैसे धार्मिक और दार्शनिक ग्रंथ भारतीय संस्कृति का अभिन्न हिस्सा हैं। भारत के विभिन्न हिस्सों में विभिन्न भाषाएँ बोली जाती हैं, जिनमें हिंदी, बांग्ला, मराठी, गुजराती, तमिल, तेलुगु, मलयालम, पंजाबी, उर्दू, कन्नड़, संस्कृत और कई अन्य क्षेत्रीय भाषाएँ शामिल हैं। हिंदी भारत की राजभाषा है, और अंग्रेजी भी व्यापक रूप से उपयोग की जाती है।

भारत में विभिन्न धर्मों का पालन किया जाता है। हिन्दू धर्म यहाँ का सबसे बड़ा धर्म है, लेकिन यहाँ मुस्लिम, सिख, ईसाई, जैन, बौद्ध, पारसी और यहूदी धर्मों के अनुयायी भी रहते हैं। यहाँ के त्योहारों का भी वैश्विक स्तर पर एक विशेष महत्व है, जैसे दिवाली, होली, ईद, दशहरा, दुर्गा पूजा, क्रिसमस, गुरु नानक जयंती और अन्य धार्मिक एवं सांस्कृतिक आयोजन।

भारतीय संस्कृति में कला, संगीत, साहित्य, नृत्य, रंगमंच और फिल्में महत्वपूर्ण स्थान रखते हैं। भारतीय फिल्म उद्योग, जिसे बॉलीवुड के नाम से जाना जाता है, दुनिया का सबसे बड़ा फिल्म उद्योग है। भारतीय कला और शिल्प को भी विश्वभर में सराहा जाता है। यहाँ के पारंपरिक नृत्य जैसे भरतनाट्यम, कथक, ओडिसी, kathakali और कुचिपुड़ी का विशेष महत्व है। भारत के मंदिरों में प्राचीन शिल्पकला के अद्भुत उदाहरण मिलते हैं, जैसे कि ताज महल, कांची मंदिर, काशी विश्वनाथ मंदिर, गोलकोंडा किला और कई अन्य धरोहर स्थल।

भारत का आर्थिक विकास तेजी से हो रहा है। यहाँ की उभरती हुई टेक्नोलॉजी, शिक्षा और स्वास्थ्य सेवा प्रणाली ने वैश्विक स्तर पर भारत को एक नया पहचान दिलाई है। भारतीय कंपनियाँ जैसे टाटा, इंफोसिस, विप्रो, रिलायंस, और अन्य उद्योग समूह दुनिया भर में प्रभावी रूप से कार्यरत हैं। भारत का सूचना प्रौद्योगिकी क्षेत्र भी वैश्विक मानकों के अनुरूप प्रगति कर रहा है। भारतीय स्टार्टअप्स और उद्यमिता का नया दौर यहाँ के युवाओं द्वारा संचालित हो रहा है। इसके अलावा, भारत में दुनिया का सबसे बड़ा इंटरनेट उपयोगकर्ता समुदाय भी है, जो डिजिटल इंडिया की ओर एक प्रमुख कदम है।

समाज में सुधार और सामाजिक न्याय के लिए सरकार द्वारा कई योजनाएँ बनाई जा रही हैं। स्वच्छ भारत मिशन, मेक इन इंडिया, डिजिटल इंडिया और प्रधानमंत्री जन धन योजना जैसी पहलों ने भारतीय समाज के हर वर्ग को लाभ पहुँचाया है। भारत में महिलाओं के अधिकारों और समानता के लिए भी कई सुधार किए जा रहे हैं, ताकि वे समाज में बराबरी की स्थिति में आ सकें।

भारत का भविष्य उज्जवल है, और यह लगातार अपने सामर्थ्य और क्षमता को साबित कर रहा है। देश के लोग एकजुट हैं और एक साथ मिलकर न केवल अपनी समस्याओं का समाधान ढूंढ रहे हैं, बल्कि भारतीयता की असली पहचान को बनाए रखते हुए विकास के नए कीर्तिमान स्थापित कर रहे हैं।
"""
nome_base = "darma"

# Executa a função principal
obter_traducao(texto, nome_base)
