from cimpy.cimgen_v2_4_15_flat_9.Base import Base


class WindLVRTQcontrolModesKind(Base):
	'''
	LVRT Q control modes .

		'''

	possibleProfileList = {'class': ['DY', ],
												}

	

	def __init__(self,  ):
	
		pass
	
	def __str__(self):
		str = 'class=WindLVRTQcontrolModesKind\n'
		attributes = self.__dict__
		for key in attributes.keys():
			str = str + key + '={}\n'.format(attributes[key])
		return str
