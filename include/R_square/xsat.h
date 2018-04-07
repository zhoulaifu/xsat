#ifndef _XSAT_H_
#define _XSAT_H_
//MUST BE positive!!
#define EPSILON 1e-10
#include <math.h>
#include <limits.h>
#include <stdint.h>
#include <inttypes.h>



double DLE(double x,double y);
double DLT(double x,double y);
double DGT(double x,double y);
double DGE(double x,double y);
double DEQ(double x,double y);
double DNE(double x,double y);
double  DCONST(double c);
double  BAND(double x,double y);
double  BOR(double x,double y);






double DLE(double x,double y){
  return x<=y?0.0:(x-y)*(x-y);
}
double DLT(double x,double y){

  return DLE(x,nextafter(y,-INFINITY));
  //  return DLE(x-y, - EPSILON);

}

double DGE(double x,double y)  {
   return DLE(y,x);

}
double  DGT(double x,double y)  {
  return DLT(y,x);

}
double DEQ(double x, double y){
    return (x-y)*(x-y);
}
double  DNE(double x,double y) {
  //return 0;
return  (x!=y)?0.0:EPSILON;      
	 
  //return BOR(DLT(x,y),DGT(x,y));
  
}

double DCONST(double c){
  //return 0;
    return c;
  
}



//DIZ can be 2, 3 or undefined, or just defined, namely 1.


//#if DIZ==2 
//double  BAND(double x,double y){ return (x<=y)?y:x ;}
//double  BOR(double x,double y){return x<=y?x:y;}

//#elif DIZ==3
//double  BAND(double x,double y){return (x==0.0 && y== 0.0)?0.0:1.0 ;}
//double  BOR(double x,double y){return (x==0.0 || y==0.0)?0.0:1.0;}


//#else
#define BAND(x,y) x+y
//double  BAND(double x,double y){return x+y;}
double  BOR(double x,double y){return x*y;}
//#endif

#endif
