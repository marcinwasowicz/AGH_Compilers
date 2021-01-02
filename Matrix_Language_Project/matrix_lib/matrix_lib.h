#ifndef HEADER_FILE
#define HEADER_FILE

typedef struct{
    double* data;
    int* dim;
    int dim_size;
}matrix;

matrix* alloc_matrix();

matrix* init_matrix_list(double* data, int* dim, int dim_size);

matrix* add_elem_by_elem(matrix* a, matrix* b);

matrix* sub_elem_by_elem(matrix* a, matrix* b);

matrix* mult_elem_by_elem(matrix* a, matrix* b);

matrix* div_elem_by_elem(matrix* a, matrix* b);

matrix* mult(matrix* a, matrix* b);

matrix* transpose(matrix* a);

matrix* zeros(int size);

matrix* ones(int size);

matrix* eye(int size);

double get_emlement(matrix* mat, int* dim, int dim_size);

void set_element(matrix* mat, int* dim, int dim_size, double value);

void add_elem_by_elem_store(matrix* a, matrix* b);

void sub_elem_by_elem_store(matrix* a, matrix* b);

void mult_elem_by_elem_store(matrix* a, matrix* b);

void div_elem_by_elem_store(matrix* a, matrix* b);

void store(matrix* a, matrix* b);

void free_matrix(matrix* mat);

void add_to_element(matrix* mat, int* dim, int dim_size, double value);

void sub_from_element(matrix* mat, int* dim, int dim_size, double value);

void mult_element_by(matrix* mat, int* dim, int dim_size, double value);

void div_element_by(matrix* mat, int* dim, int dim_size, double value);

#endif
