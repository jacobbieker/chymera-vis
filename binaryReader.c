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

	double **gridData = malloc(5 * sizeof(double *));

	for (int i = 0; i < 5; ++i) {
		int sizeToRead = 0;
		fread(&sizeToRead, sizeof(int), 1, f);
		sizeToRead /= sizeof(double);
		fprintf(stderr, "sizeToRead: %d\n", sizeToRead);
		double *buffer = malloc(sizeof(double)*sizeToRead);
		gridData[i] = malloc(sizeof(double) * sizeToRead);
		fread(buffer, sizeof(double), sizeToRead, f);
		for (int j = 0; j < sizeToRead; ++j) {
			gridData[i][j] = buffer[j];
		}
		fread(&sizeToRead, sizeof(int), 1, f);
	}
	int currentPosition = ftell(f);

	int sizeToRead;
	fread(&sizeToRead, sizeof(float), 1, f);
	fprintf(stderr, "sizeToRead: %d\n", sizeToRead);
	
	sizeToRead /= sizeof(float);
	fprintf(stderr, "Shortened sizeToRead: %d\n", sizeToRead);

	double zof3n, rof3n, delt, time, elost, den, sound, ommax;
	int    jreq;

	fread(&zof3n, sizeof(double),1, f);
	fread(&rof3n, sizeof(double),1, f);
	fread(&delt, sizeof(double),1, f);
	fread(&time, sizeof(double),1, f);
	fread(&elost, sizeof(double),1, f);
	fread(&den, sizeof(double),1, f);
	fread(&sound, sizeof(double),1, f);
	fread(&jreq, sizeof(int),1, f);
	fread(&ommax, sizeof(double),1, f);

	fprintf(stderr, "zof3n: %f rof3n: %f delt: %f time: %f elost: %f den: %f sound: %f jreq: %d ommax: %f\n", zof3n, rof3n, delt, time, elost, den, sound, jreq, ommax);

	fclose(output);
	fclose(f);
	return 0;
}
