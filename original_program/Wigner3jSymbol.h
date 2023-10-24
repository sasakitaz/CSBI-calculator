/*  https://nukephysik101.wordpress.com/2019/01/30/3j-6j-9j-symbol-fro-c/ より引用  */
#ifndef WignerSymbols
#define WignerSymbols
#include <stdlib.h>
#include <cmath>
using namespace std;
double factorial(double n){
  if( n < 0 ) return -100.;
  return (n == 1. || n == 0.) ? 1. : factorial(n-1) * n ;
}
 
double CGcoeff(double J, double m, double J1, double m1, double J2, double m2){
  // (J1,m1) + (J2, m2) = (J, m)
 
  if( m != m1 + m2 ) return 0;
 
  double Jmin = abs(J1 - J2);
  double Jmax = J1+J2;
 
  if( J < Jmin || Jmax < J ) return 0;
 
  double s0 = (2*J+1.) * factorial(J+J1-J2) * factorial(J-J1+J2) * factorial(J1+J2-J) / factorial(J+J1+J2 + 1.);
  s0 = sqrt(s0);
 
  double s = factorial(J +m ) * factorial(J -m);
  double s1 = factorial(J1+m1) * factorial(J1-m1);
  double s2 = factorial(J2+m2) * factorial(J2-m2);
  s = sqrt(s * s1 * s2);
 
  //printf(" s0, s = %f , %f \n", s0, s);
 
  int kMax = min( min( J1+J2-J, J1 - m1), J2 + m2);
 
  double CG = 0.;
  for( int k = 0; k <= kMax; k++){
    double k1 = factorial(J1+J2-J-k);
    double k2 = factorial(J1-m1-k);
    double k3 = factorial(J2+m2-k);
    double k4 = factorial(J - J2 + m1 +k);
    double k5 = factorial(J - J1 - m2 +k);
    double temp = pow(-1, k) / (factorial(k) * k1 * k2 * k3 * k4 * k5);
    if( k1 == -100. || k2 == -100. || k3 == -100. || k4 == -100. || k5 == -100. ) temp = 0.;
 
    //printf(" %d | %f \n", k, temp);
    CG += temp;
  }
 
  return s0*s*CG;
 
}
 
double wigner_3j(double J1, double J2, double J3, double m1, double m2, double m3){
 
  // ( J1 J2 J3 ) = (-1)^(J1-J2 - m3)/ sqrt(2*J3+1) * CGcoeff(J3, -m3, J1, m1, J2, m2) 
  // ( m1 m2 m3 )
 
  return pow(-1, J1 - J2 - m3)/sqrt(2*J3+1) * CGcoeff(J3, -m3, J1, m1, J2, m2);
 
}
 
#endif
