install:
	python.exe -m pip install --upgrade pip &&\
	python -m spacy download en_core_web_lg &&\
		pip install -r requirements.txt
