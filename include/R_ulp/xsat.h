#ifndef _XSAT_H_
#define _XSAT_H_
//MUST BE NEAGATIVE!!
#define EPSILON 0
#include <math.h>
#include <limits.h>
#include <stdint.h>
#include <inttypes.h>


/* uint64_t ulp_i(double x, double y) { */
/*   int64_t xx = *((int64_t*)&x); */
/*   xx = xx < 0 ? LLONG_MIN - xx : xx; */
/*   int64_t yy = *((int64_t*)&y); */
/*   yy = yy < 0 ? LLONG_MIN - yy : yy; */
/*   uint64_t ret=xx>=yy?xx-yy:yy-xx; */
/*   //return (double) (ret); */
/*   return  (ret); */
/*   //return ((double)ret)*((double)ret);; */
/* } */

/* uint64_t substract_u64(uint64_t a, uint64_t b){ */
/*   return a > b ? a - b : b - a; */
/* } */
/* void CHECK(double x,double y){ */
/*   if (ulp_i(-x,-y)!=ulp_i(x,y)) */
/*     printf ("****************************************************issue 1 \n"); */
/*   if (x*y>=0 && ulp_i(x,y)!=substract_u64(ulp_i(0,x),ulp_i(0,y))) */
/*     printf ("****************************************************issue 2 \n"); */
/*   if (x*y==0 &&  ulp_i(x,y)!=ulp_i(0,x)+ulp_i(0,y)) */
/*     printf ("****************************************************issue 3 \n"); */
/*   if (x!=y &&  ulp_i(x,y)== 0) */
/*     printf ("****************************************************issue 4 \n"); */
/*   if (x==y &&  ulp_i(x,y)!= 0) */
/*     printf ("****************************************************issue 5 \n"); */
/*   if (ulp_i(x,y)!=ulp_i(y,x)) */
/*     printf ("****************************************************issue 6 \n"); */
/*   if (ulp_i(x,y)!=ulp_i(x,x/2+y/2) + ulp_i(x/2+y/2,y)) */
/*     printf ("****************************************************issue 7 \n"); */
/*   if ( (x<y) && ulp_i(x,y)!=ulp_i(x,nextafter(y,-INFINITY))+1) */
    
/*     printf ("****************************************************issue 8 \n"); */

/*   if ((x>y) && ulp_i(x,y)!=ulp_i(x,nextafter(y,-INFINITY))-1) */
/*     printf ("****************************************************issue 9 \n");   */
	     
/*   return; */
/* } */

double DLE(double x,double y);
double DLT(double x,double y);
double DGT(double x,double y);
double DGE(double x,double y);
double DEQ(double x,double y);
double DNE(double x,double y);

double  BAND(double x,double y);
double  BOR(double x,double y);
float TR32(double x);
double MAX(double a, double b);

double ulp(double x, double y) {
  int64_t xx = *((int64_t*)&x);
  xx = xx < 0 ? LLONG_MIN - xx : xx;
  int64_t yy = *((int64_t*)&y);
  yy = yy < 0 ? LLONG_MIN - yy : yy;
  uint64_t ret=xx>=yy?xx-yy:yy-xx;
  //CHECK(x,y);
  /* if ( ((double)ret)*((double)ret)==0){ */
  /*   printf("*******x = %g, y = %g\n", x,y); */
  /* } */
  return (double) (ret);
  //return ((double)ret)*((double)ret);;
}



double DLE(double x,double y){
  //printf ("x = %g, y = %g\n",x,y);

    
    return x<=y?0.0:ulp(x,y);
  // return x<=y?0.0:(x-y)*(x-y);
  //     return 0;
}
double DLT(double x,double y){
  //  return DLE(x-y,EPSILON);
  //  return DLE(x,y);
  return x<y?0.0:ulp(x,y)+1;
  //return x<y?0.0:ulp(x,nextafter(y,-INFINITY));
  //    return 0;
}

double DGE(double x,double y)  {
   return DLE(y,x);
  //  return 0;
}
double  DGT(double x,double y)  {
  return DLT(y,x);

  //return 0;
}
double DEQ(double x, double y){
  //  return fabs(x-y);
  // return x>y?x-y:y-x;
  //   return (x-y)*(x-y);
  //double a = log2(1+fabs(x)) - log2(1+fabs(y));

  
  return ulp(x,y);
  //  return (x-y)*(x-y);

}
double  DNE(double x,double y) {
  //return 0;
  return  (x==y)?1.0:0.0;      
	 
  //return BOR(DLT(x,y),DGT(x,y));
  
}




//DIZ can be 2, 3 or undefined, or just defined, namely 1.


//#if DIZ==2 
//double  BAND(double x,double y){ return (x<=y)?y:x ;}
//double  BOR(double x,double y){return x<=y?x:y;}

//#elif DIZ==3
//double  BAND(double x,double y){return (x==0.0 && y== 0.0)?0.0:1.0 ;}
//double  BOR(double x,double y){return (x==0.0 || y==0.0)?0.0:1.0;}


//#else
//double  BAND(double x,double y){return x+y;}
//#define BAND(x,y) (x+y)
#define MIN(a, b) (((a) < (b)) ? (a) : (b)) 
double MAX(double a, double b) {
  return (((a) > (b)) ? (a) : (b));
}
double  BAND(double x,double y){return x+y;}
double  BOR(double x,double y){return x*y;}

//#endif
float TR32(double x){
  return (float)x;
}
#endif
