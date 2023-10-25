#pragma once
#include <Python.h>
#include <iostream>
#include <vector>
#include <numeric>  //accumulate
#include <omp.h> 
#include "Eigen/Core"   // x(行, 列)
#include "Eigen/Dense"  // 固有値計算ルーチンの入ったインクルードファイル
#define PRINT_MAT(X) cout << #X << ":\n" << X << endl << endl   //行列の出力
using namespace std;

class MatrixParameter 
{
public:
    MatrixParameter(int temn0, int temnpls, int temnmns, int temj, int temm, int temjrow, int temmBrow, int temkrow, int temn0row, int temvrow, int temjcolumn, int temmBcolumn, int temkcolumn, int temn0column, int temvcolumn)
        : n0(temn0)
        , npls(temnpls)
        , nmns(temnmns)
        , j(temj)
        , m(temm)
        , jrow(temjrow)
        , mBrow(temmBrow)
        , krow(temkrow)
        , n0row(temn0row)
        , vrow(temvrow)
        , lrow(m - mBrow)
        , jcolumn(temjcolumn)
        , mBcolumn(temmBcolumn)
        , kcolumn(temkcolumn)
        , n0column(temn0column)
        , vcolumn(temvcolumn)
        , lcolumn(m - mBcolumn)
    {
    }
    int matrix_size(); //matrix size
    tuple<vector<int>, vector<int>, vector<int>>size_vec(); 
    int row2();
    int row3();
    int row4();
    int column2();
    int column3();
    int column4();
    int row();
    int column();

protected:
    int n0;
    int npls;
    int nmns;
    int j;
    int m;
    int jrow;
    int mBrow;
    int krow;
    int n0row;
    int vrow;
    int lrow;
    int jcolumn;
    int mBcolumn;
    int kcolumn;
    int n0column;
    int vcolumn;
    int lcolumn;
    int nplsrow = (vrow + lrow)/2;
    int nmnsrow = (vrow - lrow)/2;
    int nplscolumn = (vcolumn + lcolumn)/2;
    int nmnscolumn = (vcolumn - lcolumn)/2;

};

int MatrixParameter::matrix_size()
{
    vector<int> dim(1, 0);
    vector<int> allowl(1, 0);
    vector<int> allowmB(1, 0);

    for (int ll = - nmns; ll <= npls; ll++){
        for (int mB = - j; mB <= j; mB++){

            int jdim = 0;
            for (int num = 0; num <= j; num++){
                int jd = (2*abs(num) + 1);
                jdim += jd;
            }

            int mminus = 0;
            int mmm;
            for (int mm = 0; mm <= abs(mB); mm++){
                if (mm == 0){
                    mmm = 0;
                }
                else {
                    mmm = (2 * (abs(mm) - 1) + 1);
                }
                mminus += mmm;
            }

            if (ll + mB == m){
                int d = (npls + 1 - abs(ll))*(jdim - mminus);
                dim.push_back(d);
                allowl.push_back(ll);
                allowmB.push_back(mB);
            }
        }
    }
    int dimension = accumulate(dim.begin(), dim.end(), 0)*(n0 + 1);
    return dimension;
}

tuple<vector<int>, vector<int>, vector<int>> MatrixParameter::size_vec()
{
    vector<int> dim(1, 0);
    vector<int> allowl(1, 0);
    vector<int> allowmB(1, 0);
    dim.pop_back();
    allowl.pop_back();
    allowmB.pop_back();
    for (int ll = - nmns; ll <= npls; ll++){
        for (int mB = - j; mB <= j; mB++){
            int jdim = 0;
            for (int num = 0; num <= j; num++){
                int jd = (2*abs(num) + 1);
                jdim += jd;
            }

            int mminus = 0;
            int mmm;
            for (int mm = 0; mm <= abs(mB); mm++){
                if (mm == 0){
                    mmm = 0;
                }
                else {
                    mmm = (2*(abs(mm) - 1) + 1);
                }
                mminus += mmm;
            }

            if (ll + mB == m){
                int d = (npls + 1 - abs(ll))*(jdim - mminus);
                dim.push_back(d);
                allowl.push_back(ll);
                allowmB.push_back(mB);
            }
        }
    }

    return forward_as_tuple(dim, allowl, allowmB);
}

int MatrixParameter::row2()
{
    int jrsum = 0;
    int jr;
    for (int numjrow = abs(mBrow); numjrow <= jrow; numjrow++){
        if (numjrow == abs(mBrow)){
            jr = 0;
        }
        else {
            jr = (2*(numjrow - 1) + 1);
        }
        jrsum += jr;
    }
    return jrsum;
}

int MatrixParameter::row3()
{
    int krsum = 0;
    for (int numkrow = - jrow; numkrow <= krow; numkrow++){
        krsum += 1;
    }
    return krsum;
}

int MatrixParameter::row4()
{
    int jjrsum = 0;
    for (int jjrow = abs(mBrow); jjrow <= j; jjrow++){
        jjrsum += 2*jjrow + 1;
    }
    return jjrsum;
}

int MatrixParameter::column2()
{
    int jcsum = 0;
    int jc;
    for (int numjcolumn = abs(mBcolumn); numjcolumn <= jcolumn; numjcolumn++){
        if (numjcolumn == abs(mBcolumn)){
            jc = 0;
        }
        else {
            jc = (2*(numjcolumn - 1) + 1);
        }
        jcsum += jc;
    }
    return jcsum;
}

int MatrixParameter::column3()
{
    int kcsum = 0;
    for (int numkcolumn = - jcolumn; numkcolumn <= kcolumn; numkcolumn++){
        kcsum += 1;
    }
    return kcsum;
}

int MatrixParameter::column4()
{
    int jjcsum = 0;
    for (int jjcolumn = abs(mBcolumn); jjcolumn <= j; jjcolumn++){
        jjcsum += 2*jjcolumn + 1;
    }
    return jjcsum;
}

int MatrixParameter::row(){
    return row2() + (row3() - 1) + (vrow - abs(lrow))/2*row4() + n0row*matrix_size()/(n0 + 1);
}

int MatrixParameter::column(){
    return column2() + (column3() - 1) + (vcolumn - abs(lcolumn))/2*column4() + n0column*matrix_size()/(n0 + 1);
}