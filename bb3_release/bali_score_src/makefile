install: bali_score 

clean:
	rm *.o

HEADERS = general.h clustalw.h

CC	= cc
CFLAGS  = -c -O -I$(EXPAT_INC)
LFLAGS	= -O -lm -L$(EXPAT_LIB) -lexpat
EXPAT_LIB	= C:\Users\Sanke\Downloads\BioInformatics Project\bb3_release\bali_score_src\expat-1.95.2\lib
EXPAT_INC	= C:\Users\Sanke\Downloads\BioInformatics Project\bb3_release\bali_score_src\expat-1.95.2\include


bali_score : readxml.o init.o util.o bali_score.o
	$(CC) -o $@ readxml.o init.o util.o bali_score.o $(LFLAGS)


.c.o :	$(HEADERS)
	$(CC) $(CFLAGS) $?

