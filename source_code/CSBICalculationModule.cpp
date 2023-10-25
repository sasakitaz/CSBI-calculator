#pragma once
#include <Python.h>
#include <string>
#include <iostream>
#include <vector>
#include <omp.h> 
#include "Parameter.h"
#include "tools.h"
#include "MatrixElement300.h"
/*
#include "diagonalization_dsyevd.h"   //LAPACKを用いた対角化
#include "Eigenstate.h" //固有値計算後の成分計算
*/
#include "Eigen/Core"   // x(行, 列)
#include "Eigen/Dense"  // 固有値計算ルーチンの入ったインクルードファイル
#define PRINT_MAT(X) cout << #X << ":\n" << X << endl << endl   //行列の出力
using namespace std;


static PyObject* HamiltonianMatrixGeneration(PyObject* self, PyObject* args){
    int PotParameter_list_size;
    PyObject* Symmetry;
    PyObject* MatrixSize_list;
    PyObject* MolParameter_list;
    PyObject* PotParameter_list, *PotParameter;
    vector<double> PotParam;
    double param;
    // Decide variable type (list)
    if (!PyArg_ParseTuple(args, "OOOO", &Symmetry, &MatrixSize_list, &MolParameter_list, &PotParameter_list)){
        return NULL;
    }
    PotParameter_list_size = PyList_Size(PotParameter_list);
    //Symmetry
    const char *sym = PyUnicode_AsUTF8(Symmetry);
    //Matrix Size
    int n0   = PyLong_AsLong(PyList_GetItem(MatrixSize_list, 0));
    int npls = PyLong_AsLong(PyList_GetItem(MatrixSize_list, 1));
    int nmns = PyLong_AsLong(PyList_GetItem(MatrixSize_list, 1));
    int j    = PyLong_AsLong(PyList_GetItem(MatrixSize_list, 2));
    int m    = PyLong_AsLong(PyList_GetItem(MatrixSize_list, 3));
    //Molecular Parameter
    //rotational constants of small molecule
    double A = PyFloat_AsDouble(PyList_GetItem(MolParameter_list, 0));
    double B = PyFloat_AsDouble(PyList_GetItem(MolParameter_list, 1));
    double C = PyFloat_AsDouble(PyList_GetItem(MolParameter_list, 2));
    //rotational constants of large molecule
    double B_large = PyFloat_AsDouble(PyList_GetItem(MolParameter_list, 3));
    double C_large = PyFloat_AsDouble(PyList_GetItem(MolParameter_list, 4));
    double mu = PyFloat_AsDouble(PyList_GetItem(MolParameter_list, 5));
    double Re = PyFloat_AsDouble(PyList_GetItem(MolParameter_list, 6)); //GUIにReを入れる
    //Potential Paramter
    for (int i = 0; i < PotParameter_list_size ; i++){
        PotParameter = PyList_GetItem(PotParameter_list, i);
        param = PyFloat_AsDouble(PotParameter);    // PyObject -> double
        PotParam.push_back(param);
        Py_DECREF(PotParameter);
    }

    MatrixParameter hoge(n0, npls, nmns, j, m, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
    int dimension = hoge.matrix_size();
    cout << "symmetry,\t" << sym << endl;
    cout << "dimension,\t"  << dimension << endl;
    cout <<"n0 = , " <<  n0 << ",\t npls = , " << npls << ",\t nmns = , " << nmns << ",\t j = , " << j << ",\t m = , " << m << ",\t" << endl;
    Eigen::MatrixXd Hamiltonian = Eigen::MatrixXd::Ones(hoge.matrix_size(), hoge.matrix_size());;
    if (strcmp( sym, "K") == 0) {
        cout << "calculate as K sym." << endl; 
        Hamiltonian = H_K(n0, npls, nmns, j, m,    //matrix size
                       B_large, C_large, mu, Re,   //molecular parameter
                       PotParam);
    }
    else if (strcmp( sym, "Dinftyd") == 0) {
        cout << "calculate as Dinftyd sym." << endl; 
        Hamiltonian = H_Dinftyd(n0, npls, nmns, j, m,    //matrix size
                       B, B_large, C_large, mu, Re,   //molecular parameter
                       PotParam);
    }
    else if (strcmp( sym, "Cinftyv") == 0) {
        cout << "calculate as Cinftyv sym." << endl; 
        Hamiltonian = H_Cinftyv(n0, npls, nmns, j, m,    //matrix size
                       B, B_large, C_large, mu, Re,   //molecular parameter
                       PotParam);
    }
    else if (strcmp( sym, "C2v") == 0) {
        cout << "calculate as C2v sym." << endl; 
        Hamiltonian = H_C2v(n0, npls, nmns, j, m,    //matrix size
                       A, B, C, B_large, C_large, mu, Re,   //molecular parameter
                       PotParam);
    }
    else if (strcmp( sym, "C3v_prolate") == 0) {
        cout << "calculate as C3v prolate sym." << endl; 
        Hamiltonian = H_C3v_prolate(n0, npls, nmns, j, m,    //matrix size
                       A, B, B_large, C_large, mu, Re,   //molecular parameter
                       PotParam);
    }
    else if (strcmp( sym, "C3v_oblate") == 0) {
        cout << "calculate as C3v obrater sym." << endl; 
        Hamiltonian = H_C3v_oblate(n0, npls, nmns, j, m,    //matrix size
                       B, C, B_large, C_large, mu, Re,   //molecular parameter
                       PotParam);
    }
    else if (strcmp( sym, "Td") == 0) {
        cout << "calculate as Td sym." << endl; 
        Hamiltonian = H_Td(n0, npls, nmns, j, m,    //matrix size
                       B, B_large, C_large, mu, Re,   //molecular parameter
                       PotParam);
    }
    else {cout << "Error " << endl;}
    PyObject* ReturnHamiltonian, *Hamiltonian_Element;
    ReturnHamiltonian = PyList_New(dimension*dimension);
    for (int i = 0; i < dimension; i++) {
        for (int j = 0; j < dimension; j++) {
            Hamiltonian_Element = PyFloat_FromDouble(Hamiltonian(i, j));    //2回以上実行しようとするとここでセグフォが出る．
            PyList_SET_ITEM(ReturnHamiltonian, j + i*dimension, Hamiltonian_Element);
            Py_INCREF(Hamiltonian_Element);
        }
    }
    return ReturnHamiltonian;
}


// addModule definition(python's name)
static PyMethodDef CSBICalc[] = {
    { "HamiltonianMatrixGeneration", HamiltonianMatrixGeneration, METH_VARARGS, ""},
    //{ "Eigenstate", Eigenstate, METH_VARARGS, ""},
    { NULL }
};

// addModule definition struct
static struct PyModuleDef CSBICalcModule = {
    PyModuleDef_HEAD_INIT,
    "CSBICalcModule",
    "CSBI modelの計算をします",
    -1,
    CSBICalc
};

// Initializes addModule
PyMODINIT_FUNC PyInit_CSBICalcModule(void)
{
    return PyModule_Create(&CSBICalcModule);
}