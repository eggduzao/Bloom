#include "mex.h"
#include "util.h"

void mexFunction(int nlhs, mxArray *plhs[],
		 int nrhs, const mxArray *prhs[])
{
  mwSize ndims, len, i, nnz;
  mwSize *dims;
  double *indata, *outdata, d;

  if((nlhs > 1) || (nrhs < 1) || (nrhs > 2))    
    mexErrMsgTxt("Usage: x = gammaln(n) or gammaln(n,d)");

  ndims = mxGetNumberOfDimensions(prhs[0]);
  dims = (mwSize*)mxGetDimensions(prhs[0]);
  indata = mxGetPr(prhs[0]);
  len = mxGetNumberOfElements(prhs[0]);

  if(mxIsSparse(prhs[0])) {
    plhs[0] = mxDuplicateArray(prhs[0]);
    nnz = mxGetJc(prhs[0])[mxGetN(prhs[0])];
    if(nnz != mxGetNumberOfElements(prhs[0])) {
      mexErrMsgTxt("Cannot handle sparse n.");
    }
  } else {
    plhs[0] = mxCreateNumericArray(ndims, dims, mxDOUBLE_CLASS, mxREAL);
  }
  outdata = mxGetPr(plhs[0]);

  if(nrhs == 1) {
    for(i=0;i<len;i++)
      *outdata++ = gammaln(*indata++);
  } else {
    if(mxGetNumberOfElements(prhs[1]) != 1) mexErrMsgTxt("d is not scalar.");
    d = *mxGetPr(prhs[1]);
    for(i=0;i<len;i++)
      *outdata++ = gammaln2(*indata++,d);
  }
}


