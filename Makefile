NAME = computorv2

all:
	@echo "Python project: nothing to compile. Run with 'python3 main.py'"

run:
	python3 main.py

test:
	python3 defense_tester.py

clean:
	rm -rf __pycache__
	rm -rf src/__pycache__
	rm -rf src/*/__pycache__

fclean: clean

re: fclean all
