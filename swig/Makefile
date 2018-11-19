default:all

all:
	swig -c++ -python example.i
	python setup.py build_ext --inplace

.PHONY:clean

clean:
	rm -rf *.o 
	rm build -rf 
	rm *.pyc *.cxx *.so -rf

