from PIL import Image
from wolfpack import settings

def set_attributes(obj,data):
    for key, value in data.items():
            setattr(obj, key, value)
    obj.save()
    return obj

def resize_img(uploaded_file,fileurl,size,num,filename):
        img = Image.open('.'+fileurl)
        imgGray = img.resize(size)
        filep='/media/'+str(num)+uploaded_file.id.hex+filename
        imgGray.save('.'+filep)
        return filep

def convert_img(uploaded_file,fileurl,num,filename):
        img = Image.open('.'+fileurl)
        imgGray = img.convert('L')
        filep='/media/'+str(num)+uploaded_file.id.hex+filename
        imgGray.save('.'+filep)
        return filep

def add_urls(dict):
        data={}
        for k,v in dict.items():
                if("image" in k and v):
                        data[k]=settings.DOMAIN_URL+v
                else:
                        data[k]=v
        return data