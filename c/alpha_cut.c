#include "mex.h"
#include "util.h"

void mexFunction(int nlhs, mxArray *plhs[],
		 int nrhs, const mxArray *prhs[])
{
  int rows, cols, len, i, nnz;
  double *indata, *indata2, *outdata;

  if(nrhs != 2)
    mexErrMsgTxt("Usage: di_pochhammer(x,n)");

  if(mxGetNumberOfElements(prhs[0]) == 1) {
    rows = mxGetM(prhs[1]);
    cols = mxGetN(prhs[1]);
  } else {
    rows = mxGetM(prhs[0]);
    cols = mxGetN(prhs[0]);
  }
  indata = mxGetPr(prhs[0]);
  indata2 = mxGetPr(prhs[1]);
  len = rows*cols;

  if(mxIsSparse(prhs[0])) {
    nnz = mxGetJc(prhs[0])[mxGetN(prhs[0])];
    if(nnz != mxGetNumberOfElements(prhs[0])) {
      mexErrMsgTxt("Cannot handle sparse x.  Sorry.");
    }
  }

  if(mxIsSparse(prhs[1])) {
    plhs[0] = mxDuplicateArray(prhs[1]);
    nnz = mxGetJc(prhs[1])[mxGetN(prhs[1])];
    if(mxGetNumberOfElements(prhs[0]) == 1) {
      len = nnz;
    } else if(nnz != mxGetNumberOfElements(prhs[1])) {
      mexErrMsgTxt("Cannot handle sparse n unless length(x)=1.");
    }
  }
  else {
    plhs[0] = mxCreateDoubleMatrix(rows, cols, mxREAL);
  }
  outdata = mxGetPr(plhs[0]);

  if(mxGetNumberOfElements(prhs[0]) == 1) {
    for(i=0;i<len;i++)
      *outdata++ = di_pochhammer(*indata, (int)*indata2++);
  } 
  else if(mxGetNumberOfElements(prhs[1]) == 1) {
    for(i=0;i<len;i++)
      *outdata++ = di_pochhammer(*indata++, (int)*indata2);
  } 
  else {
    if((mxGetM(prhs[1]) != rows) || (mxGetN(prhs[1]) != cols)) 
      mexErrMsgTxt("arguments are not the same size");
    for(i=0;i<len;i++)
      *outdata++ = di_pochhammer(*indata++, (int)*indata2++);
  }
}


