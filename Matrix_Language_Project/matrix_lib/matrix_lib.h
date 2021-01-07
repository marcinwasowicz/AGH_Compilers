#ifndef HEADER_FILE
#define HEADER_FILE

typedef struct{
    double* data;
    int* dim;
    int dim_size;
    bool garbage_collectable;
}matrix;

matrix* init_matrix_list(double* data, int* dim, int dim_size, bool garbage_collectable);

matrix* add_elem_by_elem(matrix* a, matrix* b, bool garbage_collectable);

matrix* sub_elem_by_elem(matrix* a, matrix* b, bool garbage_collectable);

matrix* mult_elem_by_elem(matrix* a, matrix* b, bool garbage_collectable);

matrix* div_elem_by_elem(matrix* a, matrix* b, bool garbage_collectable);

double get_element(matrix* mat, int* dim, int dim_size);

void set_element(matrix* mat, int* dim, int dim_size, double value);

matrix* mult(matrix* a, matrix* b, bool garbage_collectable);

matrix* transpose(matrix* a, bool garbage_collectable);

matrix* zeros(int size, bool garbage_collectable);

matrix* ones(int size, bool garbage_collectable);

matrix* eye(int size, bool garbage_collectable);

void add_elem_by_elem_store(matrix* a, matrix* b);

void sub_elem_by_elem_store(matrix* a, matrix* b);

void mult_elem_by_elem_store(matrix* a, matrix* b);

void div_elem_by_elem_store(matrix* a, matrix* b);

void free_matrix(matrix* mat);

void add_to_element(matrix* mat, int* dim, int dim_size, double value);

void sub_from_element(matrix* mat, int* dim, int dim_size, double value);

void mult_element_by(matrix* mat, int* dim, int dim_size, double value);

void div_element_by(matrix* mat, int* dim, int dim_size, double value);

void printf_matrix_internal(matrix* mat, int dim_itr, int idx);

void printf_matrix(matrix* mat);

#endif
