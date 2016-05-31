#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main (int argc, char *argv[]) {
	if (argc != 3) {
		printf("Usage: %s <file1> <file2>\n", argv[0]);
		exit(EXIT_FAILURE);
	}

	FILE *f = fopen(argv[1],"r");
	if (!f) {
		printf("Unable to open file!\n");
		return 1;
	}
	FILE *output = fopen(argv[2], "w");

	fseek(f, 0, SEEK_END);
	long int sizeOfFile = ftell(f);
	fseek(f, 0, SEEK_SET);
	fprintf(stderr, "Outside of for loop: Current position is: %ld\n", ftell(f));

	double **gridData = malloc(5 * sizeof(double *));

	fprintf(stderr, "Size of double: %lu\n", sizeof(double));

	for (int i = 0; i < 5; ++i) {
		int sizeToRead = 0;
		fread(&sizeToRead, sizeof(int), 1, f);
		sizeToRead /= sizeof(double);
		//fseek();
		fprintf(stderr, "sizeToRead: %d\n", sizeToRead);
		double *buffer = malloc(sizeof(double)*sizeToRead);
		gridData[i] = malloc(sizeof(double) * sizeToRead);
		fread(buffer, sizeof(double), sizeToRead, f);
		fprintf(stderr, "Current position is: %ld\n", ftell(f));
		for (int j = 0; j < sizeToRead; ++j) {
			gridData[i][j] = buffer[j];
		}
		fread(&sizeToRead, sizeof(int), 1, f);
		fprintf(stderr, "second sizeToRead: %d\n", sizeToRead);
	}
	int currentPosition = ftell(f);
	fprintf(stderr, "sizeOfFile: %ld currentPosition: %d", sizeOfFile, currentPosition);

	int sizeToRead;
	fread(&sizeToRead, sizeof(int), 1, f);
	fprintf(stderr, "sizeToRead: %d\n", sizeToRead);
	int *metaData = malloc(sizeof(int)*sizeToRead);
	fread(metaData, sizeof(int), sizeToRead, f);

	for (int i = 0; i < sizeToRead; ++i) {
		if (metaData[i] != 0.0) {
			fprintf(stderr, "metaData: %d\n",metaData[i]);
		}
	}

	//fprintf(output, "%d\n", sizeToRead);
	// Free memory here

	fclose(output);
	fclose(f);
	return 0;
}
