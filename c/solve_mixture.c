#include "mex.h"
#include <string.h>
#ifdef BLAS64
#include "blas.h"
#else
#ifdef UNDERSCORE_LAPACK_CALL

extern int dtrsm_(char *side, char *uplo, char *transa, char *diag, 
		  int *m, int *n, double *alpha, double *a, int *lda, 
		  double *b, int *ldb);
#else
extern int dtrsm(char *side, char *uplo, char *transa, char *diag, 
		  int *m, int *n, double *alpha, double *a, int *lda, 
		  double *b, int *ldb);
#endif
#endif

void mexFunction(int nlhs, mxArray *plhs[],
		 int nrhs, const mxArray *prhs[])
{
  mwSize m,n;
	ptrdiff_t m64, n64;
#ifndef BLAS64
	int im,in;
#endif
  double *T,*b,*x;
  char side='L',uplo='U',trans='N',diag='N';
  double one = 1;

  if(nrhs != 2 || nlhs > 1)
    mexErrMsgTxt("Usage: x = solve_triu(T,b)");

  m = mxGetM(prhs[0]);
  n = mxGetN(prhs[0]);
  if(m != n) mexErrMsgTxt("matrix must be square");

  n = mxGetN(prhs[1]);
  T = mxGetPr(prhs[0]);
  b = mxGetPr(prhs[1]);

  if(mxIsSparse(prhs[0]) || mxIsSparse(prhs[1])) {
    mexErrMsgTxt("Sorry, can't handle sparse matrices yet.");
  }
  if(mxGetNumberOfDimensions(prhs[0]) != 2) {
    mexErrMsgTxt("Arguments must be matrices.");
  }
  if(mxGetNumberOfDimensions(prhs[1]) != 2) {
    mexErrMsgTxt("Arguments must be matrices.");
  }

  plhs[0] = mxCreateDoubleMatrix(m, n, mxREAL);
  x = mxGetPr(plhs[0]);
  memcpy(x,b,m*n*sizeof(double));
  b = x;
#ifdef BLAS64
	m64 = m;
	n64 = n;
  dtrsm(&side,&uplo,&trans,&diag,&m64,&n64,&one,T,&m64,x,&m64);
#else
	im = (int)m;
	in = (int)n;
#ifdef UNDERSCORE_LAPACK_CALL
  dtrsm_(&side,&uplo,&trans,&diag,&im,&in,&one,T,&im,x,&im);
#else
  dtrsm(&side,&uplo,&trans,&diag,&im,&in,&one,T,&im,x,&im);
#endif
#endif
}


