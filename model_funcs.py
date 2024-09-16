#пространство для творчества Полины Д


from transformers import Blip2Processor, Blip2ForConditionalGeneration
import torch
from PIL import Image

processor = Blip2Processor.from_pretrained("processor_files")
model = Blip2ForConditionalGeneration.from_pretrained("eng_model_files")



def convert_image(image):
    '''
    тут возможно я сама добавлю обрезку фото и конвертацию к .png если можно, 
    если нет, то буду заставлять пользователя присылать только png снаружи
    '''
    #пока хз нужны ли нам какие-то преобразования
    #мб в будущем для ускорения 
    return image

def get_model_output(image_path):
    '''
    принимает путь к файлу с картинкой, формат (jpg или png неважен)
    возвращает строку с текстовым описанием
    '''
    raw_image = Image.open(image_path).convert('RGB')
    prompt = "Question: What clothes are in the picture? Answer: In the picture there is a person wearing"

    inputs = processor(raw_image, text=prompt, return_tensors="pt")

    generated_ids = model.generate(**inputs, max_new_tokens=5)
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
    return generated_text

def get_text_res(image):
    '''
        image прям из телеги
    '''
    image = convert_image(image)
    return get_model_output(image)
