import functions as fc
import keras
from tensorflow import keras
from tensorflow.keras import Model
from tensorflow.keras.models import load_model
from keras.utils import np_utils
import numpy as np
import os 
import getpass


def learning(paths, classnames, modelname):

	if not(os.path.exists('C:\\Users\\'+ getpass.getuser() + '\\Documents\\Docthrush')):
		os.mkdir('C:\\Users\\'+ getpass.getuser() + '\\Documents\\Docthrush')

	
	with open('C:\\Users\\'+ getpass.getuser() + '\\Documents\\Docthrush\\' + modelname + '.txt', 'w+') as f:
		for i in (classnames):
			f.write(i + '\n')
		f.write('\n')
		f.write('\n')
		f.write('\n')

	data=[]
	for i in range(len(paths)):
		fc.pdf_to_png(paths[i])
		fc.resizeZ(paths[i])
		data+=fc.png_to_list(paths[i])
		for file in os.listdir(paths[i]):
			if file.endswith(".png"):
				os.remove(file)




	#общее кол-во файлов
	val=0
	for i in range(len(paths)):
		val+=sum([len(files) for r, d, files in os.walk(paths[i])])

	#таргеты
	tar=[]
	for i in range(len(paths)):
		for j in range(sum([len(files) for r, d, files in os.walk(paths[i])])):
			tar.append(i)

	#print('targets\n', tar)

	#tar.reverse()
	tar_array=np_utils.to_categorical(tar)
	
	dataN=np.array(data)
	dataN = np.array(dataN).reshape(val, 810*570*3)
	dataN = dataN / 255.0

	model = Model()
	model = fc.learning(dataN, tar_array, classnames)
	
	
	
	

	path_model = 'C:\\Users\\'+ getpass.getuser() + '\\Documents\\Docthrush\\' + modelname + '.h5'
	model.save(path_model)



