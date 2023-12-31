import json
import os

import openai
import dotenv

dotenv.load_dotenv()
openai.api_key = os.getenv('OPEN_AI_TOKEN')


def get_keywords_values(message):
    messages = [
        {'role': 'system', 'content': 'Write answer using English'},
        {"role": "user",
         "content": message}]
    functions = [
        {
            "name": "get_current_weather",
            "description": "Get flat request using english languge",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "enum": ['Gürsu', 'an', 'Kagıcak', 'Tatlısu', 'Kyrenia', 'Lara', 'Adabükü', 'Yıldız', 'Eyüp', 'Çatalköy', 'Fethiye', 'Karaoğlanoğlu', 'Mahmutlar', 'Beycik', 'Beyoğlu', 'Bagcılar', 'Gocek', 'Konakli', 'Gazipaşa', 'Yeni', 'LimanKonyaaltı', 'Kuşadası', 'Gündoğan', 'Altıntaş', 'Eyüpsultan', 'Kızıltoprak', 'Muratpaşa', 'Hurma', 'Gürsü', 'Kuşkavağı', 'Bodrum', 'Sarisu', 'Muratpasa', 'Konaklı', 'Edremit', 'Molla', 'Göynük', 'Olüdeniz', 'Kadıköy', 'Şişli', 'Iskele', 'Narlıdere', 'Boğaz', 'Long', 'Kargıcak', 'Çiğli', 'Gaziosmanpaşa', 'Çeşme', 'Bornova', 'Çamyuva', 'Alsancak', 'Izmir', 'Kemer', 'Soğuksu', 'Bahçeşehir', 'Kadıkoy', 'Guzeloba', 'Finike', 'Istanbul', 'Tarsus', 'Kumluca', 'Konyaalti', 'Bellapais', 'Ermenek', 'Liman', 'İskele', 'Arapsuyu', 'Varlık', 'Incekum', 'Aslanbucak', 'Acıbadem', 'Mezitli', 'Didim', 'Kağıthane', 'Camyuva', 'Büyükçekmece', 'Kalkan', 'Erdemli', 'Kızılarık', 'Avcılar', 'Ovacık', 'Göksu', 'İzmir', 'Konyaaltı', 'Beylikdüzü', 'a', 'Tömük', 'Beşiktaş', 'Güzeloba', 'Gazıpaşa', 'Oba', 'Demirtaş', 'Esenyurt', 'Üsküdar', 'Göcek', 'Antalya', 'from', 'Alanya', 'Kuzdere', 'Kestel', 'Lapta', 'Başakşehir', 'Hisarönü', 'Güzelobа', 'Tuzla', 'Altınkum', 'Buyukcekmece', 'Bahçeli', 'Doşemealtı', 'Küçükçekmece', 'Beylıkdüzü', 'Gebizli', 'Konak', 'Kartal', 'Ozanköy', 'Pendik', 'Ataşehir', 'Bayraklı', 'Belek', 'Güzelyurt', 'Kargicak', 'Аланья', 'Kadriye', 'Bahçelievler', 'Avsallar', 'Tece', 'the', 'Arslanbucak', 'Maltepe', 'Çeşmeli', 'Altintaş', 'Esentepe', 'Uluç', 'Yenigün', 'Akbük', 'Famagusta', 'Bağcılar', 'Döşemealtı', 'Kadikoy', 'Karşıyaka', 'Antalya:', 'Kepez', 'Yalıkavak', 'Gönyük', 'Bafra', 'HurmaKonyaaltı', 'Kundu', 'Sarısu', 'Uncalı', 'Sariyer', 'Ümraniye', 'Yenisehir', 'Gazipasa', 'Sisli', 'Dosemеalti']
                    },
                    'bedrooms': {
                        "type": "integer",
                        "description": "How many bedrooms are required, e.g. 3",
                    },
                    'price': {
                        "type": "integer",
                        "description": "What is the budget for buying an apartment in USD dollars, e.g. 150000$",
                    },
                    'type': {
                        "type": "integer",
                        "description": "Need aparatment (1) or villa (0), e.g. 1",
                    },
                    'meters': {
                        "type": "integer",
                        "description": "What number of meters are interested in, e.g. 56",
                    }
                },
                "required": ["location", 'bedrooms', 'floors', 'price', 'type', 'meters'],
            },
        }
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto"
    )
    response_message = response["choices"][0]["message"]
    if response_message.get("function_call"):
        function_args = json.loads(response_message["function_call"]["arguments"])
        return {'is_ok': True, 'args': function_args}
    else:
        return {'is_ok': False, 'args': {}}
