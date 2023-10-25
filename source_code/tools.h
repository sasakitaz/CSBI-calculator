#pragma once
#include "Wigner3jSymbol.h" //wigner 3j symbol
//#include "Parameter.h"
//#include "diagonalization_dsyevd.h"   //LAPACKを用いた対角化
#define PRINT_MAT(X) cout << #X << ":\n" << X << endl << endl   //行列の出力
using namespace std;


class tools : public MatrixParameter
{
protected:
    double kzz;     //Morse potential parameter
    double az;      //Morse potential parameter 
    double shbaromega;  //harmonic frequency of stretch
    int p;          //spherical harmonics parameter
    int q;          //spherical harmonics parameter
    int m_couple;   //angular momentum coupling in Vam and VamR
public:
    tools(int temn0, int temnpls, int temnmns, int temj, int temm, int temjrow, int temmBrow, int temkrow, int temn0row, int temvrow, int temjcolumn, int temmBcolumn, int temkcolumn, int temn0column, int temvcolumn) : MatrixParameter(temn0, temnpls, temnmns, temj, temm, temjrow, temmBrow, temkrow, temn0row, temvrow, temjcolumn, temmBcolumn, temkcolumn, temn0column, temvcolumn)
    {
    }
    double Wigner3jSymbol(int p, int q);
    double Wigner3jSymbol_couple(int p, int q, int m_couple);
    Eigen::MatrixXd DVR_Ri(double kzz, double az, double shbaromega);
    Eigen::MatrixXd DVR_Ri_vec(double kzz, double az, double shbaromega);
};

double tools::Wigner3jSymbol(int p, int q) {
    double symbol1 = wigner_3j(    jrow, p,  jcolumn, 
                                 - krow, q,  kcolumn);
    double symbol2 = wigner_3j(    jrow, p,  jcolumn,
                                - mBrow, 0, mBcolumn);
    double symbol = symbol1*symbol2;
    return symbol;
}

double tools::Wigner3jSymbol_couple(int p, int q, int m_couple) {
    double symbolpls1 = wigner_3j(    jrow,        p,  jcolumn, 
                                    - krow,        q,  kcolumn);
    double symbolpls2 = wigner_3j(    jrow,        p,  jcolumn,
                                   - mBrow, m_couple, mBcolumn);
    double symbolpls = symbolpls1*symbolpls2;
    return symbolpls;
}

Eigen::MatrixXd  tools::DVR_Ri(double kzz, double az, double shbaromega) {
    Eigen::MatrixXd x = Eigen::MatrixXd::Zero(n0 + 1, n0 + 1);
    for (int i = 1; i <= n0; i++) {
        x(i, i - 1) = (double)sqrt(i);    //creation operator
        x(i - 1, i) = (double)sqrt(i);    //annihilation operator
    }
    x = sqrt(shbaromega/(4*kzz*az*az))*x;   //position operator
    //Eigen::SelfAdjointEigenSolver< Eigen::Matrix<double, n0, n0>> s(x); 
    Eigen::SelfAdjointEigenSolver<Eigen::MatrixXd> s(x); 

    //Eigen::VectorXd eig_val = Eigen::VectorXd::Zero(x.rows());
    //Eigen::MatrixXd eig_vec = Eigen::MatrixXd::Zero(x.rows(), x.rows());
    //tie(eig_val, eig_vec) = diagonalization_dsyevd(x);
    //PRINT_MAT(s.eigenvectors());
    return s.eigenvalues();
}  

Eigen::MatrixXd  tools::DVR_Ri_vec(double kzz, double az, double shbaromega) {
    Eigen::MatrixXd x = Eigen::MatrixXd::Zero(n0 + 1, n0 + 1);
    for (int i = 1; i <= n0; i++) {
        x(i, i - 1) = (double)sqrt(i);    //creation operator
        x(i - 1, i) = (double)sqrt(i);    //annihilation operator
    }
    x = sqrt(shbaromega/(4*kzz*az*az))*x;   //position operator
    //Eigen::VectorXd eig_val = Eigen::VectorXd::Zero(x.rows());
    //Eigen::MatrixXd eig_vec = Eigen::MatrixXd::Zero(x.rows(), x.rows());
    //tie(eig_val, eig_vec) = diagonalization_dsyevd(x);
    //Eigen::SelfAdjointEigenSolver< Eigen::Matrix<double, n0 + 1, n0 + 1>> s(x);
    Eigen::SelfAdjointEigenSolver<Eigen::MatrixXd> s(x); 
    //PRINT_MAT(s.eigenvectors());
    return s.eigenvectors();
}  

/*
複数の戻り値がある場合
1.戻り値をstd::tupleにする
2.std::forward_as_tuple()で値を返す
3.std::tie()で受け取る
参考: 
*/
/*
//DVRは関数で定義。得られる固有値Riと固有ベクトルRi_vecは計算全体で同じなのでオブジェクトを生成して繰り返し回す必要がない。むしろ内部に対角化を含んでいるため何度も回すと計算コストがかかる。
tuple<Eigen::MatrixXd, Eigen::MatrixXd>  DVR(double kzz, double az) {
    Eigen::MatrixXd x = Eigen::MatrixXd::Zero(n0 + 1, n0 + 1);
    for (int i = 1; i <= n0; i++) {
        x(i, i - 1) = (double)sqrt(i);    //creation operator
        x(i - 1, i) = (double)sqrt(i);    //annihilation operator
    }
    x = sqrt(shbaromega/(4*kzz*az*az))*x;   //position operator
    Eigen::SelfAdjointEigenSolver< Eigen::Matrix<double, n0 + 1, n0 + 1>> s(x);   //三重対角行列なのでアルゴリズムにこだわれば高速化できる
    cout << "!!diagonalize_DVR!!" << endl;
    //PRINT_MAT(s.eigenvectors());
    return forward_as_tuple(s.eigenvalues(), s.eigenvectors());
}  

class DVR : public tools
{
protected:
    double kzz;     //Morse potential parameter
    double az;      //Morse potential parameter 

public:
    DVR(int temn0, int temnpls, int temnmns, int temj, int temm, int temjrow, int temmBrow, int temkrow, int temn0row, int temvrow, int temjcolumn, int temmBcolumn, int temkcolumn, int temn0column, int temvcolumn) : tools(temn0, temnpls, temnmns, temj, temm, temjrow, temmBrow, temkrow, temn0row, temvrow, temjcolumn, temmBcolumn, temkcolumn, temn0column, temvcolumn)
    {
    }
    double Ri(double kzz, double az);
    double Ri_vec(double kzz, double az);
};

Eigen::MatrixXd DVR::Ri(double kzz, double az) {
    Eigen::MatrixXd R;
    tie(R, ignore) = DVR(kzz, az);
    //PRINT_MAT(R);
    return R;
}

Eigen::MatrixXd DVR::Ri_vec(double kzz, double az) {
    Eigen::MatrixXd R_vec;
    tie(ignore, R_vec) = DVR(kzz, az);
    //PRINT_MAT(R_vec);
    return R_vec;
}

Eigen::MatrixXd Ri = getRi();
Eigen::MatrixXd Ri_vec = getRi_vec();
*/
