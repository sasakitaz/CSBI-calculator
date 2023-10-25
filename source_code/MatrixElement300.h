

#pragma once
#include "tools.h"
#define PRINT_MAT(X) cout << #X << ":\n" << X << endl << endl   //行列の出力
using namespace std;


/**************************************************************************
ver.200での変更点
角運動量を考慮して運動エネルギー項を修正
参照：W. Kim et al., J. Chem. Phys. 110, 8461 (1999)

20230703
T_5_2：交換関係を計算しなおし
[A_+^+ A_-^+ - A_; A_-] -> [A_+^+ A_-^+ - A_; A_- + 1]

20230707 ver.300での変更点
Bz-Arを再現するように運動エネルギー項を修正

sqrt(3/(8*M_PI))はY_1^1の規格化定数に由来しているのでm_cpl=1のときは全て同じで修正しなくていい．
***************************************************************************/

using namespace std;

class MatrixElement : public tools
{
protected:
    int p;   //spherical harmonics parameter
    int q;   //spherical harmonics parameter

public:
    //基底クラスのコンストラクタ呼び出し
    MatrixElement(int temn0, int temnpls, int temnmns, int temj, int temm, int temjrow, int temmBrow, int temkrow, int temn0row, int temvrow, int temjcolumn, int temmBcolumn, int temkcolumn, int temn0column, int temvcolumn) : tools(temn0, temnpls, temnmns, temj, temm, temjrow, temmBrow, temkrow, temn0row, temvrow, temjcolumn, temmBcolumn, temkcolumn, temn0column, temvcolumn)
    {
    }
    double Tb();    //bend kinetic
    double Tb_1();   //
    double Tb_2();   //
    double Ts();    //stretch kitnetic
    double Ts_1();   //
    double T_3_1();   //
    double T_4_1();   //
    double T_4_2();   //
    double T_5_1();   //
    double T_5_2();   //
    double T_6_1();   //
    double T_6_2();   //
    double T_7_1();   //
    double Tr();    //internal rotation kinetic
    double Tr_symtop();
    double Tr_asymtop_1();
    double Tr_asymtop_2();
    double Tr_asymtop_3();
    double Tr_1();  //
    double Vs(double kzz, double az, double shbaromega);   //stretch potential
    double Vb();    //bend potential
    double Vr(int p, int q);    //internal rotation potential 
    double Vsb(double kzz, double az, double shbaromega);   //stretch-bend coupling potential
    double Vsr(int p, int q);   //stretch-internal rotation coupling potential
    double Vssr(int p, int q);  //stretch-internal rotation coupling potential(stretch Taylor expansion higher term)
    double Vbr(int p, int q);   //bend-internal rotation coupling potential
    double angular_coupling(int p, int q, int m_couple);
    double Vam(int p, int q, int m_couple); //angular momentum coupling potential
    double VamR(int n, double Re, int p, int q, int m_couple, double kzz, double az, double shbaromega);    //angular momentum coupling potential(R dependence)
};

double MatrixElement::Tb(){
  double me_Tb;
  if (jrow ==jcolumn && krow == kcolumn && n0row == n0column) {
      if (nplsrow - nplscolumn == + 1 && nmnsrow - nmnscolumn == + 1){
          me_Tb = 2*sqrt((nplscolumn + 1)*(nmnscolumn + 1));
      }
      else if (nplsrow - nplscolumn == - 1 && nmnsrow - nmnscolumn == - 1) {
          me_Tb = 2*sqrt((nplscolumn)*(nmnscolumn));
      }
      else if (nplsrow - nplscolumn == 0 && nmnsrow - nmnscolumn == 0) {
          me_Tb = - 2*(nplscolumn + nmnscolumn + 1);
      }
      else {
          me_Tb = 0;
      }
  }
  else {
      me_Tb = 0;
  }
  return me_Tb;
}

double MatrixElement::Tb_1(){
  double me_Tb_1;
  if (jrow ==jcolumn && krow == kcolumn) {
    if (n0row - n0column == + 1) {
      if (nplsrow - nplscolumn == + 1 && nmnsrow - nmnscolumn == + 1){
          me_Tb_1 = 2*sqrt((nplscolumn + 1)*(nmnscolumn + 1))*sqrt(n0column + 1);
      }
      else if (nplsrow - nplscolumn == - 1 && nmnsrow - nmnscolumn == - 1) {
          me_Tb_1 = 2*sqrt((nplscolumn)*(nmnscolumn))*sqrt(n0column + 1);
      }
      else if (nplsrow - nplscolumn == 0 && nmnsrow - nmnscolumn == 0) {
          me_Tb_1 = - 2*(nplscolumn + nmnscolumn + 1)*sqrt(n0column + 1);
      }
      else {
          me_Tb_1 = 0;
      }
    }
    else if (n0row - n0column == - 1) {
      if (nplsrow - nplscolumn == + 1 && nmnsrow - nmnscolumn == + 1){
          me_Tb_1 = 2*sqrt((nplscolumn + 1)*(nmnscolumn + 1))*sqrt(n0column);
      }
      else if (nplsrow - nplscolumn == - 1 && nmnsrow - nmnscolumn == - 1) {
          me_Tb_1 = 2*sqrt((nplscolumn)*(nmnscolumn))*sqrt(n0column);
      }
      else if (nplsrow - nplscolumn == 0 && nmnsrow - nmnscolumn == 0) {
          me_Tb_1 = - 2*(nplscolumn + nmnscolumn + 1)*sqrt(n0column);
      }
      else {
          me_Tb_1 = 0;
      }
    }
    else {
      me_Tb_1 = 0;
    }
  }
  else {
    me_Tb_1 = 0;
  }
  return me_Tb_1;
}

double MatrixElement::Tb_2(){
  double me_Tb_2;
  if (jrow ==jcolumn && krow == kcolumn) {
    if (n0row - n0column == + 2) {
      if (nplsrow - nplscolumn == + 1 && nmnsrow - nmnscolumn == + 1){
          me_Tb_2 = 2*sqrt((nplscolumn + 1)*(nmnscolumn + 1))*sqrt((n0column + 1)*(n0column + 2));
      }
      else if (nplsrow - nplscolumn == - 1 && nmnsrow - nmnscolumn == - 1) {
          me_Tb_2 = 2*sqrt((nplscolumn)*(nmnscolumn))*sqrt((n0column + 1)*(n0column + 2));
      }
      else if (nplsrow - nplscolumn == 0 && nmnsrow - nmnscolumn == 0) {
          me_Tb_2 = - 2*(nplscolumn + nmnscolumn + 1)*sqrt((n0column + 1)*(n0column + 2));
      }
      else {
          me_Tb_2 = 0;
      }
    }
    else if (n0row - n0column == - 2) {
      if (nplsrow - nplscolumn == + 1 && nmnsrow - nmnscolumn == + 1){
          me_Tb_2 = 2*sqrt((nplscolumn + 1)*(nmnscolumn + 1))*sqrt((n0column)*(n0column - 1));
      }
      else if (nplsrow - nplscolumn == - 1 && nmnsrow - nmnscolumn == - 1) {
          me_Tb_2 = 2*sqrt((nplscolumn)*(nmnscolumn))*sqrt((n0column)*(n0column - 1));
      }
      else if (nplsrow - nplscolumn == 0 && nmnsrow - nmnscolumn == 0) {
          me_Tb_2 = - 2*(nplscolumn + nmnscolumn + 1)*sqrt((n0column)*(n0column - 1));
      }
      else {
          me_Tb_2 = 0;
      }
    }
    else if (n0row - n0column == 0) {
      if (nplsrow - nplscolumn == + 1 && nmnsrow - nmnscolumn == + 1){
          me_Tb_2 = 2*sqrt((nplscolumn + 1)*(nmnscolumn + 1))*(2*n0column + 1);
      }
      else if (nplsrow - nplscolumn == - 1 && nmnsrow - nmnscolumn == - 1) {
          me_Tb_2 = 2*sqrt((nplscolumn)*(nmnscolumn))*(2*n0column + 1);
      }
      else if (nplsrow - nplscolumn == 0 && nmnsrow - nmnscolumn == 0) {
          me_Tb_2 = - 2*(nplscolumn + nmnscolumn + 1)*(2*n0column + 1);
      }
      else {
          me_Tb_2 = 0;
      }
    }
    else {
      me_Tb_2 = 0;
    }
  }
  else {
    me_Tb_2 = 0;
  }
  return me_Tb_2;
}

double MatrixElement::Ts(){
    double me_Ts;
    if (jrow == jcolumn && krow == kcolumn && nplsrow == nplscolumn && nmnsrow == nmnscolumn){
        switch (n0row - n0column){
            case 0:
                me_Ts = - 2*n0column - 1;
                break;
            case + 2:
                me_Ts = sqrt((n0column + 1)*(n0column + 2));
                break;
            case - 2:
                me_Ts = sqrt(n0column*(n0column - 1));
                break;
            default:
                me_Ts = 0;
                break;
        }
    }
    else {
        me_Ts = 0;
    }
    return me_Ts;
}

double MatrixElement::Ts_1(){
  double me_Ts_1;
  if (jrow == jcolumn && krow == kcolumn) {
    if (nplsrow - nplscolumn == + 1 && nmnsrow - nmnscolumn == + 1){
      if (n0row - n0column == + 2) {
        me_Ts_1 = sqrt((n0column + 1)*(n0column + 2))*sqrt((nplscolumn + 1)*(nmnscolumn + 1));
      }
      else if (n0row - n0column == - 2) {
        me_Ts_1 = sqrt(n0column*(n0column - 1))*sqrt((nplscolumn + 1)*(nmnscolumn + 1));
      }
      else if (n0row - n0column == 0) {
        me_Ts_1 = (- 2*n0column - 1)*sqrt((nplscolumn + 1)*(nmnscolumn + 1));
      }
      else {
        me_Ts_1 = 0;
      }
    }
    else if (nplsrow - nplscolumn == - 1 && nmnsrow - nmnscolumn == - 1) {
      if (n0row - n0column == + 2) {
        me_Ts_1 = sqrt((n0column + 1)*(n0column + 2))*sqrt((nplscolumn)*(nmnscolumn));
      }
      else if (n0row - n0column == - 2) {
        me_Ts_1 = sqrt(n0column*(n0column - 1))*sqrt((nplscolumn)*(nmnscolumn));
      }
      else if (n0row - n0column == 0) {
        me_Ts_1 = (- 2*n0column - 1)*sqrt((nplscolumn)*(nmnscolumn));
      }
      else {
        me_Ts_1 = 0;
      }
    }
    else if (nplsrow - nplscolumn == 0 && nmnsrow - nmnscolumn == 0) {
      if (n0row - n0column == + 2) {
        me_Ts_1 = sqrt((n0column + 1)*(n0column + 2))*(nplscolumn + nmnscolumn + 1);
      }
      else if (n0row - n0column == - 2) {
        me_Ts_1 = sqrt(n0column*(n0column - 1))*(nplscolumn + nmnscolumn + 1);
      }
      else if (n0row - n0column == 0) {
        me_Ts_1 = (- 2*n0column - 1)*(nplscolumn + nmnscolumn + 1);
      }
      else {
        me_Ts_1 = 0;
      }
    }
    else {
      me_Ts_1 = 0;
    }
  }
  else {
    me_Ts_1 = 0;
  }
  return me_Ts_1;
}

double MatrixElement::T_3_1(){
  double me_T_3_1;
  if (n0row == n0column && nplsrow == nplscolumn && nmnsrow == nmnscolumn && jrow ==jcolumn && krow == kcolumn) {
    me_T_3_1 = nplscolumn*nplscolumn + nmnscolumn*nmnscolumn - 2*nplscolumn*nmnscolumn;
  }
  else {
    me_T_3_1 = 0;
  }
  return me_T_3_1;
}

double MatrixElement::T_4_1(){
  double me_T_4_1;
  if (nplsrow == nplscolumn && nmnsrow == nmnscolumn && jrow ==jcolumn && krow == kcolumn) {
    if (n0row - n0column == + 2) {
      me_T_4_1 = sqrt((n0column + 1)*(n0column + 2));
    }
    else if (n0row - n0column == - 2) {
      me_T_4_1 = - sqrt(n0column*(n0column - 1));
    }
    else if (n0row - n0column == 0) {
      me_T_4_1 = 1;
    }
    else {
      me_T_4_1 = 0;
    }
  }
  else {
    me_T_4_1 = 0;
  }
  return me_T_4_1;
}

double MatrixElement::T_5_1(){
  double me_T_5_1;
  if (jrow ==jcolumn && krow == kcolumn) {
    if (n0row - n0column == + 2) {
      if (nplsrow - nplscolumn == + 1 && nmnsrow - nmnscolumn == + 1) {
        me_T_5_1 = sqrt((nplscolumn + 1)*(nmnscolumn + 1))*sqrt((n0column + 1)*(n0column + 2));
      }
      else if (nplsrow - nplscolumn == - 1 && nmnsrow - nmnscolumn == - 1) {
        me_T_5_1 = - sqrt(nplscolumn*nmnscolumn)*sqrt((n0column + 1)*(n0column + 2));
      }
      else if (nplsrow - nplscolumn == 0 && nmnsrow - nmnscolumn == 0) {
        me_T_5_1 = sqrt((n0column + 1)*(n0column + 2));
      }
      else {
        me_T_5_1 = 0;
      }
    }
    else if (n0row - n0column == - 2) {
      if (nplsrow - nplscolumn == + 1 && nmnsrow - nmnscolumn == + 1) {
        me_T_5_1 = - sqrt((nplscolumn + 1)*(nmnscolumn + 1))*sqrt(n0column*(n0column - 1));
      }
      else if (nplsrow - nplscolumn == - 1 && nmnsrow - nmnscolumn == - 1) {
        me_T_5_1 = sqrt(nplscolumn*nmnscolumn)*sqrt(n0column*(n0column - 1));
      }
      else if (nplsrow - nplscolumn == 0 && nmnsrow - nmnscolumn == 0) {
        me_T_5_1 = - sqrt((n0column)*(n0column));
      }
      else {
        me_T_5_1 = 0;
      }
    }
    else {
      me_T_5_1 = 0;
    }
  }
  else {
    me_T_5_1 = 0;
  }
  return me_T_5_1;
}

double MatrixElement::T_5_2(){
  double me_T_5_2;
  if (jrow - jcolumn == 0 && krow - kcolumn == 0) {
    if (n0row - n0column == + 1) {
      if (nplsrow - nplscolumn == + 1 && nmnsrow - nmnscolumn == + 1) {
        me_T_5_2 = sqrt((nplscolumn + 1)*(nmnscolumn + 1))*sqrt(n0column + 1);
      }
      else if (nplsrow - nplscolumn == - 1 && nmnsrow - nmnscolumn == - 1) {
        me_T_5_2 = - sqrt(nplscolumn*nmnscolumn)*sqrt(n0column + 1);
      }
      else {
        me_T_5_2 = 0;
      }
    }
    else if (n0row - n0column == - 1) {
      if (nplsrow - nplscolumn == + 1 && nmnsrow - nmnscolumn == + 1) {
        me_T_5_2 = - sqrt((nplscolumn + 1)*(nmnscolumn + 1))*sqrt(n0column);
      }
      else if (nplsrow - nplscolumn == - 1 && nmnsrow - nmnscolumn == - 1) {
        me_T_5_2 = sqrt(nplscolumn*nmnscolumn)*sqrt(n0column);
      }
      else {
        me_T_5_2 = 0;
      }
    }
    else {
      me_T_5_2 = 0;
    }
  }
  else {
    me_T_5_2 = 0;
  }
  return me_T_5_2;
}

double MatrixElement::T_6_1(){
  double me_T_6_1;
  if (jrow == jcolumn && krow == kcolumn) {
    if (n0row - n0column == + 1) {
      if (mBrow - mBcolumn == + 1) {
        if (nplsrow - nplscolumn == - 1) {
          me_T_6_1 = - sqrt(nplscolumn)*sqrt((jcolumn - mBcolumn)*(jcolumn + mBcolumn + 1))*sqrt(n0column + 1);
        }
        else if (nmnsrow - nmnscolumn == + 1) {
          me_T_6_1 = sqrt(nmnscolumn + 1)*sqrt((jcolumn - mBcolumn)*(jcolumn + mBcolumn + 1))*sqrt(n0column + 1);
        }
        else {
          me_T_6_1 = 0;
        }
      }
      else if (mBrow - mBcolumn == - 1) {
        if (nplsrow - nplscolumn == + 1) {
          me_T_6_1 = - sqrt(nplscolumn + 1)*sqrt((jcolumn + mBcolumn)*(jcolumn - mBcolumn + 1))*sqrt(n0column + 1);
        }
        else if (nmnsrow - nmnscolumn == - 1) {
          me_T_6_1 = sqrt(nmnscolumn)*sqrt((jcolumn + mBcolumn)*(jcolumn - mBcolumn + 1))*sqrt(n0column + 1);
        }
        else {
          me_T_6_1 = 0;
        }
      }
      else {
        me_T_6_1 = 0;
      }
    }
    else if (n0row - n0column == - 1) {
      if (mBrow - mBcolumn == + 1) {
        if (nplsrow - nplscolumn == - 1) {
          me_T_6_1 = - sqrt(nplscolumn)*sqrt((jcolumn - mBcolumn)*(jcolumn + mBcolumn + 1))*sqrt(n0column);
        }
        else if (nmnsrow - nmnscolumn == + 1) {
          me_T_6_1 = sqrt(nmnscolumn + 1)*sqrt((jcolumn - mBcolumn)*(jcolumn + mBcolumn + 1))*sqrt(n0column);
        }
        else {
          me_T_6_1 = 0;
        }
      }
      else if (mBrow - mBcolumn == - 1) {
        if (nplsrow - nplscolumn == + 1) {
          me_T_6_1 = - sqrt(nplscolumn + 1)*sqrt((jcolumn + mBcolumn)*(jcolumn - mBcolumn + 1))*sqrt(n0column);
        }
        else if (nmnsrow - nmnscolumn == - 1) {
          me_T_6_1 = sqrt(nmnscolumn)*sqrt((jcolumn + mBcolumn)*(jcolumn - mBcolumn + 1))*sqrt(n0column);
        }
        else {
          me_T_6_1 = 0;
        }
      }
      else {
        me_T_6_1 = 0;
      }
    }
    else {
      me_T_6_1 = 0;
    }
  }
  else {
    me_T_6_1 = 0;
  }
  return me_T_6_1;
}

double MatrixElement::T_6_2(){
  double me_T_6_2;
  if (jrow == jcolumn && krow == kcolumn) {
    if (n0row - n0column == + 1) {
      if (mBrow - mBcolumn == + 1) {
        if (nplsrow - nplscolumn == - 1) {
          me_T_6_2 = - sqrt(nplscolumn)*sqrt((jcolumn - mBcolumn)*(jcolumn + mBcolumn + 1))*sqrt(n0column + 1);
        }
        else if (nmnsrow - nmnscolumn == + 1) {
          me_T_6_2 = - sqrt(nmnscolumn + 1)*sqrt((jcolumn - mBcolumn)*(jcolumn + mBcolumn + 1))*sqrt(n0column + 1);
        }
        else {
          me_T_6_2 = 0;
        }
      }
      else if (mBrow - mBcolumn == - 1) {
        if (nplsrow - nplscolumn == + 1) {
          me_T_6_2 = sqrt(nplscolumn + 1)*sqrt((jcolumn + mBcolumn)*(jcolumn - mBcolumn + 1))*sqrt(n0column + 1);
        }
        else if (nmnsrow - nmnscolumn == - 1) {
          me_T_6_2 = sqrt(nmnscolumn)*sqrt((jcolumn + mBcolumn)*(jcolumn - mBcolumn + 1))*sqrt(n0column + 1);
        }
        else {
          me_T_6_2 = 0;
        }
      }
      else {
        me_T_6_2 = 0;
      }
    }
    else if (n0row - n0column == - 1) {
      if (mBrow - mBcolumn == + 1) {
        if (nplsrow - nplscolumn == - 1) {
          me_T_6_2 = sqrt(nplscolumn)*sqrt((jcolumn - mBcolumn)*(jcolumn + mBcolumn + 1))*sqrt(n0column);
        }
        else if (nmnsrow - nmnscolumn == + 1) {
          me_T_6_2 = sqrt(nmnscolumn + 1)*sqrt((jcolumn - mBcolumn)*(jcolumn + mBcolumn + 1))*sqrt(n0column);
        }
        else {
          me_T_6_2 = 0;
        }
      }
      else if (mBrow - mBcolumn == - 1) {
        if (nplsrow - nplscolumn == + 1) {
          me_T_6_2 = - sqrt(nplscolumn + 1)*sqrt((jcolumn + mBcolumn)*(jcolumn - mBcolumn + 1))*sqrt(n0column);
        }
        else if (nmnsrow - nmnscolumn == - 1) {
          me_T_6_2 = - sqrt(nmnscolumn)*sqrt((jcolumn + mBcolumn)*(jcolumn - mBcolumn + 1))*sqrt(n0column);
        }
        else {
          me_T_6_2 = 0;
        }
      }
      else {
        me_T_6_2 = 0;
      }
    }
    else {
      me_T_6_2 = 0;
    }
  }
  else {
    me_T_6_2 = 0;
  }
  return me_T_6_2;
}

double MatrixElement::T_7_1(){
  double me_T_7_1;
  if (jrow == jcolumn && krow == kcolumn && n0row == n0column && nplsrow == nplscolumn && nmnsrow == nmnscolumn) {
    me_T_7_1 = (nplscolumn + nmnscolumn + 1)*mBcolumn;
  }
  else {
    me_T_7_1 = 0;
  }
  return me_T_7_1;
}

double MatrixElement::Tr(){
    double me_Tr;
    if (jrow == jcolumn && krow == kcolumn && n0row == n0column && nplsrow == nplscolumn && nmnsrow == nmnscolumn) {
        me_Tr = jrow*(jrow + 1);
    }
    else {
        me_Tr = 0;
    }
    return me_Tr;
}

double MatrixElement::Tr_symtop(){
    double me_Tr_sym;
    if (jrow == jcolumn && krow == kcolumn && n0row == n0column && nplsrow == nplscolumn && nmnsrow == nmnscolumn) {
        me_Tr_sym = kcolumn*kcolumn;
    }
    else {
        me_Tr_sym = 0;
    }
    return me_Tr_sym;
}

//Bernas p.203
double MatrixElement::Tr_asymtop_1(){
    double me_Tr_asym_1;
    if (jrow == jcolumn && krow == kcolumn && n0row == n0column && nplsrow == nplscolumn && nmnsrow == nmnscolumn) {
        me_Tr_asym_1 = jcolumn*(jcolumn + 1);
    }
    else {
        me_Tr_asym_1 = 0;
    }
    return me_Tr_asym_1;
}
double MatrixElement::Tr_asymtop_2(){
    double me_Tr_asym_2;
    if (jrow == jcolumn && krow == kcolumn && n0row == n0column && nplsrow == nplscolumn && nmnsrow == nmnscolumn) {
        me_Tr_asym_2 =  kcolumn*kcolumn;
    }
    else {
        me_Tr_asym_2 = 0;
    }
    return me_Tr_asym_2;
}
double MatrixElement::Tr_asymtop_3(){
    double me_Tr_asym_3;
    if (jrow == jcolumn && n0row == n0column && nplsrow == nplscolumn && nmnsrow == nmnscolumn) {
        if (krow - kcolumn == + 2) {
          me_Tr_asym_3 = sqrt((jcolumn - kcolumn)*(kcolumn + kcolumn + 1)*(jcolumn - kcolumn + 1)*(jcolumn + kcolumn + 2));
        }
        else if (krow - kcolumn == - 2) {
          me_Tr_asym_3 = sqrt((jcolumn + kcolumn)*(kcolumn - kcolumn + 1)*(jcolumn + kcolumn - 1)*(jcolumn - kcolumn + 2));
        }
        else {
          me_Tr_asym_3 = 0;
        }
    }
    else {
        me_Tr_asym_3 = 0;
    }
    return me_Tr_asym_3;
}

double MatrixElement::Tr_1(){
    double me_Tr_1;
    if (jrow == jcolumn && krow == kcolumn && n0row == n0column && nplsrow == nplscolumn && nmnsrow == nmnscolumn) {
        me_Tr_1 = mBcolumn^2;
    }
    else {
        me_Tr_1 = 0;
    }
    return me_Tr_1;
}

double MatrixElement::Vs(double kzz, double az, double shbaromega){
    double me_Vs;
    //PRINT_MAT(Ri);
    tools dvr(n0, npls, nmns, j, m, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
    Eigen::MatrixXd Ri = dvr.DVR_Ri(kzz, az, shbaromega);
    Eigen::MatrixXd Ri_vec = dvr.DVR_Ri_vec(kzz, az, shbaromega);
    double VVs = 0;
    for (int i = 0; i <= n0; i++) {
        VVs += (1 - exp(-az*Ri(i, 0)))*(1 - exp(-az*Ri(i, 0)))*Ri_vec(n0row, i)*Ri_vec(n0column, i);
    }
    //Vs
    if (jrow == jcolumn && krow == kcolumn && nplsrow == nplscolumn && nmnsrow == nmnscolumn) {
        me_Vs = VVs;
    }
    else {
        me_Vs = 0;
    }
    return me_Vs;
}

double MatrixElement::Vb() {
    double me_Vb;
    if (jrow == jcolumn && krow == kcolumn && n0row == n0column) {
        if (nplsrow - nplscolumn == + 1 && nmnsrow - nmnscolumn == + 1){
            me_Vb = 2*sqrt((nplscolumn + 1)*(nmnscolumn + 1));
        }
        else if (nplsrow - nplscolumn == - 1 && nmnsrow - nmnscolumn == - 1) {
            me_Vb = 2*sqrt((nplscolumn)*(nmnscolumn));
        }
        else if (nplsrow - nplscolumn == 0 && nmnsrow - nmnscolumn == 0) {
            me_Vb = 2*(nplscolumn + nmnscolumn + 1);
        }
        else {
            me_Vb = 0;
        }
    }
    else {
        me_Vb = 0;
    }
    return me_Vb;
}

double MatrixElement::Vr(int p, int q) {
    double me_Vr;
    if (n0row == n0column && nplsrow == nplscolumn && nmnsrow == nmnscolumn) {
        me_Vr = pow((-1), (mBrow - kcolumn))*sqrt((2*jcolumn + 1)*(2*jrow + 1))*tools::Wigner3jSymbol(p, q);
    }
    else {
        me_Vr = 0;
    }
    return me_Vr;
}

double MatrixElement::Vsb(double kzz, double az, double shbaromega) {
    //unitary matrix product
    double VVsb = 0;
    tools dvr(n0, npls, nmns, j, m, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
    Eigen::MatrixXd Ri = dvr.DVR_Ri(kzz, az, shbaromega);
    Eigen::MatrixXd Ri_vec = dvr.DVR_Ri_vec(kzz, az, shbaromega);
    for (int i = 0; i <= n0; i++) {
        VVsb += (1 - exp(-az*Ri(i, 0)))*Ri_vec(n0row, i)*Ri_vec(n0column, i);
    }
    //Vsb
    double me_Vsb;
    if (jrow == jcolumn && krow == kcolumn) {
        if (nplsrow - nplscolumn == + 1 && nmnsrow - nmnscolumn == + 1) {
            me_Vsb = 2*sqrt((nplscolumn + 1)*(nmnscolumn + 1))*VVsb;
        }
        else if (nplsrow - nplscolumn == - 1 && nmnsrow - nmnscolumn == - 1) {
            me_Vsb = 2*sqrt((nplscolumn)*(nmnscolumn))*VVsb;
        }
        else if (nplsrow - nplscolumn == 0 && nmnsrow - nmnscolumn == 0) {
            me_Vsb = 2*(nplscolumn + nmnscolumn + 1)*VVsb;
        }
        else {
            me_Vsb = 0;
        }
    }
    else {
        me_Vsb = 0;
    }
    return me_Vsb;
}

double MatrixElement::Vsr(int p, int q) {
    double me_Vsr;
    if (nplsrow == nplscolumn && nmnsrow == nmnscolumn) {
        if (n0row - n0column == + 1) {
            me_Vsr = sqrt(n0column + 1)
                    *pow((-1), (mBcolumn - kcolumn))*sqrt((2*jcolumn + 1)*(2*jrow + 1))*tools::Wigner3jSymbol(p, q);
        }
        else if (n0row - n0column == - 1) {
            me_Vsr = sqrt(n0column)
                    *pow((-1), (mBcolumn - kcolumn))*sqrt((2*jcolumn + 1)*(2*jrow + 1))*tools::Wigner3jSymbol(p, q);
        }
        else {
            me_Vsr = 0;
        }
    }
    else {
        me_Vsr = 0;
    }
    return me_Vsr;
}

double MatrixElement::Vssr(int p, int q) {
    double me_Vssr;
    if (nplsrow == nplscolumn && nmnsrow == nmnscolumn) {
        if (n0row - n0column == 0) {
            me_Vssr = (2*n0column + 1)
                    *pow((-1), (mBcolumn - kcolumn))*sqrt((2*jcolumn + 1)*(2*jrow + 1))*tools::Wigner3jSymbol(p, q);
        }
        else if (n0row - n0column == + 2) {
            me_Vssr = sqrt((n0column + 1)*(n0column + 2))
                    *pow((-1), (mBcolumn - kcolumn))*sqrt((2*jcolumn + 1)*(2*jrow + 1))*tools::Wigner3jSymbol(p, q);
        }
        else if (n0row - n0column == - 2) {
            me_Vssr = sqrt(n0column*(n0column - 1))
                    *pow((-1), (mBcolumn - kcolumn))*sqrt((2*jcolumn + 1)*(2*jrow + 1))*tools::Wigner3jSymbol(p, q);
        }
        else {
            me_Vssr = 0;
        }
    }
    else {
        me_Vssr = 0;
    }
    return me_Vssr;
}

double MatrixElement::Vbr(int p, int q) {
    double me_Vbr;
    if (n0row == n0column) {
        if (nplsrow - nplscolumn == + 1 && nmnsrow - nmnscolumn == + 1) {
            me_Vbr = 2*sqrt((nplscolumn + 1)*(nmnscolumn + 1))
                        *pow((-1), (mBrow - krow))*sqrt((2*jcolumn + 1)*(2*jrow + 1))*tools::Wigner3jSymbol(p, q);
        }
        else if (nplsrow - nplscolumn == - 1 && nmnsrow - nmnscolumn == - 1) {
            me_Vbr = 2*sqrt((nplscolumn)*(nmnscolumn))
                        *pow((-1), (mBrow - krow))*sqrt((2*jcolumn + 1)*(2*jrow + 1))*tools::Wigner3jSymbol(p, q);
        }
        else if (nplsrow - nplscolumn == 0 && nmnsrow - nmnscolumn == 0) {
            me_Vbr = 2*(nplscolumn + nmnscolumn + 1)
                        *pow((-1), (mBrow - krow))*sqrt((2*jcolumn + 1)*(2*jrow + 1))*tools::Wigner3jSymbol(p, q);
        }
        else {
            me_Vbr = 0;
        }
    }
    else {
        me_Vbr = 0;
    }
    return me_Vbr;
}

//Pythonのときの旧プログラムから関数自体を変更
double MatrixElement::angular_coupling(int p, int q, int m_couple) {
    double me_Vam = 0;
    //m_couple = \pm 1のみを想定。それ以外は行列要素が異なるためこの行列要素は使えない。
    if (m_couple == + 1 ) {
        if (nplsrow - nplscolumn == + 1 && nmnsrow - nmnscolumn == 0) {
            me_Vam =  sqrt(nplscolumn + 1) 
                      *pow((-1), (mBcolumn - kcolumn))*sqrt((2*jcolumn + 1)*(2*jrow + 1))*tools::Wigner3jSymbol_couple(p, q, - 1);
        }
        else if (nplsrow - nplscolumn == 0 && nmnsrow - nmnscolumn == - 1) {
            me_Vam =  sqrt(nmnscolumn)
                      *pow((-1), (mBcolumn - kcolumn))*sqrt((2*jcolumn + 1)*(2*jrow + 1))*tools::Wigner3jSymbol_couple(p, q, - 1);
        }
        else {
            me_Vam = 0;
        }
    }

    else if (m_couple == - 1) {
        if (nplsrow - nplscolumn == - 1 && nmnsrow - nmnscolumn == 0) {
            me_Vam =  sqrt(nplscolumn) 
                      *pow((-1), (mBcolumn - kcolumn))*sqrt((2*jcolumn + 1)*(2*jrow + 1))*tools::Wigner3jSymbol_couple(p, q, + 1);
        }
        else if (nplsrow - nplscolumn == 0 && nmnsrow - nmnscolumn == + 1) {
            me_Vam =  sqrt(nmnscolumn + 1)
                      *pow((-1), (mBcolumn - kcolumn))*sqrt((2*jcolumn + 1)*(2*jrow + 1))*tools::Wigner3jSymbol_couple(p, q, + 1);
        }
        else {
            me_Vam = 0;
        }
    }
    else {
        cout << "!! ERROR, m_couple is not 1 !!" << endl;
        return 0;
    }
    return me_Vam;
}

double MatrixElement::Vam(int p, int q, int m_couple) {
    double me_Vam = 0;
    if (n0row - n0column == 0) {
        me_Vam = MatrixElement::angular_coupling(p, q, m_couple);
    }
    else {
        me_Vam= 0;
    }
    return me_Vam;
}

double MatrixElement::VamR(int n, double Re, int p, int q, int m_couple, double kzz, double az, double shbaromega) {
    double VVamR = 0;
    tools dvr(n0, npls, nmns, j, m, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
    Eigen::MatrixXd Ri = dvr.DVR_Ri(kzz, az, shbaromega);
    Eigen::MatrixXd Ri_vec = dvr.DVR_Ri_vec(kzz, az, shbaromega);
    for (int i = 0; i <= n0; i++) {
        VVamR += pow((Ri(i, 0) + Re), (-n))*Ri_vec(n0row, i)*Ri_vec(n0column, i);
    }
    double me_VamR = 0;
    me_VamR = VVamR*MatrixElement::angular_coupling(p, q, m_couple);
    return me_VamR;
}

//K symmetry
Eigen::MatrixXd H_K (int n0, int npls, int nmns, int j, int m,    //matrix size
                     double B_large, double C_large, double mu, double Re,   //molecular parameter
                     vector<double> PotParam
                     ) 
{    
    //constant
    double hbar = 1.054571817*pow(10, -34);
    double c = 2.99792458*pow(10, 8);

    double Ix = hbar*hbar/(2*B_large)*5.03412*pow(10, 22);
    double Iz = hbar*hbar/(2*C_large)*5.03412*pow(10, 22); //長さはm単位

    double mub = mu;

    double Re2Ix = (Re*pow(10, -10))*(Re*pow(10, -10))/Ix;
    double omegas = sqrt(2*PotParam[0]*PotParam[1]*PotParam[1]*1.98645*pow(10, -23)*pow(10, 20)/mu);   //単位はs-1
    double omegab = sqrt(2*PotParam[2]*1.98645*pow(10, -23)*pow(10, 20)/mub);   //単位はs-1
    double shbaromega = 1/(2*M_PI)*omegas/c/100;    //単位変換で1/hcをかけ、hbarをかけるため、2\piが必要。
    double bhbaromega = 1/(2*M_PI)*omegab/c/100;
    double ReIxsqrt2mubomegas = Re*pow(10, -10)/Ix*sqrt(2*mub*hbar/omegas);
    //double ReIxsqrt2muomegas = Re*pow(10, -10)/Ix*sqrt(2*mu*hbar/omegas);
    double hbar2Ix = hbar*hbar/Ix*5.03412*pow(10, 22); //1 J = 5.03412 \times 10^22 cm-1
    double hbar2Iz = hbar*hbar/Iz*5.03412*pow(10, 22);
    //double Resqrt2mubhbaromegas = hbar2Ix*Re*pow(10, -10)*sqrt(2*mu*omegas/hbar);
    //double Resqrt2muhbaromegas = hbar2Ix*Re*pow(10, -10)*sqrt(2*mu*omegas/hbar);
    //double omegasomegab = shbaromega/bhbaromega;
    double Vbcoeff = hbar/(2*mub*omegab)*pow(10, 20);
    double Vscoeff = hbar/(2*mu*omegas)*pow(10, 20);

    double kzz = PotParam[0];
    double az = PotParam[1];
    double kxx = PotParam[2];
    double kxxz = PotParam[3];
    double V001 = PotParam[4];
    double V002 = PotParam[5];
    double V022 = PotParam[6];
    double V003 = PotParam[7];
    double V203 = PotParam[8];
    double V303 = PotParam[9];
    double V004 = PotParam[10];
    double VR001 = PotParam[11];
    double VR002 = PotParam[12];
    double VR202 = PotParam[13];
    double VR003 = PotParam[14];
    double VR203 = PotParam[15];
    double VR303 = PotParam[16];
    double VR004 = PotParam[17];
    double VRR001 = PotParam[18];
    double VRR002 = PotParam[19];
    double VRR202 = PotParam[20];
    double VRR003 = PotParam[21];
    double VRR203 = PotParam[22];
    double VRR303 = PotParam[23];
    double VRR004 = PotParam[24];
    double Vrho001 = PotParam[25];
    double Vrho002 = PotParam[26];
    double Vrho202 = PotParam[27];
    double Vrho003 = PotParam[28];
    double Vrho203 = PotParam[29];
    double Vrho303 = PotParam[30];
    double Vrho004 = PotParam[31];
    double Vam011_0 = PotParam[32];
    double Vam012_0 = PotParam[33];
    double Vam022_0 = PotParam[34];
    double Vam212_0 = PotParam[35];
    double Vam222_0 = PotParam[36];
    double Vam013_0 = PotParam[37];
    double Vam023_0 = PotParam[38];
    double Vam011_6 = PotParam[39];
    double Vam012_6 = PotParam[40];
    double Vam022_6 = PotParam[41];
    double Vam212_6 = PotParam[42];
    double Vam222_6 = PotParam[43];
    double Vam013_6 = PotParam[44];
    double Vam023_6 = PotParam[45];
    double Vam011_8 = PotParam[46];
    double Vam012_8 = PotParam[47];
    double Vam022_8 = PotParam[48];
    double Vam212_8 = PotParam[49];
    double Vam222_8 = PotParam[50];
    double Vam013_8 = PotParam[51];
    double Vam023_8 = PotParam[52];
    double Vam011_10 = PotParam[53];
    double Vam012_10 = PotParam[54];
    double Vam022_10 = PotParam[55];
    double Vam212_10 = PotParam[56];
    double Vam222_10 = PotParam[57];
    double Vam013_10 = PotParam[58];
    double Vam023_10 = PotParam[59];

    MatrixParameter dim(n0, npls, nmns, j, m, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
    //vector<vector<double>> result(dim.matrix_size(), vector<double>(dim.matrix_size()));
    Eigen::MatrixXd result = Eigen::MatrixXd::Ones(dim.matrix_size(), dim.matrix_size());
    vector<int> drow(1, 0);
    vector<int> ddrow(1, 0);
    int dddrow= 0;
    for (int mBrow = - j; mBrow <= j; mBrow++) {                                                    // assign row mB
        for (int vrow = abs(m - mBrow); vrow <= (npls + nmns - abs(m - mBrow)); vrow += 2) {  //assign row v
            int jrdim = 0;
            int jdrow;
            for (int num = 0; num<= j; num++) {
                jdrow = (2 * abs(num) + 1);
                jrdim += jdrow;
            }
            int mrminus = 0;
            int mmmrow;
            for (int mm = 0; mm <= abs(mBrow); mm++) {
                if (mm == 0) {
                    mmmrow = 0;
                }
                else {
                    mmmrow = (2 * (abs(mm) - 1) + 1);
                }
                mrminus += mmmrow;
            }
            int d = (npls + 1 - abs(m - mBrow))*(jrdim - mrminus);
            drow.push_back(d);
            if (d != drow[drow.size() - 2]) {
                ddrow.push_back(d);
                dddrow += ddrow[ddrow.size() - 2];
            }

            vector<int> dcolumn(1, 0);
            vector<int> ddcolumn(1, 0);
            int dddcolumn = 0;
            for (int mBcolumn = - j; mBcolumn <= j; mBcolumn++) {                                       // assign column mB
                for (int vcolumn = abs(m - mBcolumn); vcolumn <= (npls + nmns - abs(m - mBcolumn)); vcolumn += 2) {   // assign column v
                    int jcdim = 0;
                    int jdcolumn;
                    for (int num = 0; num<= j; num++) {
                        jdcolumn = (2 * abs(num) + 1);
                        jcdim += jdcolumn;
                        }
                    int mcminus = 0;
                    int mmmcolumn;
                    for (int mm = 0; mm <= abs(mBcolumn); mm++) {
                        if (mm == 0) {
                            mmmcolumn = 0;
                        }
                        else {
                            mmmcolumn = (2 * (abs(mm) - 1) + 1);
                        }
                        mcminus += mmmcolumn;
                    }
                    int d = (npls + 1 - abs(m - mBcolumn))*(jcdim - mcminus);
                    dcolumn.push_back(d);
                    if (d != dcolumn[dcolumn.size() - 2]) { //dcolumn.size() - 2 > 0の条件を追加したらエラーが消えるかもしれない．
                        ddcolumn.push_back(d);
                        dddcolumn += ddcolumn[ddcolumn.size() - 2];
                    }

                    #pragma omp parallel for num_threads(12)
                    for (int jrow = abs(mBrow); jrow <= j; jrow++) {                                            // assign row j
                        for (int krow = - jrow; krow <= jrow; krow++) {                                         // assign row k
                            for (int n0row = 0; n0row <= n0; n0row++) {                                         // assign row n0
                                for (int jcolumn = abs(mBcolumn); jcolumn <= j; jcolumn++) {                                                // assign column j      
                                    for (int kcolumn = - jcolumn; kcolumn <= jcolumn; kcolumn++) {                                          // assign column k
                                        for (int n0column = 0; n0column <= n0; n0column++) {                                                // assign column n0
                                            // matrix element
                                            MatrixElement matrix(n0, npls, nmns, j, m, jrow, mBrow, krow, n0row, vrow, jcolumn, mBcolumn, kcolumn, n0column, vcolumn);
                                            result(dddrow + matrix.row(), dddcolumn + matrix.column())
                                             = 

                                              - bhbaromega/4*(
                                                + (1 + Re2Ix*mu)*matrix.Tb()    //Tb
                                                + ReIxsqrt2mubomegas*sqrt(mub/mu)*matrix.Tb_1()
                                                + hbar2Ix/2*1/shbaromega*mub/mu*matrix.Tb_2()
                                                )

                                              - shbaromega/4*matrix.Ts()    //Ts
                                                - hbar2Ix/4*omegas/omegab*mu/mub*matrix.Ts_1()
                                              
                                              + hbar2Iz*matrix.T_3_1()
                                              - hbar2Ix/2*matrix.T_4_1()

                                              + hbar2Ix/2*matrix.T_5_1()
                                              + shbaromega*ReIxsqrt2mubomegas/2*matrix.T_5_2()
                                              + 1/sqrt(2)*hbar2Ix/2*sqrt(omegab/omegas)*sqrt(mub/mu)*matrix.T_6_1()
                                              + 1/sqrt(2)*hbar2Ix/2*sqrt(omegas/omegab)*sqrt(mu/mub)*matrix.T_6_2()
                                              + hbar2Iz*matrix.T_7_1()
                                              
                                              + kzz*matrix.Vs(kzz, az, shbaromega)  //Vs
                                              + bhbaromega/4*matrix.Vb()    //Vb  //Vxx termは入れてない。

                                              //Vsb
                                              + kxxz*Vbcoeff*matrix.Vsb(kzz, az, shbaromega);
                                            
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    return result;
}

//Dinftyd
Eigen::MatrixXd H_Dinftyd (int n0, int npls, int nmns, int j, int m,    //matrix size
                     double B, double B_large, double C_large, double mu, double Re,   //molecular parameter
                     vector<double> PotParam
                     ) 
{    
    //constant
    double hbar = 1.054571817*pow(10, -34);
    double c = 2.99792458*pow(10, 8);

    double Ix = hbar*hbar/(2*B_large)*5.03412*pow(10, 22);
    double Iz = hbar*hbar/(2*C_large)*5.03412*pow(10, 22); //長さはm単位

    double mub = mu;

    double Re2Ix = (Re*pow(10, -10))*(Re*pow(10, -10))/Ix;
    double omegas = sqrt(2*PotParam[0]*PotParam[1]*PotParam[1]*1.98645*pow(10, -23)*pow(10, 20)/mu);   //単位はs-1
    double omegab = sqrt(2*PotParam[2]*1.98645*pow(10, -23)*pow(10, 20)/mub);   //単位はs-1
    double shbaromega = 1/(2*M_PI)*omegas/c/100;    //単位変換で1/hcをかけ、hbarをかけるため、2\piが必要。
    double bhbaromega = 1/(2*M_PI)*omegab/c/100;
    double ReIxsqrt2mubomegas = Re*pow(10, -10)/Ix*sqrt(2*mub*hbar/omegas);
    //double ReIxsqrt2muomegas = Re*pow(10, -10)/Ix*sqrt(2*mu*hbar/omegas);
    double hbar2Ix = hbar*hbar/Ix*5.03412*pow(10, 22); //1 J = 5.03412 \times 10^22 cm-1
    double hbar2Iz = hbar*hbar/Iz*5.03412*pow(10, 22);
    //double Resqrt2mubhbaromegas = hbar2Ix*Re*pow(10, -10)*sqrt(2*mu*omegas/hbar);
    //double Resqrt2muhbaromegas = hbar2Ix*Re*pow(10, -10)*sqrt(2*mu*omegas/hbar);
    double Vbcoeff = hbar/(2*mub*omegab)*pow(10, 20);
    double Vscoeff = hbar/(2*mu*omegas)*pow(10, 20);

    double kzz = PotParam[0];
    double az = PotParam[1];
    double kxx = PotParam[2];
    double kxxz = PotParam[3];
    double V001 = PotParam[4];
    double V002 = PotParam[5];
    double V202 = PotParam[6];
    double V003 = PotParam[7];
    double V203 = PotParam[8];
    double V303 = PotParam[9];
    double V004 = PotParam[10];
    double VR001 = PotParam[11];
    double VR002 = PotParam[12];
    double VR202 = PotParam[13];
    double VR003 = PotParam[14];
    double VR203 = PotParam[15];
    double VR303 = PotParam[16];
    double VR004 = PotParam[17];
    double VRR001 = PotParam[18];
    double VRR002 = PotParam[19];
    double VRR202 = PotParam[20];
    double VRR003 = PotParam[21];
    double VRR203 = PotParam[22];
    double VRR303 = PotParam[23];
    double VRR004 = PotParam[24];
    double Vrho001 = PotParam[25];
    double Vrho002 = PotParam[26];
    double Vrho202 = PotParam[27];
    double Vrho003 = PotParam[28];
    double Vrho203 = PotParam[29];
    double Vrho303 = PotParam[30];
    double Vrho004 = PotParam[31];
    double Vam011_0 = PotParam[32];
    double Vam012_0 = PotParam[33];
    double Vam022_0 = PotParam[34];
    double Vam212_0 = PotParam[35];
    double Vam222_0 = PotParam[36];
    double Vam013_0 = PotParam[37];
    double Vam023_0 = PotParam[38];
    double Vam011_6 = PotParam[39];
    double Vam012_6 = PotParam[40];
    double Vam022_6 = PotParam[41];
    double Vam212_6 = PotParam[42];
    double Vam222_6 = PotParam[43];
    double Vam013_6 = PotParam[44];
    double Vam023_6 = PotParam[45];
    double Vam011_8 = PotParam[46];
    double Vam012_8 = PotParam[47];
    double Vam022_8 = PotParam[48];
    double Vam212_8 = PotParam[49];
    double Vam222_8 = PotParam[50];
    double Vam013_8 = PotParam[51];
    double Vam023_8 = PotParam[52];
    double Vam011_10 = PotParam[53];
    double Vam012_10 = PotParam[54];
    double Vam022_10 = PotParam[55];
    double Vam212_10 = PotParam[56];
    double Vam222_10 = PotParam[57];
    double Vam013_10 = PotParam[58];
    double Vam023_10 = PotParam[59];

    MatrixParameter dim(n0, npls, nmns, j, m, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
    //vector<vector<double>> result(dim.matrix_size(), vector<double>(dim.matrix_size()));
    Eigen::MatrixXd result = Eigen::MatrixXd::Ones(dim.matrix_size(), dim.matrix_size());
    vector<int> drow(1, 0);
    vector<int> ddrow(1, 0);
    int dddrow= 0;
    for (int mBrow = - j; mBrow <= j; mBrow++) {                                                    // assign row mB
        for (int vrow = abs(m - mBrow); vrow <= (npls + nmns - abs(m - mBrow)); vrow += 2) {  //assign row v
            int jrdim = 0;
            int jdrow;
            for (int num = 0; num<= j; num++) {
                jdrow = (2 * abs(num) + 1);
                jrdim += jdrow;
            }
            int mrminus = 0;
            int mmmrow;
            for (int mm = 0; mm <= abs(mBrow); mm++) {
                if (mm == 0) {
                    mmmrow = 0;
                }
                else {
                    mmmrow = (2 * (abs(mm) - 1) + 1);
                }
                mrminus += mmmrow;
            }
            int d = (npls + 1 - abs(m - mBrow))*(jrdim - mrminus);
            drow.push_back(d);
            if (d != drow[drow.size() - 2]) {
                ddrow.push_back(d);
                dddrow += ddrow[ddrow.size() - 2];
            }

            vector<int> dcolumn(1, 0);
            vector<int> ddcolumn(1, 0);
            int dddcolumn = 0;
            for (int mBcolumn = - j; mBcolumn <= j; mBcolumn++) {                                       // assign column mB
                for (int vcolumn = abs(m - mBcolumn); vcolumn <= (npls + nmns - abs(m - mBcolumn)); vcolumn += 2) {   // assign column v
                    int jcdim = 0;
                    int jdcolumn;
                    for (int num = 0; num<= j; num++) {
                        jdcolumn = (2 * abs(num) + 1);
                        jcdim += jdcolumn;
                        }
                    int mcminus = 0;
                    int mmmcolumn;
                    for (int mm = 0; mm <= abs(mBcolumn); mm++) {
                        if (mm == 0) {
                            mmmcolumn = 0;
                        }
                        else {
                            mmmcolumn = (2 * (abs(mm) - 1) + 1);
                        }
                        mcminus += mmmcolumn;
                    }
                    int d = (npls + 1 - abs(m - mBcolumn))*(jcdim - mcminus);
                    dcolumn.push_back(d);
                    if (d != dcolumn[dcolumn.size() - 2]) { //dcolumn.size() - 2 > 0の条件を追加したらエラーが消えるかもしれない．
                        ddcolumn.push_back(d);
                        dddcolumn += ddcolumn[ddcolumn.size() - 2];
                    }

                    #pragma omp parallel for num_threads(12)
                    for (int jrow = abs(mBrow); jrow <= j; jrow++) {                                            // assign row j
                        for (int krow = - jrow; krow <= jrow; krow++) {                                         // assign row k
                            for (int n0row = 0; n0row <= n0; n0row++) {                                         // assign row n0
                                for (int jcolumn = abs(mBcolumn); jcolumn <= j; jcolumn++) {                                                // assign column j      
                                    for (int kcolumn = - jcolumn; kcolumn <= jcolumn; kcolumn++) {                                          // assign column k
                                        for (int n0column = 0; n0column <= n0; n0column++) {                                                // assign column n0
                                            // matrix element
                                            MatrixElement matrix(n0, npls, nmns, j, m, jrow, mBrow, krow, n0row, vrow, jcolumn, mBcolumn, kcolumn, n0column, vcolumn);
                                            result(dddrow + matrix.row(), dddcolumn + matrix.column())
                                             = 

                                              - bhbaromega/4*(
                                                + (1 + Re2Ix*mu)*matrix.Tb()    //Tb
                                                + ReIxsqrt2mubomegas*sqrt(mub/mu)*matrix.Tb_1()
                                                + hbar2Ix/2*1/shbaromega*mub/mu*matrix.Tb_2()
                                                )

                                              - shbaromega/4*matrix.Ts()    //Ts
                                                - hbar2Ix/4*omegas/omegab*mu/mub*matrix.Ts_1()
                                            
                                              
                                              + hbar2Iz*matrix.T_3_1()
                                              - hbar2Ix/2*matrix.T_4_1()
                                              //+ Resqrt2mubhbaromegas/2*matrix.T_4_2()
                                              + hbar2Ix/2*matrix.T_5_1()
                                              + shbaromega*ReIxsqrt2mubomegas/2*matrix.T_5_2()
                                              + 1/sqrt(2)*hbar2Ix/2*sqrt(omegab/omegas)*sqrt(mub/mu)*matrix.T_6_1()
                                              + 1/sqrt(2)*hbar2Ix/2*sqrt(omegas/omegab)*sqrt(mu/mub)*matrix.T_6_2()
                                              + hbar2Iz*matrix.T_7_1()
                                              

                                              + B*matrix.Tr()   //Tr
                                              + hbar2Ix*matrix.Tr() + (hbar2Iz - hbar2Ix)*matrix.Tr_1()
                                              
                                              + kzz*matrix.Vs(kzz, az, shbaromega)  //Vs
                                              + bhbaromega/4*matrix.Vb()    //Vb  //Vxx termは入れてない。
                                            
                                              //Vr
                                              + V002*( matrix.Vr(2, 0) ) 
                                              + V004*( matrix.Vr(4, 0) )
                                            
                                              //Vsb
                                              + kxxz*Vbcoeff*matrix.Vsb(kzz, az, shbaromega)
                                            
                                              //Vsr
                                              + VR002*sqrt( Vscoeff )*( matrix.Vsr(2, 0) )
                                              + VR004*sqrt( Vscoeff )*( matrix.Vsr(4, 0) )
                                              //Vssr
                                              + VRR002*( Vscoeff )*( matrix.Vssr(2, 0) )
                                              + VRR004*( Vscoeff )*( matrix.Vssr(4, 0) )
                                              //Vbr
                                              + Vrho002*Vbcoeff*( matrix.Vbr(2, 0) )
                                              + Vrho004*Vbcoeff*( matrix.Vbr(4, 0) )
                                              
                                              //Vam
                                              + Vam012_0*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( (matrix.Vam(2, 0, 1) - matrix.Vam(2, 0, -1)) )
                                              //VamR
                                              + Vam012_6*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( (matrix.VamR(6, Re, 2, 0, 1, kzz, az, shbaromega) - matrix.VamR(6, Re, 2, 0, -1, kzz, az, shbaromega)) )
                                              + Vam012_8*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( (matrix.VamR(8, Re, 2, 0, 1, kzz, az, shbaromega) - matrix.VamR(8, Re, 2, 0, -1, kzz, az, shbaromega)) )
                                              + Vam012_10*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( (matrix.VamR(10, Re, 2, 0, 1, kzz, az, shbaromega) - matrix.VamR(10, Re, 2, 0, -1, kzz, az, shbaromega)) );
                                            
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    //PRINT_MAT(result);
    return result;
}

//Cinftyv
Eigen::MatrixXd H_Cinftyv (int n0, int npls, int nmns, int j, int m,    //matrix size
                     double B, double B_large, double C_large, double mu, double Re,   //molecular parameter
                     vector<double> PotParam
                     ) 
{    
    //constant
    double hbar = 1.054571817*pow(10, -34);
    double c = 2.99792458*pow(10, 8);

    double Ix = hbar*hbar/(2*B_large)*5.03412*pow(10, 22);
    double Iz = hbar*hbar/(2*C_large)*5.03412*pow(10, 22); //長さはm単位

    double mub = mu;

    double Re2Ix = (Re*pow(10, -10))*(Re*pow(10, -10))/Ix;
    double omegas = sqrt(2*PotParam[0]*PotParam[1]*PotParam[1]*1.98645*pow(10, -23)*pow(10, 20)/mu);   //単位はs-1
    double omegab = sqrt(2*PotParam[2]*1.98645*pow(10, -23)*pow(10, 20)/mub);   //単位はs-1
    double shbaromega = 1/(2*M_PI)*omegas/c/100;    //単位変換で1/hcをかけ、hbarをかけるため、2\piが必要。
    double bhbaromega = 1/(2*M_PI)*omegab/c/100;
    double ReIxsqrt2mubomegas = Re*pow(10, -10)/Ix*sqrt(2*mub*hbar/omegas);
    //double ReIxsqrt2muomegas = Re*pow(10, -10)/Ix*sqrt(2*mu*hbar/omegas);
    double hbar2Ix = hbar*hbar/Ix*5.03412*pow(10, 22); //1 J = 5.03412 \times 10^22 cm-1
    double hbar2Iz = hbar*hbar/Iz*5.03412*pow(10, 22);
    //double Resqrt2mubhbaromegas = hbar2Ix*Re*pow(10, -10)*sqrt(2*mu*omegas/hbar);
    //double Resqrt2muhbaromegas = hbar2Ix*Re*pow(10, -10)*sqrt(2*mu*omegas/hbar);
    double Vbcoeff = hbar/(2*mub*omegab)*pow(10, 20);
    double Vscoeff = hbar/(2*mu*omegas)*pow(10, 20);

    double kzz = PotParam[0];
    double az = PotParam[1];
    double kxx = PotParam[2];
    double kxxz = PotParam[3];
    double V001 = PotParam[4];
    double V002 = PotParam[5];
    double V202 = PotParam[6];
    double V003 = PotParam[7];
    double V203 = PotParam[8];
    double V303 = PotParam[9];
    double V004 = PotParam[10];
    double VR001 = PotParam[11];
    double VR002 = PotParam[12];
    double VR202 = PotParam[13];
    double VR003 = PotParam[14];
    double VR203 = PotParam[15];
    double VR303 = PotParam[16];
    double VR004 = PotParam[17];
    double VRR001 = PotParam[18];
    double VRR002 = PotParam[19];
    double VRR202 = PotParam[20];
    double VRR003 = PotParam[21];
    double VRR203 = PotParam[22];
    double VRR303 = PotParam[23];
    double VRR004 = PotParam[24];
    double Vrho001 = PotParam[25];
    double Vrho002 = PotParam[26];
    double Vrho202 = PotParam[27];
    double Vrho003 = PotParam[28];
    double Vrho203 = PotParam[29];
    double Vrho303 = PotParam[30];
    double Vrho004 = PotParam[31];
    double Vam011_0 = PotParam[32];
    double Vam012_0 = PotParam[33];
    double Vam022_0 = PotParam[34];
    double Vam212_0 = PotParam[35];
    double Vam222_0 = PotParam[36];
    double Vam013_0 = PotParam[37];
    double Vam023_0 = PotParam[38];
    double Vam011_6 = PotParam[39];
    double Vam012_6 = PotParam[40];
    double Vam022_6 = PotParam[41];
    double Vam212_6 = PotParam[42];
    double Vam222_6 = PotParam[43];
    double Vam013_6 = PotParam[44];
    double Vam023_6 = PotParam[45];
    double Vam011_8 = PotParam[46];
    double Vam012_8 = PotParam[47];
    double Vam022_8 = PotParam[48];
    double Vam212_8 = PotParam[49];
    double Vam222_8 = PotParam[50];
    double Vam013_8 = PotParam[51];
    double Vam023_8 = PotParam[52];
    double Vam011_10 = PotParam[53];
    double Vam012_10 = PotParam[54];
    double Vam022_10 = PotParam[55];
    double Vam212_10 = PotParam[56];
    double Vam222_10 = PotParam[57];
    double Vam013_10 = PotParam[58];
    double Vam023_10 = PotParam[59];

    MatrixParameter dim(n0, npls, nmns, j, m, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
    //vector<vector<double>> result(dim.matrix_size(), vector<double>(dim.matrix_size()));
    Eigen::MatrixXd result = Eigen::MatrixXd::Ones(dim.matrix_size(), dim.matrix_size());
    vector<int> drow(1, 0);
    vector<int> ddrow(1, 0);
    int dddrow= 0;
    for (int mBrow = - j; mBrow <= j; mBrow++) {                                                    // assign row mB
        for (int vrow = abs(m - mBrow); vrow <= (npls + nmns - abs(m - mBrow)); vrow += 2) {  //assign row v
            int jrdim = 0;
            int jdrow;
            for (int num = 0; num<= j; num++) {
                jdrow = (2 * abs(num) + 1);
                jrdim += jdrow;
            }
            int mrminus = 0;
            int mmmrow;
            for (int mm = 0; mm <= abs(mBrow); mm++) {
                if (mm == 0) {
                    mmmrow = 0;
                }
                else {
                    mmmrow = (2 * (abs(mm) - 1) + 1);
                }
                mrminus += mmmrow;
            }
            int d = (npls + 1 - abs(m - mBrow))*(jrdim - mrminus);
            drow.push_back(d);
            if (d != drow[drow.size() - 2]) {
                ddrow.push_back(d);
                dddrow += ddrow[ddrow.size() - 2];
            }

            vector<int> dcolumn(1, 0);
            vector<int> ddcolumn(1, 0);
            int dddcolumn = 0;
            for (int mBcolumn = - j; mBcolumn <= j; mBcolumn++) {                                       // assign column mB
                for (int vcolumn = abs(m - mBcolumn); vcolumn <= (npls + nmns - abs(m - mBcolumn)); vcolumn += 2) {   // assign column v
                    int jcdim = 0;
                    int jdcolumn;
                    for (int num = 0; num<= j; num++) {
                        jdcolumn = (2 * abs(num) + 1);
                        jcdim += jdcolumn;
                        }
                    int mcminus = 0;
                    int mmmcolumn;
                    for (int mm = 0; mm <= abs(mBcolumn); mm++) {
                        if (mm == 0) {
                            mmmcolumn = 0;
                        }
                        else {
                            mmmcolumn = (2 * (abs(mm) - 1) + 1);
                        }
                        mcminus += mmmcolumn;
                    }
                    int d = (npls + 1 - abs(m - mBcolumn))*(jcdim - mcminus);
                    dcolumn.push_back(d);
                    if (d != dcolumn[dcolumn.size() - 2]) { //dcolumn.size() - 2 > 0の条件を追加したらエラーが消えるかもしれない．
                        ddcolumn.push_back(d);
                        dddcolumn += ddcolumn[ddcolumn.size() - 2];
                    }

                    #pragma omp parallel for num_threads(12)
                    for (int jrow = abs(mBrow); jrow <= j; jrow++) {                                            // assign row j
                        for (int krow = - jrow; krow <= jrow; krow++) {                                         // assign row k
                            for (int n0row = 0; n0row <= n0; n0row++) {                                         // assign row n0
                                for (int jcolumn = abs(mBcolumn); jcolumn <= j; jcolumn++) {                                                // assign column j      
                                    for (int kcolumn = - jcolumn; kcolumn <= jcolumn; kcolumn++) {                                          // assign column k
                                        for (int n0column = 0; n0column <= n0; n0column++) {                                                // assign column n0
                                            // matrix element
                                            MatrixElement matrix(n0, npls, nmns, j, m, jrow, mBrow, krow, n0row, vrow, jcolumn, mBcolumn, kcolumn, n0column, vcolumn);
                                            result(dddrow + matrix.row(), dddcolumn + matrix.column())
                                             = 

                                              - bhbaromega/4*(
                                                + (1 + Re2Ix*mu)*matrix.Tb()    //Tb
                                                + ReIxsqrt2mubomegas*sqrt(mub/mu)*matrix.Tb_1()
                                                + hbar2Ix/2*1/shbaromega*mub/mu*matrix.Tb_2()
                                                )

                                              - shbaromega/4*matrix.Ts()    //Ts
                                                - hbar2Ix/4*omegas/omegab*mu/mub*matrix.Ts_1()
                                            
                                              
                                              + hbar2Iz*matrix.T_3_1()
                                              - hbar2Ix/2*matrix.T_4_1()
                                              //+ Resqrt2mubhbaromegas/2*matrix.T_4_2()
                                              + hbar2Ix/2*matrix.T_5_1()
                                              + shbaromega*ReIxsqrt2mubomegas/2*matrix.T_5_2()
                                              + 1/sqrt(2)*hbar2Ix/2*sqrt(omegab/omegas)*sqrt(mub/mu)*matrix.T_6_1()
                                              + 1/sqrt(2)*hbar2Ix/2*sqrt(omegas/omegab)*sqrt(mu/mub)*matrix.T_6_2()
                                              + hbar2Iz*matrix.T_7_1()
                                              

                                              + B*matrix.Tr()   //Tr
                                              + hbar2Ix*matrix.Tr() + (hbar2Iz - hbar2Ix)*matrix.Tr_1()
                                              
                                              + kzz*matrix.Vs(kzz, az, shbaromega)  //Vs
                                              + bhbaromega/4*matrix.Vb()    //Vb  //Vxx termは入れてない。
                                            
                                              //Vr
                                              + V001*( matrix.Vr(1, 0) )
                                              + V002*( matrix.Vr(2, 0) )
                                              + V003*( matrix.Vr(3, 0) ) 
                                              + V004*( matrix.Vr(4, 0) )
                                            
                                              //Vsb
                                              + kxxz*Vbcoeff*matrix.Vsb(kzz, az, shbaromega)
                                            
                                              //Vsr
                                              + VR001*sqrt( Vscoeff )*( matrix.Vsr(1, 0) )
                                              + VR002*sqrt( Vscoeff )*( matrix.Vsr(2, 0) )
                                              + VR003*sqrt( Vscoeff )*( matrix.Vsr(2, 0) )
                                              + VR004*sqrt( Vscoeff )*( matrix.Vsr(4, 0) )
                                              //Vssr
                                              + VRR001*( Vscoeff )*( matrix.Vssr(1, 0) )
                                              + VRR002*( Vscoeff )*( matrix.Vssr(2, 0) )
                                              + VRR003*( Vscoeff )*( matrix.Vssr(3, 0) )
                                              + VRR004*( Vscoeff )*( matrix.Vssr(4, 0) )
                                              //Vbr
                                              + Vrho001*Vbcoeff*( matrix.Vbr(1, 0) )
                                              + Vrho002*Vbcoeff*( matrix.Vbr(2, 0) )
                                              + Vrho003*Vbcoeff*( matrix.Vbr(3, 0) )
                                              + Vrho004*Vbcoeff*( matrix.Vbr(4, 0) )
                                              
                                              //Vam
                                              + Vam011_0*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( (matrix.Vam(1, 0, 1) - matrix.Vam(1, 0, -1)) )
                                              + Vam012_0*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( (matrix.Vam(2, 0, 1) - matrix.Vam(2, 0, -1)) )
                                              + Vam013_0*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( (matrix.Vam(3, 0, 1) - matrix.Vam(3, 0, -1)) )
                                              //VamR
                                              + Vam011_6*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( (matrix.VamR(6, Re, 1, 0, 1, kzz, az, shbaromega) - matrix.VamR(6, Re, 1, 0, -1, kzz, az, shbaromega)) )
                                              + Vam012_6*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( (matrix.VamR(6, Re, 2, 0, 1, kzz, az, shbaromega) - matrix.VamR(6, Re, 2, 0, -1, kzz, az, shbaromega)) )
                                              + Vam013_6*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( (matrix.VamR(6, Re, 3, 0, 1, kzz, az, shbaromega) - matrix.VamR(6, Re, 3, 0, -1, kzz, az, shbaromega)) )

                                              + Vam011_8*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( (matrix.VamR(8, Re, 1, 0, 1, kzz, az, shbaromega) - matrix.VamR(8, Re, 1, 0, -1, kzz, az, shbaromega)) )
                                              + Vam012_8*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( (matrix.VamR(8, Re, 2, 0, 1, kzz, az, shbaromega) - matrix.VamR(8, Re, 2, 0, -1, kzz, az, shbaromega)) )
                                              + Vam013_8*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( (matrix.VamR(8, Re, 3, 0, 1, kzz, az, shbaromega) - matrix.VamR(8, Re, 3, 0, -1, kzz, az, shbaromega)) )

                                              + Vam011_10*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( (matrix.VamR(10, Re, 1, 0, 1, kzz, az, shbaromega) - matrix.VamR(10, Re, 1, 0, -1, kzz, az, shbaromega)) )
                                              + Vam012_10*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( (matrix.VamR(10, Re, 2, 0, 1, kzz, az, shbaromega) - matrix.VamR(10, Re, 2, 0, -1, kzz, az, shbaromega)) )
                                              + Vam013_10*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( (matrix.VamR(10, Re, 3, 0, 1, kzz, az, shbaromega) - matrix.VamR(10, Re, 3, 0, -1, kzz, az, shbaromega)) );
                                            
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    //PRINT_MAT(result);
    return result;
}


//C2v kinetic termの修正が必要  //sqrt(3/(8*M_PI))はY_1^1の規格化定数に由来しているのでm_cpl=1のときは全て同じで修正しなくていい．  //対称性 J. Chern. Phys., Vol. 98, No.8, 15 April 1993
Eigen::MatrixXd H_C2v (int n0, int npls, int nmns, int j, int m,    //matrix size
                     double A, double B, double C, double B_large, double C_large, double mu, double Re,   //molecular parameter
                     vector<double> PotParam
                     ) 
{    
    //constant
    double hbar = 1.054571817*pow(10, -34);
    double c = 2.99792458*pow(10, 8);

    double Ix = hbar*hbar/(2*B_large)*5.03412*pow(10, 22);
    double Iz = hbar*hbar/(2*C_large)*5.03412*pow(10, 22); //長さはm単位

    double mub = mu;

    double Re2Ix = (Re*pow(10, -10))*(Re*pow(10, -10))/Ix;
    double omegas = sqrt(2*PotParam[0]*PotParam[1]*PotParam[1]*1.98645*pow(10, -23)*pow(10, 20)/mu);   //単位はs-1
    double omegab = sqrt(2*PotParam[2]*1.98645*pow(10, -23)*pow(10, 20)/mub);   //単位はs-1
    double shbaromega = 1/(2*M_PI)*omegas/c/100;    //単位変換で1/hcをかけ、hbarをかけるため、2\piが必要。
    double bhbaromega = 1/(2*M_PI)*omegab/c/100;
    double ReIxsqrt2mubomegas = Re*pow(10, -10)/Ix*sqrt(2*mub*hbar/omegas);
    //double ReIxsqrt2muomegas = Re*pow(10, -10)/Ix*sqrt(2*mu*hbar/omegas);
    double hbar2Ix = hbar*hbar/Ix*5.03412*pow(10, 22); //1 J = 5.03412 \times 10^22 cm-1
    double hbar2Iz = hbar*hbar/Iz*5.03412*pow(10, 22);
    //double Resqrt2mubhbaromegas = hbar2Ix*Re*pow(10, -10)*sqrt(2*mu*omegas/hbar);
    //double Resqrt2muhbaromegas = hbar2Ix*Re*pow(10, -10)*sqrt(2*mu*omegas/hbar);
    double Vbcoeff = hbar/(2*mub*omegab)*pow(10, 20);
    double Vscoeff = hbar/(2*mu*omegas)*pow(10, 20);

    double kzz = PotParam[0];
    double az = PotParam[1];
    double kxx = PotParam[2];
    double kxxz = PotParam[3];
    double V001 = PotParam[4];
    double V002 = PotParam[5];
    double V202 = PotParam[6];
    double V003 = PotParam[7];
    double V203 = PotParam[8];
    double V303 = PotParam[9];
    double V004 = PotParam[10];
    double VR001 = PotParam[11];
    double VR002 = PotParam[12];
    double VR202 = PotParam[13];
    double VR003 = PotParam[14];
    double VR203 = PotParam[15];
    double VR303 = PotParam[16];
    double VR004 = PotParam[17];
    double VRR001 = PotParam[18];
    double VRR002 = PotParam[19];
    double VRR202 = PotParam[20];
    double VRR003 = PotParam[21];
    double VRR203 = PotParam[22];
    double VRR303 = PotParam[23];
    double VRR004 = PotParam[24];
    double Vrho001 = PotParam[25];
    double Vrho002 = PotParam[26];
    double Vrho202 = PotParam[27];
    double Vrho003 = PotParam[28];
    double Vrho203 = PotParam[29];
    double Vrho303 = PotParam[30];
    double Vrho004 = PotParam[31];
    double Vam011_0 = PotParam[32];
    double Vam012_0 = PotParam[33];
    double Vam022_0 = PotParam[34];
    double Vam212_0 = PotParam[35];
    double Vam222_0 = PotParam[36];
    double Vam013_0 = PotParam[37];
    double Vam023_0 = PotParam[38];
    double Vam011_6 = PotParam[39];
    double Vam012_6 = PotParam[40];
    double Vam022_6 = PotParam[41];
    double Vam212_6 = PotParam[42];
    double Vam222_6 = PotParam[43];
    double Vam013_6 = PotParam[44];
    double Vam023_6 = PotParam[45];
    double Vam011_8 = PotParam[46];
    double Vam012_8 = PotParam[47];
    double Vam022_8 = PotParam[48];
    double Vam212_8 = PotParam[49];
    double Vam222_8 = PotParam[50];
    double Vam013_8 = PotParam[51];
    double Vam023_8 = PotParam[52];
    double Vam011_10 = PotParam[53];
    double Vam012_10 = PotParam[54];
    double Vam022_10 = PotParam[55];
    double Vam212_10 = PotParam[56];
    double Vam222_10 = PotParam[57];
    double Vam013_10 = PotParam[58];
    double Vam023_10 = PotParam[59];

    MatrixParameter dim(n0, npls, nmns, j, m, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
    //vector<vector<double>> result(dim.matrix_size(), vector<double>(dim.matrix_size()));
    Eigen::MatrixXd result = Eigen::MatrixXd::Ones(dim.matrix_size(), dim.matrix_size());
    vector<int> drow(1, 0);
    vector<int> ddrow(1, 0);
    int dddrow= 0;
    for (int mBrow = - j; mBrow <= j; mBrow++) {                                                    // assign row mB
        for (int vrow = abs(m - mBrow); vrow <= (npls + nmns - abs(m - mBrow)); vrow += 2) {  //assign row v
            int jrdim = 0;
            int jdrow;
            for (int num = 0; num<= j; num++) {
                jdrow = (2 * abs(num) + 1);
                jrdim += jdrow;
            }
            int mrminus = 0;
            int mmmrow;
            for (int mm = 0; mm <= abs(mBrow); mm++) {
                if (mm == 0) {
                    mmmrow = 0;
                }
                else {
                    mmmrow = (2 * (abs(mm) - 1) + 1);
                }
                mrminus += mmmrow;
            }
            int d = (npls + 1 - abs(m - mBrow))*(jrdim - mrminus);
            drow.push_back(d);
            if (d != drow[drow.size() - 2]) {
                ddrow.push_back(d);
                dddrow += ddrow[ddrow.size() - 2];
            }

            vector<int> dcolumn(1, 0);
            vector<int> ddcolumn(1, 0);
            int dddcolumn = 0;
            for (int mBcolumn = - j; mBcolumn <= j; mBcolumn++) {                                       // assign column mB
                for (int vcolumn = abs(m - mBcolumn); vcolumn <= (npls + nmns - abs(m - mBcolumn)); vcolumn += 2) {   // assign column v
                    int jcdim = 0;
                    int jdcolumn;
                    for (int num = 0; num<= j; num++) {
                        jdcolumn = (2 * abs(num) + 1);
                        jcdim += jdcolumn;
                        }
                    int mcminus = 0;
                    int mmmcolumn;
                    for (int mm = 0; mm <= abs(mBcolumn); mm++) {
                        if (mm == 0) {
                            mmmcolumn = 0;
                        }
                        else {
                            mmmcolumn = (2 * (abs(mm) - 1) + 1);
                        }
                        mcminus += mmmcolumn;
                    }
                    int d = (npls + 1 - abs(m - mBcolumn))*(jcdim - mcminus);
                    dcolumn.push_back(d);
                    if (d != dcolumn[dcolumn.size() - 2]) { //dcolumn.size() - 2 > 0の条件を追加したらエラーが消えるかもしれない．
                        ddcolumn.push_back(d);
                        dddcolumn += ddcolumn[ddcolumn.size() - 2];
                    }

                    #pragma omp parallel for num_threads(12)
                    for (int jrow = abs(mBrow); jrow <= j; jrow++) {                                            // assign row j
                        for (int krow = - jrow; krow <= jrow; krow++) {                                         // assign row k
                            for (int n0row = 0; n0row <= n0; n0row++) {                                         // assign row n0
                                for (int jcolumn = abs(mBcolumn); jcolumn <= j; jcolumn++) {                                                // assign column j      
                                    for (int kcolumn = - jcolumn; kcolumn <= jcolumn; kcolumn++) {                                          // assign column k
                                        for (int n0column = 0; n0column <= n0; n0column++) {                                                // assign column n0
                                            // matrix element
                                            MatrixElement matrix(n0, npls, nmns, j, m, jrow, mBrow, krow, n0row, vrow, jcolumn, mBcolumn, kcolumn, n0column, vcolumn);
                                            result(dddrow + matrix.row(), dddcolumn + matrix.column())
                                             = 

                                              - bhbaromega/4*(
                                                + (1 + Re2Ix*mu)*matrix.Tb()    //Tb
                                                + ReIxsqrt2mubomegas*sqrt(mub/mu)*matrix.Tb_1()
                                                + hbar2Ix/2*1/shbaromega*mub/mu*matrix.Tb_2()
                                                )

                                              - shbaromega/4*matrix.Ts()    //Ts
                                                - hbar2Ix/4*omegas/omegab*mu/mub*matrix.Ts_1()
                                            
                                              
                                              + hbar2Iz*matrix.T_3_1()
                                              - hbar2Ix/2*matrix.T_4_1()
                                              //+ Resqrt2mubhbaromegas/2*matrix.T_4_2()
                                              + hbar2Ix/2*matrix.T_5_1()
                                              + shbaromega*ReIxsqrt2mubomegas/2*matrix.T_5_2()
                                              + 1/sqrt(2)*hbar2Ix/2*sqrt(omegab/omegas)*sqrt(mub/mu)*matrix.T_6_1()
                                              + 1/sqrt(2)*hbar2Ix/2*sqrt(omegas/omegab)*sqrt(mu/mub)*matrix.T_6_2()
                                              + hbar2Iz*matrix.T_7_1()
                                              
                                              //Bernas p.203
                                              + (A + B)/2*matrix.Tr_asymtop_1()   //Tr
                                              + (C - (A + B)/2)*matrix.Tr_asymtop_2()
                                              + (A - B)/4*matrix.Tr_asymtop_3()
                                              + hbar2Ix*matrix.Tr() + (hbar2Iz - hbar2Ix)*matrix.Tr_1()
                                              
                                              + kzz*matrix.Vs(kzz, az, shbaromega)  //Vs
                                              + bhbaromega/4*matrix.Vb()    //Vb  //Vxx termは入れてない。
                                            
                                              //Vr
                                              + V001*( 1/2*matrix.Vr(1, 0)*2 )
                                              + V002*( 1/2*matrix.Vr(2, 0)*2 )
                                              + V202*( 1/1*(matrix.Vr(2, +2) + pow(-1, +2)*matrix.Vr(2, -2)) )
                                              + V003*( 1/2*matrix.Vr(3, 0)*2 ) 
                                              + V203*( 1/1*(matrix.Vr(3, +2) + pow(-1, +2)*matrix.Vr(3, -2)) )
                                              
                                            
                                              //Vsb
                                              + kxxz*Vbcoeff*matrix.Vsb(kzz, az, shbaromega)
                                            
                                              //Vsr
                                              + VR001*sqrt( Vscoeff )*( 1/2*matrix.Vsr(1, 0)*2 )
                                              + VR002*sqrt( Vscoeff )*( 1/2*matrix.Vsr(2, 0)*2 )
                                              + VR202*sqrt( Vscoeff )*( 1/1*(matrix.Vsr(2, +2) + pow(-1, +2)*matrix.Vsr(2, -2)) )
                                              + VR003*sqrt( Vscoeff )*( 1/2*matrix.Vsr(3, 0)*2 ) 
                                              + VR203*sqrt( Vscoeff )*( 1/1*(matrix.Vsr(3, +2) + pow(-1, +2)*matrix.Vsr(3, -2)) )
                                              

                                              //Vssr
                                              + VRR001*( Vscoeff )*( 1/2*matrix.Vssr(1, 0)*2 )
                                              + VRR002*( Vscoeff )*( 1/2*matrix.Vssr(2, 0)*2 )
                                              + VRR202*( Vscoeff )*( 1/1*(matrix.Vssr(2, +2) + pow(-1, +2)*matrix.Vssr(2, -2)) )
                                              + VRR003*( Vscoeff )*( 1/2*matrix.Vssr(3, 0)*2 ) 
                                              + VRR203*( Vscoeff )*( 1/1*(matrix.Vssr(3, +2) + pow(-1, +2)*matrix.Vssr(3, -2)) )

                                              //Vbr
                                              + Vrho001*Vbcoeff*( 1/2*matrix.Vbr(1, 0)*2 )
                                              + Vrho002*Vbcoeff*( 1/2*matrix.Vbr(2, 0)*2 )
                                              + Vrho202*Vbcoeff*( 1/1*(matrix.Vbr(2, +2) + pow(-1, +2)*matrix.Vbr(2, -2)) )
                                              + Vrho003*Vbcoeff*( 1/2*matrix.Vbr(3, 0)*2 )
                                              + Vrho203*Vbcoeff*( 1/1*(matrix.Vbr(3, +2) + pow(-1, +2)*matrix.Vbr(3, -2)) )
                                              
                                              //Vam
                                              + Vam011_0*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( 1/2*(matrix.Vam(1, 0, 1) - matrix.Vam(1, 0, -1))*2 )
                                              + Vam012_0*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( 1/2*(matrix.Vam(2, 0, 1) - matrix.Vam(2, 0, -1))*2 )
                                              + Vam212_0*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( 1/1*((matrix.Vam(2, 2, 1) - matrix.Vam(2, 2, -1)) + pow(-1, +2)*(matrix.Vam(2, -2, 1) - matrix.Vam(2, -2, -1))) )
                                              + Vam013_0*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( 1/2*(matrix.Vam(3, 0, 1) - matrix.Vam(3, 0, -1))*2 )
                                              //VamR
                                              + Vam011_6*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( 1/2*(matrix.VamR(6, Re, 1, 0, 1, kzz, az, shbaromega) - matrix.VamR(6, Re, 1, 0, -1, kzz, az, shbaromega))*2 )
                                              + Vam012_6*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( 1/2*(matrix.VamR(6, Re, 2, 0, 1, kzz, az, shbaromega) - matrix.VamR(6, Re, 2, 0, -1, kzz, az, shbaromega))*2 )
                                              + Vam212_6*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( 1/1*((matrix.VamR(6, Re, 2, 2, 1, kzz, az, shbaromega) - matrix.VamR(6, Re, 2, -2, -1, kzz, az, shbaromega)) + pow(-1, +2)*(matrix.VamR(6, Re, 2, -2, 1, kzz, az, shbaromega) - matrix.VamR(6, Re, 2, -2, -1, kzz, az, shbaromega))) )
                                              + Vam013_6*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( 1/2*(matrix.VamR(6, Re, 3, 0, 1, kzz, az, shbaromega) - matrix.VamR(6, Re, 3, 0, -1, kzz, az, shbaromega))*2 )

                                              + Vam011_8*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( 1/2*(matrix.VamR(8, Re, 1, 0, 1, kzz, az, shbaromega) - matrix.VamR(8, Re, 1, 0, -1, kzz, az, shbaromega))*2 )
                                              + Vam012_8*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( 1/2*(matrix.VamR(8, Re, 2, 0, 1, kzz, az, shbaromega) - matrix.VamR(8, Re, 2, 0, -1, kzz, az, shbaromega))*2 )
                                              + Vam212_8*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( 1/1*((matrix.VamR(8, Re, 2, 2, 1, kzz, az, shbaromega) - matrix.VamR(8, Re, 2, -2, -1, kzz, az, shbaromega)) + pow(-1, +2)*(matrix.VamR(8, Re, 2, -2, 1, kzz, az, shbaromega) - matrix.VamR(8, Re, 2, -2, -1, kzz, az, shbaromega))) )
                                              + Vam013_8*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( 1/2*(matrix.VamR(8, Re, 3, 0, 1, kzz, az, shbaromega) - matrix.VamR(8, Re, 3, 0, -1, kzz, az, shbaromega))*2 )

                                              + Vam011_10*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( 1/2*(matrix.VamR(10, Re, 1, 0, 1, kzz, az, shbaromega) - matrix.VamR(10, Re, 1, 0, -1, kzz, az, shbaromega))*2 )
                                              + Vam012_10*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( 1/2*(matrix.VamR(10, Re, 2, 0, 1, kzz, az, shbaromega) - matrix.VamR(10, Re, 2, 0, -1, kzz, az, shbaromega))*2 )
                                              + Vam212_10*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( 1/1*((matrix.VamR(10, Re, 2, 2, 1, kzz, az, shbaromega) - matrix.VamR(10, Re, 2, -2, -1, kzz, az, shbaromega)) + pow(-1, +2)*(matrix.VamR(10, Re, 2, -2, 1, kzz, az, shbaromega) - matrix.VamR(10, Re, 2, -2, -1, kzz, az, shbaromega))) )
                                              + Vam013_10*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( 1/2*(matrix.VamR(10, Re, 3, 0, 1, kzz, az, shbaromega) - matrix.VamR(10, Re, 3, 0, -1, kzz, az, shbaromega))*2 );
                                            
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    //PRINT_MAT(result);
    return result;
}

//C3v  //対称性 J. Chern. Phys. 94 (1), 1 January 1991
Eigen::MatrixXd H_C3v_prolate (int n0, int npls, int nmns, int j, int m,    //matrix size
                     double A, double B, double B_large, double C_large, double mu, double Re,   //molecular parameter
                     vector<double> PotParam
                     ) 
{    
    //constant
    double hbar = 1.054571817*pow(10, -34);
    double c = 2.99792458*pow(10, 8);

    double Ix = hbar*hbar/(2*B_large)*5.03412*pow(10, 22);
    double Iz = hbar*hbar/(2*C_large)*5.03412*pow(10, 22); //長さはm単位

    double mub = mu;

    double Re2Ix = (Re*pow(10, -10))*(Re*pow(10, -10))/Ix;
    double omegas = sqrt(2*PotParam[0]*PotParam[1]*PotParam[1]*1.98645*pow(10, -23)*pow(10, 20)/mu);   //単位はs-1
    double omegab = sqrt(2*PotParam[2]*1.98645*pow(10, -23)*pow(10, 20)/mub);   //単位はs-1
    double shbaromega = 1/(2*M_PI)*omegas/c/100;    //単位変換で1/hcをかけ、hbarをかけるため、2\piが必要。
    double bhbaromega = 1/(2*M_PI)*omegab/c/100;
    double ReIxsqrt2mubomegas = Re*pow(10, -10)/Ix*sqrt(2*mub*hbar/omegas);
    //double ReIxsqrt2muomegas = Re*pow(10, -10)/Ix*sqrt(2*mu*hbar/omegas);
    double hbar2Ix = hbar*hbar/Ix*5.03412*pow(10, 22); //1 J = 5.03412 \times 10^22 cm-1
    double hbar2Iz = hbar*hbar/Iz*5.03412*pow(10, 22);
    //double Resqrt2mubhbaromegas = hbar2Ix*Re*pow(10, -10)*sqrt(2*mu*omegas/hbar);
    //double Resqrt2muhbaromegas = hbar2Ix*Re*pow(10, -10)*sqrt(2*mu*omegas/hbar);
    double Vbcoeff = hbar/(2*mub*omegab)*pow(10, 20);
    double Vscoeff = hbar/(2*mu*omegas)*pow(10, 20);

    double kzz = PotParam[0];
    double az = PotParam[1];
    double kxx = PotParam[2];
    double kxxz = PotParam[3];
    double V001 = PotParam[4];
    double V002 = PotParam[5];
    double V022 = PotParam[6];
    double V003 = PotParam[7];
    double V203 = PotParam[8];
    double V303 = PotParam[9];
    double V004 = PotParam[10];
    double VR001 = PotParam[11];
    double VR002 = PotParam[12];
    double VR202 = PotParam[13];
    double VR003 = PotParam[14];
    double VR203 = PotParam[15];
    double VR303 = PotParam[16];
    double VR004 = PotParam[17];
    double VRR001 = PotParam[18];
    double VRR002 = PotParam[19];
    double VRR202 = PotParam[20];
    double VRR003 = PotParam[21];
    double VRR203 = PotParam[22];
    double VRR303 = PotParam[23];
    double VRR004 = PotParam[24];
    double Vrho001 = PotParam[25];
    double Vrho002 = PotParam[26];
    double Vrho202 = PotParam[27];
    double Vrho003 = PotParam[28];
    double Vrho203 = PotParam[29];
    double Vrho303 = PotParam[30];
    double Vrho004 = PotParam[31];
    double Vam011_0 = PotParam[32];
    double Vam012_0 = PotParam[33];
    double Vam022_0 = PotParam[34];
    double Vam212_0 = PotParam[35];
    double Vam222_0 = PotParam[36];
    double Vam013_0 = PotParam[37];
    double Vam023_0 = PotParam[38];
    double Vam011_6 = PotParam[39];
    double Vam012_6 = PotParam[40];
    double Vam022_6 = PotParam[41];
    double Vam212_6 = PotParam[42];
    double Vam222_6 = PotParam[43];
    double Vam013_6 = PotParam[44];
    double Vam023_6 = PotParam[45];
    double Vam011_8 = PotParam[46];
    double Vam012_8 = PotParam[47];
    double Vam022_8 = PotParam[48];
    double Vam212_8 = PotParam[49];
    double Vam222_8 = PotParam[50];
    double Vam013_8 = PotParam[51];
    double Vam023_8 = PotParam[52];
    double Vam011_10 = PotParam[53];
    double Vam012_10 = PotParam[54];
    double Vam022_10 = PotParam[55];
    double Vam212_10 = PotParam[56];
    double Vam222_10 = PotParam[57];
    double Vam013_10 = PotParam[58];
    double Vam023_10 = PotParam[59];

    MatrixParameter dim(n0, npls, nmns, j, m, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
    //vector<vector<double>> result(dim.matrix_size(), vector<double>(dim.matrix_size()));
    Eigen::MatrixXd result = Eigen::MatrixXd::Ones(dim.matrix_size(), dim.matrix_size());
    vector<int> drow(1, 0);
    vector<int> ddrow(1, 0);
    int dddrow= 0;
    for (int mBrow = - j; mBrow <= j; mBrow++) {                                                    // assign row mB
        for (int vrow = abs(m - mBrow); vrow <= (npls + nmns - abs(m - mBrow)); vrow += 2) {  //assign row v
            int jrdim = 0;
            int jdrow;
            for (int num = 0; num<= j; num++) {
                jdrow = (2 * abs(num) + 1);
                jrdim += jdrow;
            }
            int mrminus = 0;
            int mmmrow;
            for (int mm = 0; mm <= abs(mBrow); mm++) {
                if (mm == 0) {
                    mmmrow = 0;
                }
                else {
                    mmmrow = (2 * (abs(mm) - 1) + 1);
                }
                mrminus += mmmrow;
            }
            int d = (npls + 1 - abs(m - mBrow))*(jrdim - mrminus);
            drow.push_back(d);
            if (d != drow[drow.size() - 2]) {
                ddrow.push_back(d);
                dddrow += ddrow[ddrow.size() - 2];
            }

            vector<int> dcolumn(1, 0);
            vector<int> ddcolumn(1, 0);
            int dddcolumn = 0;
            for (int mBcolumn = - j; mBcolumn <= j; mBcolumn++) {                                       // assign column mB
                for (int vcolumn = abs(m - mBcolumn); vcolumn <= (npls + nmns - abs(m - mBcolumn)); vcolumn += 2) {   // assign column v
                    int jcdim = 0;
                    int jdcolumn;
                    for (int num = 0; num<= j; num++) {
                        jdcolumn = (2 * abs(num) + 1);
                        jcdim += jdcolumn;
                        }
                    int mcminus = 0;
                    int mmmcolumn;
                    for (int mm = 0; mm <= abs(mBcolumn); mm++) {
                        if (mm == 0) {
                            mmmcolumn = 0;
                        }
                        else {
                            mmmcolumn = (2 * (abs(mm) - 1) + 1);
                        }
                        mcminus += mmmcolumn;
                    }
                    int d = (npls + 1 - abs(m - mBcolumn))*(jcdim - mcminus);
                    dcolumn.push_back(d);
                    if (d != dcolumn[dcolumn.size() - 2]) { //dcolumn.size() - 2 > 0の条件を追加したらエラーが消えるかもしれない．
                        ddcolumn.push_back(d);
                        dddcolumn += ddcolumn[ddcolumn.size() - 2];
                    }

                    #pragma omp parallel for num_threads(12)
                    for (int jrow = abs(mBrow); jrow <= j; jrow++) {                                            // assign row j
                        for (int krow = - jrow; krow <= jrow; krow++) {                                         // assign row k
                            for (int n0row = 0; n0row <= n0; n0row++) {                                         // assign row n0
                                for (int jcolumn = abs(mBcolumn); jcolumn <= j; jcolumn++) {                                                // assign column j      
                                    for (int kcolumn = - jcolumn; kcolumn <= jcolumn; kcolumn++) {                                          // assign column k
                                        for (int n0column = 0; n0column <= n0; n0column++) {                                                // assign column n0
                                            // matrix element
                                            MatrixElement matrix(n0, npls, nmns, j, m, jrow, mBrow, krow, n0row, vrow, jcolumn, mBcolumn, kcolumn, n0column, vcolumn);
                                            result(dddrow + matrix.row(), dddcolumn + matrix.column())
                                             = 

                                              - bhbaromega/4*(
                                                + (1 + Re2Ix*mu)*matrix.Tb()    //Tb
                                                + ReIxsqrt2mubomegas*sqrt(mub/mu)*matrix.Tb_1()
                                                + hbar2Ix/2*1/shbaromega*mub/mu*matrix.Tb_2()
                                                )

                                              - shbaromega/4*matrix.Ts()    //Ts
                                                - hbar2Ix/4*omegas/omegab*mu/mub*matrix.Ts_1()
                                            
                                              
                                              + hbar2Iz*matrix.T_3_1()
                                              - hbar2Ix/2*matrix.T_4_1()
                                              //+ Resqrt2mubhbaromegas/2*matrix.T_4_2()
                                              + hbar2Ix/2*matrix.T_5_1()
                                              + shbaromega*ReIxsqrt2mubomegas/2*matrix.T_5_2()
                                              + 1/sqrt(2)*hbar2Ix/2*sqrt(omegab/omegas)*sqrt(mub/mu)*matrix.T_6_1()
                                              + 1/sqrt(2)*hbar2Ix/2*sqrt(omegas/omegab)*sqrt(mu/mub)*matrix.T_6_2()
                                              + hbar2Iz*matrix.T_7_1()
                                              
                                              //とりあえずobrateのみ
                                              + B*matrix.Tr()   //Tr
                                              + (A - B)*matrix.Tr_symtop()  
                                              + hbar2Ix*matrix.Tr() + (hbar2Iz - hbar2Ix)*matrix.Tr_1()
                                              
                                              + kzz*matrix.Vs(kzz, az, shbaromega)  //Vs
                                              + bhbaromega/4*matrix.Vb()    //Vb  //Vxx termは入れてない。
                                            
                                              //Vr
                                              + V001*( (1 + 2*(cos(2*M_PI*0/3)))/6*matrix.Vr(1, 0)*2 )
                                              + V002*( (1 + 2*(cos(2*M_PI*0/3)))/6*matrix.Vr(2, 0)*2 )
                                              + V003*( (1 + 2*(cos(2*M_PI*0/3)))/6*matrix.Vr(3, 0)*2 ) 
                                              + V303*( (1 + 2*(cos(2*M_PI*(+ 3)/3)))/6*(matrix.Vr(3, +3) + pow(-1, +3)*matrix.Vr(3, -3)) )
                                            
                                              //Vsb
                                              + kxxz*Vbcoeff*matrix.Vsb(kzz, az, shbaromega)
                                            
                                              //Vsr
                                              + VR001*sqrt( Vscoeff )*( (1 + 2*(cos(2*M_PI*0/3)))/6*matrix.Vsr(1, 0)*2 )
                                              + VR002*sqrt( Vscoeff )*( (1 + 2*(cos(2*M_PI*0/3)))/6*matrix.Vsr(2, 0)*2 )
                                              + VR003*sqrt( Vscoeff )*( (1 + 2*(cos(2*M_PI*0/3)))/6*matrix.Vsr(3, 0)*2 ) 
                                              + VR303*sqrt( Vscoeff )*( (1 + 2*(cos(2*M_PI*(+ 3)/3)))/6*(matrix.Vsr(3, +3) + pow(-1, +3)*matrix.Vsr(3, -3)) )

                                              //Vssr
                                              + VRR001*( Vscoeff )*( (1 + 2*(cos(2*M_PI*0/3)))/6*matrix.Vssr(1, 0)*2 )
                                              + VRR002*( Vscoeff )*( (1 + 2*(cos(2*M_PI*0/3)))/6*matrix.Vssr(2, 0)*2 )
                                              + VRR003*( Vscoeff )*( (1 + 2*(cos(2*M_PI*0/3)))/6*matrix.Vssr(3, 0)*2 ) 
                                              + VRR303*( Vscoeff )*( (1 + 2*(cos(2*M_PI*3/3)))/6*(matrix.Vssr(3, 3) + pow(-1, 3)*matrix.Vssr(3, -3)) )

                                              //Vbr
                                              + Vrho001*Vbcoeff*( (1 + 2*(cos(2*M_PI*0/3)))/6*matrix.Vbr(1, 0)*2 )
                                              + Vrho002*Vbcoeff*( (1 + 2*(cos(2*M_PI*0/3)))/6*matrix.Vbr(2, 0)*2 )
                                              + Vrho003*Vbcoeff*( (1 + 2*(cos(2*M_PI*0/3)))/6*matrix.Vbr(3, 0)*2 )
                                              + Vrho303*Vbcoeff*( (1 + 2*(cos(2*M_PI*3/3)))/6*(matrix.Vbr(3, 3) + pow(-1, 3)*matrix.Vbr(3, -3)) )
                                              
                                              //Vam
                                              + Vam011_0*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( (1 + 2*(cos(2*M_PI*0/3)))/6*(matrix.Vam(1, 0, 1) - matrix.Vam(1, 0, -1))*2 )
                                              + Vam012_0*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( (1 + 2*(cos(2*M_PI*0/3)))/6*(matrix.Vam(2, 0, 1) - matrix.Vam(2, 0, -1))*2 )
                                              + Vam013_0*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( (1 + 2*(cos(2*M_PI*0/3)))/6*(matrix.Vam(3, 0, 1) - matrix.Vam(3, 0, -1))*2 )
                                              //VamR
                                              + Vam011_6*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( (1 + 2*(cos(2*M_PI*0/3)))/6*(matrix.VamR(6, Re, 1, 0, 1, kzz, az, shbaromega) - matrix.VamR(6, Re, 1, 0, -1, kzz, az, shbaromega))*2  )
                                              + Vam012_6*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( (1 + 2*(cos(2*M_PI*0/3)))/6*(matrix.VamR(6, Re, 2, 0, 1, kzz, az, shbaromega) - matrix.VamR(6, Re, 2, 0, -1, kzz, az, shbaromega))*2  )
                                              + Vam013_6*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( (1 + 2*(cos(2*M_PI*0/3)))/6*(matrix.VamR(6, Re, 3, 0, 1, kzz, az, shbaromega) - matrix.VamR(6, Re, 3, 0, -1, kzz, az, shbaromega))*2  )

                                              + Vam011_8*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( (1 + 2*(cos(2*M_PI*0/3)))/6*(matrix.VamR(8, Re, 1, 0, 1, kzz, az, shbaromega) - matrix.VamR(8, Re, 1, 0, -1, kzz, az, shbaromega))*2  )
                                              + Vam012_8*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( (1 + 2*(cos(2*M_PI*0/3)))/6*(matrix.VamR(8, Re, 2, 0, 1, kzz, az, shbaromega) - matrix.VamR(8, Re, 2, 0, -1, kzz, az, shbaromega))*2  )
                                              + Vam013_8*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( (1 + 2*(cos(2*M_PI*0/3)))/6*(matrix.VamR(8, Re, 3, 0, 1, kzz, az, shbaromega) - matrix.VamR(8, Re, 3, 0, -1, kzz, az, shbaromega))*2  )

                                              + Vam011_10*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( (1 + 2*(cos(2*M_PI*0/3)))/6*(matrix.VamR(10, Re, 1, 0, 1, kzz, az, shbaromega) - matrix.VamR(10, Re, 1, 0, -1, kzz, az, shbaromega))*2  )
                                              + Vam012_10*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( (1 + 2*(cos(2*M_PI*0/3)))/6*(matrix.VamR(10, Re, 2, 0, 1, kzz, az, shbaromega) - matrix.VamR(10, Re, 2, 0, -1, kzz, az, shbaromega))*2  )
                                              + Vam013_10*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( (1 + 2*(cos(2*M_PI*0/3)))/6*(matrix.VamR(10, Re, 3, 0, 1, kzz, az, shbaromega) - matrix.VamR(10, Re, 3, 0, -1, kzz, az, shbaromega))*2  );
                                            
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    //PRINT_MAT(result);
    return result;
}

//C3v  //対称性 J. Chern. Phys. 94 (1), 1 January 1991
Eigen::MatrixXd H_C3v_oblate (int n0, int npls, int nmns, int j, int m,    //matrix size
                     double B, double C, double B_large, double C_large, double mu, double Re,   //molecular parameter
                     vector<double> PotParam
                     ) 
{    
    //constant
    double hbar = 1.054571817*pow(10, -34);
    double c = 2.99792458*pow(10, 8);

    double Ix = hbar*hbar/(2*B_large)*5.03412*pow(10, 22);
    double Iz = hbar*hbar/(2*C_large)*5.03412*pow(10, 22); //長さはm単位

    double mub = mu;

    double Re2Ix = (Re*pow(10, -10))*(Re*pow(10, -10))/Ix;
    double omegas = sqrt(2*PotParam[0]*PotParam[1]*PotParam[1]*1.98645*pow(10, -23)*pow(10, 20)/mu);   //単位はs-1
    double omegab = sqrt(2*PotParam[2]*1.98645*pow(10, -23)*pow(10, 20)/mub);   //単位はs-1
    double shbaromega = 1/(2*M_PI)*omegas/c/100;    //単位変換で1/hcをかけ、hbarをかけるため、2\piが必要。
    double bhbaromega = 1/(2*M_PI)*omegab/c/100;
    double ReIxsqrt2mubomegas = Re*pow(10, -10)/Ix*sqrt(2*mub*hbar/omegas);
    //double ReIxsqrt2muomegas = Re*pow(10, -10)/Ix*sqrt(2*mu*hbar/omegas);
    double hbar2Ix = hbar*hbar/Ix*5.03412*pow(10, 22); //1 J = 5.03412 \times 10^22 cm-1
    double hbar2Iz = hbar*hbar/Iz*5.03412*pow(10, 22);
    //double Resqrt2mubhbaromegas = hbar2Ix*Re*pow(10, -10)*sqrt(2*mu*omegas/hbar);
    //double Resqrt2muhbaromegas = hbar2Ix*Re*pow(10, -10)*sqrt(2*mu*omegas/hbar);
    double Vbcoeff = hbar/(2*mub*omegab)*pow(10, 20);
    double Vscoeff = hbar/(2*mu*omegas)*pow(10, 20);

    double kzz = PotParam[0];
    double az = PotParam[1];
    double kxx = PotParam[2];
    double kxxz = PotParam[3];
    double V001 = PotParam[4];
    double V002 = PotParam[5];
    double V022 = PotParam[6];
    double V003 = PotParam[7];
    double V203 = PotParam[8];
    double V303 = PotParam[9];
    double V004 = PotParam[10];
    double VR001 = PotParam[11];
    double VR002 = PotParam[12];
    double VR202 = PotParam[13];
    double VR003 = PotParam[14];
    double VR203 = PotParam[15];
    double VR303 = PotParam[16];
    double VR004 = PotParam[17];
    double VRR001 = PotParam[18];
    double VRR002 = PotParam[19];
    double VRR202 = PotParam[20];
    double VRR003 = PotParam[21];
    double VRR203 = PotParam[22];
    double VRR303 = PotParam[23];
    double VRR004 = PotParam[24];
    double Vrho001 = PotParam[25];
    double Vrho002 = PotParam[26];
    double Vrho202 = PotParam[27];
    double Vrho003 = PotParam[28];
    double Vrho203 = PotParam[29];
    double Vrho303 = PotParam[30];
    double Vrho004 = PotParam[31];
    double Vam011_0 = PotParam[32];
    double Vam012_0 = PotParam[33];
    double Vam022_0 = PotParam[34];
    double Vam212_0 = PotParam[35];
    double Vam222_0 = PotParam[36];
    double Vam013_0 = PotParam[37];
    double Vam023_0 = PotParam[38];
    double Vam011_6 = PotParam[39];
    double Vam012_6 = PotParam[40];
    double Vam022_6 = PotParam[41];
    double Vam212_6 = PotParam[42];
    double Vam222_6 = PotParam[43];
    double Vam013_6 = PotParam[44];
    double Vam023_6 = PotParam[45];
    double Vam011_8 = PotParam[46];
    double Vam012_8 = PotParam[47];
    double Vam022_8 = PotParam[48];
    double Vam212_8 = PotParam[49];
    double Vam222_8 = PotParam[50];
    double Vam013_8 = PotParam[51];
    double Vam023_8 = PotParam[52];
    double Vam011_10 = PotParam[53];
    double Vam012_10 = PotParam[54];
    double Vam022_10 = PotParam[55];
    double Vam212_10 = PotParam[56];
    double Vam222_10 = PotParam[57];
    double Vam013_10 = PotParam[58];
    double Vam023_10 = PotParam[59];

    MatrixParameter dim(n0, npls, nmns, j, m, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
    //vector<vector<double>> result(dim.matrix_size(), vector<double>(dim.matrix_size()));
    Eigen::MatrixXd result = Eigen::MatrixXd::Ones(dim.matrix_size(), dim.matrix_size());
    vector<int> drow(1, 0);
    vector<int> ddrow(1, 0);
    int dddrow= 0;
    for (int mBrow = - j; mBrow <= j; mBrow++) {                                                    // assign row mB
        for (int vrow = abs(m - mBrow); vrow <= (npls + nmns - abs(m - mBrow)); vrow += 2) {  //assign row v
            int jrdim = 0;
            int jdrow;
            for (int num = 0; num<= j; num++) {
                jdrow = (2 * abs(num) + 1);
                jrdim += jdrow;
            }
            int mrminus = 0;
            int mmmrow;
            for (int mm = 0; mm <= abs(mBrow); mm++) {
                if (mm == 0) {
                    mmmrow = 0;
                }
                else {
                    mmmrow = (2 * (abs(mm) - 1) + 1);
                }
                mrminus += mmmrow;
            }
            int d = (npls + 1 - abs(m - mBrow))*(jrdim - mrminus);
            drow.push_back(d);
            if (d != drow[drow.size() - 2]) {
                ddrow.push_back(d);
                dddrow += ddrow[ddrow.size() - 2];
            }

            vector<int> dcolumn(1, 0);
            vector<int> ddcolumn(1, 0);
            int dddcolumn = 0;
            for (int mBcolumn = - j; mBcolumn <= j; mBcolumn++) {                                       // assign column mB
                for (int vcolumn = abs(m - mBcolumn); vcolumn <= (npls + nmns - abs(m - mBcolumn)); vcolumn += 2) {   // assign column v
                    int jcdim = 0;
                    int jdcolumn;
                    for (int num = 0; num<= j; num++) {
                        jdcolumn = (2 * abs(num) + 1);
                        jcdim += jdcolumn;
                        }
                    int mcminus = 0;
                    int mmmcolumn;
                    for (int mm = 0; mm <= abs(mBcolumn); mm++) {
                        if (mm == 0) {
                            mmmcolumn = 0;
                        }
                        else {
                            mmmcolumn = (2 * (abs(mm) - 1) + 1);
                        }
                        mcminus += mmmcolumn;
                    }
                    int d = (npls + 1 - abs(m - mBcolumn))*(jcdim - mcminus);
                    dcolumn.push_back(d);
                    if (d != dcolumn[dcolumn.size() - 2]) { //dcolumn.size() - 2 > 0の条件を追加したらエラーが消えるかもしれない．
                        ddcolumn.push_back(d);
                        dddcolumn += ddcolumn[ddcolumn.size() - 2];
                    }

                    #pragma omp parallel for num_threads(12)
                    for (int jrow = abs(mBrow); jrow <= j; jrow++) {                                            // assign row j
                        for (int krow = - jrow; krow <= jrow; krow++) {                                         // assign row k
                            for (int n0row = 0; n0row <= n0; n0row++) {                                         // assign row n0
                                for (int jcolumn = abs(mBcolumn); jcolumn <= j; jcolumn++) {                                                // assign column j      
                                    for (int kcolumn = - jcolumn; kcolumn <= jcolumn; kcolumn++) {                                          // assign column k
                                        for (int n0column = 0; n0column <= n0; n0column++) {                                                // assign column n0
                                            // matrix element
                                            MatrixElement matrix(n0, npls, nmns, j, m, jrow, mBrow, krow, n0row, vrow, jcolumn, mBcolumn, kcolumn, n0column, vcolumn);
                                            result(dddrow + matrix.row(), dddcolumn + matrix.column())
                                             = 

                                              - bhbaromega/4*(
                                                + (1 + Re2Ix*mu)*matrix.Tb()    //Tb
                                                + ReIxsqrt2mubomegas*sqrt(mub/mu)*matrix.Tb_1()
                                                + hbar2Ix/2*1/shbaromega*mub/mu*matrix.Tb_2()
                                                )

                                              - shbaromega/4*matrix.Ts()    //Ts
                                                - hbar2Ix/4*omegas/omegab*mu/mub*matrix.Ts_1()
                                            
                                              
                                              + hbar2Iz*matrix.T_3_1()
                                              - hbar2Ix/2*matrix.T_4_1()
                                              //+ Resqrt2mubhbaromegas/2*matrix.T_4_2()
                                              + hbar2Ix/2*matrix.T_5_1()
                                              + shbaromega*ReIxsqrt2mubomegas/2*matrix.T_5_2()
                                              + 1/sqrt(2)*hbar2Ix/2*sqrt(omegab/omegas)*sqrt(mub/mu)*matrix.T_6_1()
                                              + 1/sqrt(2)*hbar2Ix/2*sqrt(omegas/omegab)*sqrt(mu/mub)*matrix.T_6_2()
                                              + hbar2Iz*matrix.T_7_1()
                                              
                                              //とりあえずobrateのみ
                                              + B*matrix.Tr()   //Tr
                                              + (B - C)*matrix.Tr_symtop()  
                                              + hbar2Ix*matrix.Tr() + (hbar2Iz - hbar2Ix)*matrix.Tr_1()
                                              
                                              + kzz*matrix.Vs(kzz, az, shbaromega)  //Vs
                                              + bhbaromega/4*matrix.Vb()    //Vb  //Vxx termは入れてない。
                                            
                                              //Vr
                                              + V001*( (1 + 2*(cos(2*M_PI*0/3)))/6*matrix.Vr(1, 0)*2 )
                                              + V002*( (1 + 2*(cos(2*M_PI*0/3)))/6*matrix.Vr(2, 0)*2 )
                                              + V003*( (1 + 2*(cos(2*M_PI*0/3)))/6*matrix.Vr(3, 0)*2 ) 
                                              + V303*( (1 + 2*(cos(2*M_PI*(+ 3)/3)))/6*(matrix.Vr(3, +3) + pow(-1, +3)*matrix.Vr(3, -3)) )
                                            
                                              //Vsb
                                              + kxxz*Vbcoeff*matrix.Vsb(kzz, az, shbaromega)
                                            
                                              //Vsr
                                              + VR001*sqrt( Vscoeff )*( (1 + 2*(cos(2*M_PI*0/3)))/6*matrix.Vsr(1, 0)*2 )
                                              + VR002*sqrt( Vscoeff )*( (1 + 2*(cos(2*M_PI*0/3)))/6*matrix.Vsr(2, 0)*2 )
                                              + VR003*sqrt( Vscoeff )*( (1 + 2*(cos(2*M_PI*0/3)))/6*matrix.Vsr(3, 0)*2 ) 
                                              + VR303*sqrt( Vscoeff )*( (1 + 2*(cos(2*M_PI*(+ 3)/3)))/6*(matrix.Vsr(3, +3) + pow(-1, +3)*matrix.Vsr(3, -3)) )

                                              //Vssr
                                              + VRR001*( Vscoeff )*( (1 + 2*(cos(2*M_PI*0/3)))/6*matrix.Vssr(1, 0)*2 )
                                              + VRR002*( Vscoeff )*( (1 + 2*(cos(2*M_PI*0/3)))/6*matrix.Vssr(2, 0)*2 )
                                              + VRR003*( Vscoeff )*( (1 + 2*(cos(2*M_PI*0/3)))/6*matrix.Vssr(3, 0)*2 ) 
                                              + VRR303*( Vscoeff )*( (1 + 2*(cos(2*M_PI*3/3)))/6*(matrix.Vssr(3, 3) + pow(-1, 3)*matrix.Vssr(3, -3)) )

                                              //Vbr
                                              + Vrho001*Vbcoeff*( (1 + 2*(cos(2*M_PI*0/3)))/6*matrix.Vbr(1, 0)*2 )
                                              + Vrho002*Vbcoeff*( (1 + 2*(cos(2*M_PI*0/3)))/6*matrix.Vbr(2, 0)*2 )
                                              + Vrho003*Vbcoeff*( (1 + 2*(cos(2*M_PI*0/3)))/6*matrix.Vbr(3, 0)*2 )
                                              + Vrho303*Vbcoeff*( (1 + 2*(cos(2*M_PI*3/3)))/6*(matrix.Vbr(3, 3) + pow(-1, 3)*matrix.Vbr(3, -3)) )
                                              
                                              //Vam
                                              + Vam011_0*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( (1 + 2*(cos(2*M_PI*0/3)))/6*(matrix.Vam(1, 0, 1) - matrix.Vam(1, 0, -1))*2 )
                                              + Vam012_0*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( (1 + 2*(cos(2*M_PI*0/3)))/6*(matrix.Vam(2, 0, 1) - matrix.Vam(2, 0, -1))*2 )
                                              + Vam013_0*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( (1 + 2*(cos(2*M_PI*0/3)))/6*(matrix.Vam(3, 0, 1) - matrix.Vam(3, 0, -1))*2 )
                                              //VamR
                                              + Vam011_6*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( (1 + 2*(cos(2*M_PI*0/3)))/6*(matrix.VamR(6, Re, 1, 0, 1, kzz, az, shbaromega) - matrix.VamR(6, Re, 1, 0, -1, kzz, az, shbaromega))*2  )
                                              + Vam012_6*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( (1 + 2*(cos(2*M_PI*0/3)))/6*(matrix.VamR(6, Re, 2, 0, 1, kzz, az, shbaromega) - matrix.VamR(6, Re, 2, 0, -1, kzz, az, shbaromega))*2  )
                                              + Vam013_6*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( (1 + 2*(cos(2*M_PI*0/3)))/6*(matrix.VamR(6, Re, 3, 0, 1, kzz, az, shbaromega) - matrix.VamR(6, Re, 3, 0, -1, kzz, az, shbaromega))*2  )

                                              + Vam011_8*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( (1 + 2*(cos(2*M_PI*0/3)))/6*(matrix.VamR(8, Re, 1, 0, 1, kzz, az, shbaromega) - matrix.VamR(8, Re, 1, 0, -1, kzz, az, shbaromega))*2  )
                                              + Vam012_8*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( (1 + 2*(cos(2*M_PI*0/3)))/6*(matrix.VamR(8, Re, 2, 0, 1, kzz, az, shbaromega) - matrix.VamR(8, Re, 2, 0, -1, kzz, az, shbaromega))*2  )
                                              + Vam013_8*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( (1 + 2*(cos(2*M_PI*0/3)))/6*(matrix.VamR(8, Re, 3, 0, 1, kzz, az, shbaromega) - matrix.VamR(8, Re, 3, 0, -1, kzz, az, shbaromega))*2  )

                                              + Vam011_10*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( (1 + 2*(cos(2*M_PI*0/3)))/6*(matrix.VamR(10, Re, 1, 0, 1, kzz, az, shbaromega) - matrix.VamR(10, Re, 1, 0, -1, kzz, az, shbaromega))*2  )
                                              + Vam012_10*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( (1 + 2*(cos(2*M_PI*0/3)))/6*(matrix.VamR(10, Re, 2, 0, 1, kzz, az, shbaromega) - matrix.VamR(10, Re, 2, 0, -1, kzz, az, shbaromega))*2  )
                                              + Vam013_10*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( (1 + 2*(cos(2*M_PI*0/3)))/6*(matrix.VamR(10, Re, 3, 0, 1, kzz, az, shbaromega) - matrix.VamR(10, Re, 3, 0, -1, kzz, az, shbaromega))*2  );
                                            
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    //PRINT_MAT(result);
    return result;
}



//Td symmetry
Eigen::MatrixXd H_Td (int n0, int npls, int nmns, int j, int m,    //matrix size
                     double B, double B_large, double C_large, double mu, double Re,   //molecular parameter
                     vector<double> PotParam
                     ) 
{    
    //constant
    double hbar = 1.054571817*pow(10, -34);
    double c = 2.99792458*pow(10, 8);

    double Ix = hbar*hbar/(2*B_large)*5.03412*pow(10, 22);
    double Iz = hbar*hbar/(2*C_large)*5.03412*pow(10, 22); //長さはm単位

    double mub = mu;

    double Re2Ix = (Re*pow(10, -10))*(Re*pow(10, -10))/Ix;
    double omegas = sqrt(2*PotParam[0]*PotParam[1]*PotParam[1]*1.98645*pow(10, -23)*pow(10, 20)/mu);   //単位はs-1
    double omegab = sqrt(2*PotParam[2]*1.98645*pow(10, -23)*pow(10, 20)/mub);   //単位はs-1
    double shbaromega = 1/(2*M_PI)*omegas/c/100;    //単位変換で1/hcをかけ、hbarをかけるため、2\piが必要。
    double bhbaromega = 1/(2*M_PI)*omegab/c/100;
    double ReIxsqrt2mubomegas = Re*pow(10, -10)/Ix*sqrt(2*mub*hbar/omegas);
    double ReIxsqrt2muomegas = Re*pow(10, -10)/Ix*sqrt(2*mu*hbar/omegas);
    double hbar2Ix = hbar*hbar/Ix*5.03412*pow(10, 22); //1 J = 5.03412 \times 10^22 cm-1
    double hbar2Iz = hbar*hbar/Iz*5.03412*pow(10, 22);
    double Resqrt2mubhbaromegas = hbar2Ix*Re*pow(10, -10)*sqrt(2*mu*omegas/hbar);
    double Resqrt2muhbaromegas = hbar2Ix*Re*pow(10, -10)*sqrt(2*mu*omegas/hbar);
    double omegasomegab = shbaromega/bhbaromega;
    double Vbcoeff = hbar/(2*mub*omegab)*pow(10, 20);
    double Vscoeff = hbar/(2*mu*omegas)*pow(10, 20);
    /*
    cout << "bhbaromega ,\t" << bhbaromega << endl;
    cout << "shbaromega ,\t" << shbaromega << endl;

    cout << "hbar2Iz,\t" << hbar*hbar/Iz*5.03412*pow(10, 22) << endl;
    cout << "hbar2Ix,\t" << hbar*hbar/Ix*5.03412*pow(10, 22) << endl;

    cout << "hbar/(mu*omegab) ,\t" << hbar/(mu*omegab) << endl;

    cout << "ReIxsqrt2mubomegas ,\t" << ReIxsqrt2mubomegas << endl;
    cout << "ReIxsqrt2muomegas ,\t" << ReIxsqrt2muomegas << endl;
    cout << "hbar2Ix ,\t" << hbar2Ix << endl;

    cout << "- Resqrt2mubhbaromegas/2 ,\t" << - Resqrt2mubhbaromegas/2 << endl;

    cout << "matrix.Tb() " << "\t" << bhbaromega/4*(1 + Re2Ix*mu) << endl;
    cout << "matrix.Tb_1()" << "\t" << bhbaromega/4*ReIxsqrt2mubomegas*sqrt(mub/mu) << endl;
    cout << "matrix.Tb_2()" << "\t" << bhbaromega/4*hbar2Ix/2*1/shbaromega*mub/mu << endl;

    cout << "matrix.Ts()" << "\t" << shbaromega/4 << endl;
    cout << "matrix.Ts_1()" << "\t" << hbar2Ix/4*omegas/omegab << "\n" << endl;

    cout << "matrix.T_3_1()" << "\t" << - hbar2Iz << endl;
    cout << "matrix.T_4_1()" << "\t" << + hbar2Ix/2 << endl;
    cout << "matrix.T_5_1()" << "\t" << - hbar2Ix/2 << endl;
    cout << "matrix.T_5_2()" << "\t" << - shbaromega*ReIxsqrt2mubomegas/2 << endl;
    cout << "matrix.T_6_1()" << "\t" << + 1/sqrt(2)*hbar2Ix/2*sqrt(omegab/omegas)*sqrt(mub/mu) << endl;
    cout << "matrix.T_6_2()" << "\t" << + 1/sqrt(2)*hbar2Ix/2*sqrt(omegas/omegab)*sqrt(mu/mub) << endl;
    cout << "matrix.T_7_1()" << "\t" << hbar2Iz << endl;

    cout << "matrix.Tr()" << "\t" << + B << endl;
    cout << "hbar2Ix" << "\t" << hbar2Ix << endl;
    cout << "matrix.Tr_1()" << "\t" << (hbar2Iz - hbar2Ix) << endl;
    cout << "matrix.Vb()" << "\t" <<bhbaromega/4 << endl;
    cout << "omegas" << "\t" << omegas << endl;
    cout << "omegab" << "\t" << omegab << endl;
    */
    double kzz = PotParam[0];
    double az = PotParam[1];
    double kxx = PotParam[2];
    double kxxz = PotParam[3];
    double V001 = PotParam[4];
    double V002 = PotParam[5];
    double V022 = PotParam[6];
    double V003 = PotParam[7];
    double V203 = PotParam[8];
    double V303 = PotParam[9];
    double V004 = PotParam[10];
    double VR001 = PotParam[11];
    double VR002 = PotParam[12];
    double VR202 = PotParam[13];
    double VR003 = PotParam[14];
    double VR203 = PotParam[15];
    double VR303 = PotParam[16];
    double VR004 = PotParam[17];
    double VRR001 = PotParam[18];
    double VRR002 = PotParam[19];
    double VRR202 = PotParam[20];
    double VRR003 = PotParam[21];
    double VRR203 = PotParam[22];
    double VRR303 = PotParam[23];
    double VRR004 = PotParam[24];
    double Vrho001 = PotParam[25];
    double Vrho002 = PotParam[26];
    double Vrho202 = PotParam[27];
    double Vrho003 = PotParam[28];
    double Vrho203 = PotParam[29];
    double Vrho303 = PotParam[30];
    double Vrho004 = PotParam[31];
    double Vam011_0 = PotParam[32];
    double Vam012_0 = PotParam[33];
    double Vam022_0 = PotParam[34];
    double Vam212_0 = PotParam[35];
    double Vam222_0 = PotParam[36];
    double Vam013_0 = PotParam[37];
    double Vam023_0 = PotParam[38];
    double Vam011_6 = PotParam[39];
    double Vam012_6 = PotParam[40];
    double Vam022_6 = PotParam[41];
    double Vam212_6 = PotParam[42];
    double Vam222_6 = PotParam[43];
    double Vam013_6 = PotParam[44];
    double Vam023_6 = PotParam[45];
    double Vam011_8 = PotParam[46];
    double Vam012_8 = PotParam[47];
    double Vam022_8 = PotParam[48];
    double Vam212_8 = PotParam[49];
    double Vam222_8 = PotParam[50];
    double Vam013_8 = PotParam[51];
    double Vam023_8 = PotParam[52];
    double Vam011_10 = PotParam[53];
    double Vam012_10 = PotParam[54];
    double Vam022_10 = PotParam[55];
    double Vam212_10 = PotParam[56];
    double Vam222_10 = PotParam[57];
    double Vam013_10 = PotParam[58];
    double Vam023_10 = PotParam[59];

    MatrixParameter dim(n0, npls, nmns, j, m, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
    //vector<vector<double>> result(dim.matrix_size(), vector<double>(dim.matrix_size()));
    Eigen::MatrixXd result = Eigen::MatrixXd::Ones(dim.matrix_size(), dim.matrix_size());
    vector<int> drow(1, 0);
    vector<int> ddrow(1, 0);
    int dddrow= 0;
    for (int mBrow = - j; mBrow <= j; mBrow++) {                                                    // assign row mB
        for (int vrow = abs(m - mBrow); vrow <= (npls + nmns - abs(m - mBrow)); vrow += 2) {  //assign row v
            int jrdim = 0;
            int jdrow;
            for (int num = 0; num<= j; num++) {
                jdrow = (2 * abs(num) + 1);
                jrdim += jdrow;
            }
            int mrminus = 0;
            int mmmrow;
            for (int mm = 0; mm <= abs(mBrow); mm++) {
                if (mm == 0) {
                    mmmrow = 0;
                }
                else {
                    mmmrow = (2 * (abs(mm) - 1) + 1);
                }
                mrminus += mmmrow;
            }
            int d = (npls + 1 - abs(m - mBrow))*(jrdim - mrminus);
            drow.push_back(d);
            if (d != drow[drow.size() - 2]) {
                ddrow.push_back(d);
                dddrow += ddrow[ddrow.size() - 2];
            }

            vector<int> dcolumn(1, 0);
            vector<int> ddcolumn(1, 0);
            int dddcolumn = 0;
            for (int mBcolumn = - j; mBcolumn <= j; mBcolumn++) {                                       // assign column mB
                for (int vcolumn = abs(m - mBcolumn); vcolumn <= (npls + nmns - abs(m - mBcolumn)); vcolumn += 2) {   // assign column v
                    int jcdim = 0;
                    int jdcolumn;
                    for (int num = 0; num<= j; num++) {
                        jdcolumn = (2 * abs(num) + 1);
                        jcdim += jdcolumn;
                        }
                    int mcminus = 0;
                    int mmmcolumn;
                    for (int mm = 0; mm <= abs(mBcolumn); mm++) {
                        if (mm == 0) {
                            mmmcolumn = 0;
                        }
                        else {
                            mmmcolumn = (2 * (abs(mm) - 1) + 1);
                        }
                        mcminus += mmmcolumn;
                    }
                    int d = (npls + 1 - abs(m - mBcolumn))*(jcdim - mcminus);
                    dcolumn.push_back(d);
                    if (d != dcolumn[dcolumn.size() - 2]) { //dcolumn.size() - 2 > 0の条件を追加したらエラーが消えるかもしれない．
                        ddcolumn.push_back(d);
                        dddcolumn += ddcolumn[ddcolumn.size() - 2];
                    }

                    #pragma omp parallel for num_threads(12)
                    for (int jrow = abs(mBrow); jrow <= j; jrow++) {                                            // assign row j
                        for (int krow = - jrow; krow <= jrow; krow++) {                                         // assign row k
                            for (int n0row = 0; n0row <= n0; n0row++) {                                         // assign row n0
                                for (int jcolumn = abs(mBcolumn); jcolumn <= j; jcolumn++) {                                                // assign column j      
                                    for (int kcolumn = - jcolumn; kcolumn <= jcolumn; kcolumn++) {                                          // assign column k
                                        for (int n0column = 0; n0column <= n0; n0column++) {                                                // assign column n0
                                            // matrix element
                                            MatrixElement matrix(n0, npls, nmns, j, m, jrow, mBrow, krow, n0row, vrow, jcolumn, mBcolumn, kcolumn, n0column, vcolumn);
                                            result(dddrow + matrix.row(), dddcolumn + matrix.column())
                                             = 

                                              - bhbaromega/4*(
                                                + (1 + Re2Ix*mu)*matrix.Tb()    //Tb
                                                + ReIxsqrt2mubomegas*sqrt(mub/mu)*matrix.Tb_1()
                                                + hbar2Ix/2*1/shbaromega*mub/mu*matrix.Tb_2()
                                                )

                                              - shbaromega/4*matrix.Ts()    //Ts
                                                - hbar2Ix/4*omegas/omegab*mu/mub*matrix.Ts_1()
                                            
                                              
                                              + hbar2Iz*matrix.T_3_1()
                                              - hbar2Ix/2*matrix.T_4_1()
                                              //+ Resqrt2mubhbaromegas/2*matrix.T_4_2()
                                              + hbar2Ix/2*matrix.T_5_1()
                                              + shbaromega*ReIxsqrt2mubomegas/2*matrix.T_5_2()
                                              + 1/sqrt(2)*hbar2Ix/2*sqrt(omegab/omegas)*sqrt(mub/mu)*matrix.T_6_1()
                                              + 1/sqrt(2)*hbar2Ix/2*sqrt(omegas/omegab)*sqrt(mu/mub)*matrix.T_6_2()
                                              + hbar2Iz*matrix.T_7_1()
                                              

                                              + B*matrix.Tr()   //Tr
                                              + hbar2Ix*matrix.Tr() + (hbar2Iz - hbar2Ix)*matrix.Tr_1()
                                              
                                              + kzz*matrix.Vs(kzz, az, shbaromega)  //Vs
                                              + bhbaromega/4*matrix.Vb()    //Vb  //Vxx termは入れてない。
                                            
                                              //Vr
                                              + V203*( matrix.Vr(3, 2) + matrix.Vr(3, -2) ) 
                                              + V004*( sqrt(14)*matrix.Vr(4, 0) - sqrt(5)*(matrix.Vr(4, 4) + matrix.Vr(4, -4)) )
                                            
                                              //Vsb
                                              + kxxz*Vbcoeff*matrix.Vsb(kzz, az, shbaromega);
                                            
                                              //Vsr
                                              + VR203*sqrt( Vscoeff )*( matrix.Vsr(3, 2) + matrix.Vsr(3, -2) )
                                              + VR004*sqrt( Vscoeff )*( sqrt(14)*matrix.Vsr(4, 0) - sqrt(5)*(matrix.Vsr(4, 4) + matrix.Vsr(4, -4)) )
                                              //Vssr
                                              + VRR203*( Vscoeff )*( matrix.Vssr(3, 2) + matrix.Vssr(3, -2) )
                                              + VRR004*( Vscoeff )*( sqrt(14)*matrix.Vssr(4, 0) - sqrt(5)*(matrix.Vssr(4, 4) + matrix.Vssr(4, -4)) )
                                              //Vbr
                                              + Vrho203*Vbcoeff*( matrix.Vbr(3, 2) + matrix.Vbr(3, -2) )
                                              + Vrho004*Vbcoeff*( sqrt(14)*matrix.Vbr(4, 0) - sqrt(5)*(matrix.Vbr(4, 4) + matrix.Vbr(4, -4)) )
                                              
                                              //Vam
                                              + Vam013_0*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( (matrix.Vam(3, 2, 1) - matrix.Vam(3, 2, -1)) + (matrix.Vam(3, -2, 1) - matrix.Vam(3, -2, -1)) )
                                              //VamR
                                              + Vam013_6*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( (matrix.VamR(6, Re, 3, 2, 1, kzz, az, shbaromega) - matrix.VamR(6, Re, 3, 2, -1, kzz, az, shbaromega)) + (matrix.VamR(6, Re, 3, -2, 1, kzz, az, shbaromega) - matrix.VamR(6, Re, 3, -2, -1, kzz, az, shbaromega)) );
                                              + Vam013_8*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( (matrix.VamR(8, Re, 3, 2, 1, kzz, az, shbaromega) - matrix.VamR(8, Re, 3, 2, -1, kzz, az, shbaromega)) + (matrix.VamR(8, Re, 3, -2, 1, kzz, az, shbaromega) - matrix.VamR(8, Re, 3, -2, -1, kzz, az, shbaromega)) );
                                              + Vam013_10*sqrt(2*Vbcoeff)/Re*sqrt(3/(8*M_PI))*( (matrix.VamR(10, Re, 3, 2, 1, kzz, az, shbaromega) - matrix.VamR(10, Re, 3, 2, -1, kzz, az, shbaromega)) + (matrix.VamR(10, Re, 3, -2, 1, kzz, az, shbaromega) - matrix.VamR(10, Re, 3, -2, -1, kzz, az, shbaromega)) );
                                            
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    //PRINT_MAT(result);
    return result;
}