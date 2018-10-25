TARGETS=emails

all: $(TARGETS)

chairs.json: chairs.txt
	./make-chairs.py

emails: *.ics chairs.json make-emails.py
	./make-emails.py

clean:
	rm -f *.eml chairs.json
