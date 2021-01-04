#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include "matrix_lib.h"


matrix* init_matrix_list(double* data, int* dim, int dim_size, bool garbage_collectable){
    matrix* mat = (matrix*) malloc(sizeof(matrix));
    mat->garbage_collectable = garbage_collectable;
    mat->dim_size = dim_size;

    mat->dim = (int*) malloc(sizeof(dim)*dim_size);
    for(int i = 0; i<dim_size; i++){
        mat->dim[i] = dim[i];
    }

    int data_size = 1;
    for(int i = 0; i<dim_size; i++){
        data_size *= dim[i];
    }

    mat->data = (double*) malloc(sizeof(double) * data_size);
    for(int i = 0; i<data_size; i++){
        mat->data[i] = data[i];
    }

    return mat;
}

matrix* add_elem_by_elem(matrix* a, matrix* b, bool garbage_collectable){
    matrix* mat = (matrix*) malloc(sizeof(matrix));
    mat->garbage_collectable = garbage_collectable;
    mat->dim_size = a->dim_size;

    mat->dim = (int*) malloc(sizeof(a->dim)*a->dim_size);
    for(int i = 0; i<a->dim_size; i++){
        mat->dim[i] = a->dim[i];
    }

    int data_size = 1;
    for(int i = 0; i<a->dim_size; i++){
        data_size *= a->dim[i];
    }

    mat->data = (double*) malloc(sizeof(double) * data_size);
    for(int i = 0; i<data_size; i++){
        mat->data[i] = a->data[i] + b->data[i];
    }

    if(!a->garbage_collectable){
        free_matrix(a);
    }

    if(!b->garbage_collectable){
        free_matrix(b);
    }

    return mat;
}

matrix* sub_elem_by_elem(matrix* a, matrix* b, bool garbage_collectable){
    matrix* mat = (matrix*) malloc(sizeof(matrix));
    mat->garbage_collectable = garbage_collectable;
    mat->dim_size = a->dim_size;

    mat->dim = (int*) malloc(sizeof(a->dim)*a->dim_size);
    for(int i = 0; i<a->dim_size; i++){
        mat->dim[i] = a->dim[i];
    }

    int data_size = 1;
    for(int i = 0; i<a->dim_size; i++){
        data_size *= a->dim[i];
    }

    mat->data = (double*) malloc(sizeof(double) * data_size);
    for(int i = 0; i<data_size; i++){
        mat->data[i] = a->data[i] - b->data[i];
    }

    if(!a->garbage_collectable){
        free_matrix(a);
    }

    if(!b->garbage_collectable){
        free_matrix(b);
    }

    return mat;
}

matrix* mult_elem_by_elem(matrix* a, matrix* b, bool garbage_collectable){
    matrix* mat = (matrix*) malloc(sizeof(matrix));
    mat->garbage_collectable = garbage_collectable;
    mat->dim_size = a->dim_size;

    mat->dim = (int*) malloc(sizeof(a->dim)*a->dim_size);
    for(int i = 0; i<a->dim_size; i++){
        mat->dim[i] = a->dim[i];
    }

    int data_size = 1;
    for(int i = 0; i<a->dim_size; i++){
        data_size *= a->dim[i];
    }

    mat->data = (double*) malloc(sizeof(double) * data_size);
    for(int i = 0; i<data_size; i++){
        mat->data[i] = a->data[i] * b->data[i];
    }

    if(!a->garbage_collectable){
        free_matrix(a);
    }

    if(!b->garbage_collectable){
        free_matrix(b);
    }

    return mat;
}

matrix* div_elem_by_elem(matrix* a, matrix* b, bool garbage_collectable){
    matrix* mat = (matrix*) malloc(sizeof(matrix));
    mat->garbage_collectable = garbage_collectable;
    mat->dim_size = a->dim_size;

    mat->dim = (int*) malloc(sizeof(a->dim)*a->dim_size);
    for(int i = 0; i<a->dim_size; i++){
        mat->dim[i] = a->dim[i];
    }

    int data_size = 1;
    for(int i = 0; i<a->dim_size; i++){
        data_size *= a->dim[i];
    }

    mat->data = (double*) malloc(sizeof(double) * data_size);
    for(int i = 0; i<data_size; i++){
        mat->data[i] = a->data[i] / b->data[i];
    }

    if(!a->garbage_collectable){
        free_matrix(a);
    }

    if(!b->garbage_collectable){
        free_matrix(b);
    }

    return mat;
}

matrix* mult(matrix* a, matrix* b, bool garbage_collectable){}

matrix* transpose(matrix* a, bool garbage_collectable){}

matrix* zeros(int size, bool garbage_collectable){}

matrix* ones(int size, bool garbage_collectable){}

matrix* eye(int size, bool garbage_collectable){}

double get_emlement(matrix* mat, int* dim, int dim_size){
    int index = dim[dim_size - 1];
    for(int i = dim_size - 2; i>= 0; i--){
        index += dim[i]*mat->dim[i];
    }
    return mat->data[index];
}

void set_element(matrix* mat, int* dim, int dim_size, double value){
    int index = dim[dim_size - 1];
    for(int i = dim_size - 2; i>= 0; i--){
        index += dim[i]*mat->dim[i];
    }
    mat->data[index] = value;
}

void add_elem_by_elem_store(matrix* a, matrix* b){
    int data_size = 1;
    for(int i = 0; i<a->dim_size; i++){
        data_size *= a->dim[i];
    }

    for(int i = 0; i<data_size; i++){
        a->data[i] += b->data[i];
    }

    if(!b->garbage_collectable){
        free_matrix(b);
    }
}

void sub_elem_by_elem_store(matrix* a, matrix* b){
    int data_size = 1;
    for(int i = 0; i<a->dim_size; i++){
        data_size *= a->dim[i];
    }

    for(int i = 0; i<data_size; i++){
        a->data[i] += b->data[i];
    }

    if(!b->garbage_collectable){
        free_matrix(b);
    }
}

void mult_elem_by_elem_store(matrix* a, matrix* b){
    int data_size = 1;
    for(int i = 0; i<a->dim_size; i++){
        data_size *= a->dim[i];
    }

    for(int i = 0; i<data_size; i++){
        a->data[i] += b->data[i];
    }

    if(!b->garbage_collectable){
        free_matrix(b);
    }
}

void div_elem_by_elem_store(matrix* a, matrix* b){
    int data_size = 1;
    for(int i = 0; i<a->dim_size; i++){
        data_size *= a->dim[i];
    }

    for(int i = 0; i<data_size; i++){
        a->data[i] += b->data[i];
    }

    if(!b->garbage_collectable){
        free_matrix(b);
    }
}

void free_matrix(matrix* mat){
    free(mat->data);
    free(mat->dim);
    free(mat);
}

void add_to_element(matrix* mat, int* dim, int dim_size, double value){
    int index = dim[dim_size - 1];
    for(int i = dim_size - 2; i>= 0; i--){
        index += dim[i]*mat->dim[i];
    }
    mat->data[index] += value;
}

void sub_from_element(matrix* mat, int* dim, int dim_size, double value){
    int index = dim[dim_size - 1];
    for(int i = dim_size - 2; i>= 0; i--){
        index += dim[i]*mat->dim[i];
    }
    mat->data[index] -= value;
}

void mult_element_by(matrix* mat, int* dim, int dim_size, double value){
    int index = dim[dim_size - 1];
    for(int i = dim_size - 2; i>= 0; i--){
        index += dim[i]*mat->dim[i];
    }
    mat->data[index] *= value;
}

void div_element_by(matrix* mat, int* dim, int dim_size, double value){
    int index = dim[dim_size - 1];
    for(int i = dim_size - 2; i>= 0; i--){
        index += dim[i]*mat->dim[i];
    }
    mat->data[index] /= value;
}



